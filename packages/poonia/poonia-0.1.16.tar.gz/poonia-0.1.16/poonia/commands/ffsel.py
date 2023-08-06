import click
import os
import subprocess
import re
import time
import json
import operator
import sys
import locale
from sys import platform

from functools import reduce
from collections import defaultdict

def group_by(key, seq):
    return dict(reduce(lambda grp, val: grp[key(val)].append(val) or grp, seq, defaultdict(list)))

def get_in(obj, *keys):
    for k in keys:
        v = obj.get(k, None)
        if v is None:
            return None
        obj = v
    return obj

def sget_in(obj, *keys):
    r = get_in(obj, *keys)
    if r is None: return ''
    return str(r)

def findall(regexp, s):
    return [m.groupdict() for m in re.finditer(regexp, s)]

def parse_stream_filters(filter, default_action='-'):
    filters = findall(r'(?P<type>[vas])(?P<action>\+|\-)(?P<text>[^+\s]+)', filter)
    filters = group_by(operator.itemgetter('type'), filters)

    actions_per_type = {t: set(f['action'] for f in fs) for t,fs in filters.items()}
    if any(1 for _,a in actions_per_type.items() if len(a) > 1):
        click.secho('You can use only one filter action type (+ or -) per stream type!', fg='red', err=True)
        sys.exit(1)
    actions_per_type = {t: list(f)[0] for t,f in actions_per_type.items()}
    
    def _filter(stream_type, *identifiers):
        stream_type_id = stream_type[:1]
        action = actions_per_type.get(stream_type_id, default_action)
        if action == '-':
            for f in filters.get(stream_type_id, []):
                if f['text'] in identifiers: return False
            return True
        else:
            for f in filters.get(stream_type_id, []):
                if f['text'] in identifiers: return True
            return False
    return _filter

def parse_default_filters(filter):
    filters = findall(r'(?P<type>[vas])\!(?P<text>\w+)', filter)
    filters = group_by(operator.itemgetter('type'), filters)
    type_index = {}
    def _filter(stream_type, language, index):
        stream_type_id = stream_type[:1]
        if stream_type_id in type_index:
            return type_index[stream_type_id] == index
        for f in filters.get(stream_type_id, []):
            if f['text'] == language:
                type_index[stream_type_id] = index
                return True
        return False
    return _filter

def sizeof_fmt(num, suffix='B'):
    num = float(num)
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

FFPROBE_CMD = 'ffprobe -hide_banner -loglevel fatal -show_error -show_format -show_streams -show_programs -show_chapters -show_private_data -print_format json --'.split(' ')
def ffprobe(fn):
    try:
        fn = fn.encode(locale.getpreferredencoding())
        r = subprocess.check_output(FFPROBE_CMD + [fn], stderr=subprocess.STDOUT)
        return json.loads(r.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        return {'error': str(e.output)}
    return {}


def escape_csv(s):
    if '"' or "," in s:
        return '"%s"' % s.replace('"', '""')
    return s

def escape_cmd(s):
    return "'%s'" % s if ' ' in s else s

def format_seconds(s):
    d = '%.2f' % (s % 1)
    return time.strftime(r'%H:%M:%S', time.gmtime(s)) + d.lstrip('0')

extract_formats = {
  'hdmv_pgs_subtitle': 'sup',
  'subrip': 'srt',
  'aac': 'aac',
  'opus': 'opus'
}

def escape_video_filter_param(s):
    return s.replace('[', r'\[').replace(']', r'\]')

external_languages = ''
def find_external_subtitles(filename):
    from pprint import pprint
    pprint(filename)

@click.command(help='FFMPEG stream operations')
@click.argument('input', nargs=-1, type=click.Path(exists=True))
@click.option('-f', '--filters', default='', help='Filter streams by language (eg. "s+eng a-ger")')
@click.option('--print', 'print_', is_flag=True, help='Print ffmpeg commands')
@click.option('--apply', is_flag=True, help='Run conversion')
@click.option('--hardsub', is_flag=True, help='Run conversion')
@click.option('--force-stereo', is_flag=True, help="Convert 5.1 audio streams to stereo")
@click.option('-c:a', 'acodec', type=click.Choice(['mp3', 'aac', 'opus']), help="Audio codec")
@click.option('-b:a', 'abitrate', type=str, help="Audio bitrate", default='96k')
@click.option('-c:v', 'vcodec', type=click.Choice(['hevc', 'avc']), help="Video codec")
@click.option('--width', type=int, help="Resize video to specified width")
@click.option('-b:v', 'vbitrate', type=str, help="Video bitrate", default='')
@click.option('--crf', default=28, help='Sets quality when converting video')
@click.option('-hw', '--hardware', is_flag=True, help='Use hardware video encoding')
@click.option('-extsub', '--external-subtitles', is_flag=True, help='Find subtitles in external file')
def ffsel(input, filters, print_, apply, hardsub, force_stereo, acodec, abitrate, vcodec, vbitrate, width, crf, hardware, external_subtitles):
    # from pprint import pprint; pprint(input)
    # files = [f for f in os.listdir(input) if os.path.isfile(f) and not f.startswith('.')] if os.path.isdir(input) else [input]
    files = [f for f in input]
    output = []
    
    for f in files:
        if external_subtitles:
            find_external_subtitles(f)

        stream_filter = parse_stream_filters(filters)
        default_filter = parse_default_filters(filters)
        hw_cli = []
        if hardware:
            if platform.startswith('linux'):
                hw_cli = ['-hwaccel', 'auto']
            elif platform.startswith('windows') or platform == 'cygwin':
                hw_cli = ['-hwaccel', 'dxva2']
        cmd = ['ffmpeg'] + hw_cli
        cmd += ['-i', f, '-c', 'copy']
        
        probe = ffprobe(f)
        if not print_:
            click.secho(f, bold=True, nl=False)
            click.secho(' (%s)' % sizeof_fmt(get_in(probe, 'format', 'size') or 0), fg='yellow')
        if not get_in(probe, 'streams'): continue
        
        streams = []
        default_streams = defaultdict(dict)
        input_stream_counter = defaultdict(lambda: -1)
        for s in get_in(probe, 'streams'):
            s_type = get_in(s, 'codec_type') # video, audio, subtitle, attachment
            s_lang = sget_in(s, 'tags', 'language')
            s_index = get_in(s, 'index')
            input_stream_counter[s_type] += 1
            s_index_type = input_stream_counter[s_type]
            s_default = bool(get_in(s, 'disposition', 'default'))

            keep = stream_filter(s_type, *filter(bool, [s_lang, get_in(s, 'channel_layout')]))
            mark_default = default_filter(s_type, s_lang, s_index) if keep else False
            streams.append([s, keep, mark_default, s_index_type])
            if mark_default:
                default_streams[s_type][True] = s_index
            if s_default and not mark_default:
                default_streams[s_type][False] = s_index
        to_undefault = [s[False] for _, s in default_streams.items() if s.get(True) and s.get(False)]

        output_stream_counter = defaultdict(lambda: -1)
        vfilter = []
        if width: vfilter += ['scale=%i:trunc(ow/a/2)*2' % width]
        for s, keep, mark_default, s_index_type in streams:
            s_type = get_in(s, 'codec_type')
            s_info = ''
            if s_type == 'video':
                s_info = '%sx%s' % (get_in(s, 'width'), get_in(s, 'height'))
            elif s_type == 'audio':
                s_info = '%s' % (get_in(s, 'channel_layout'),)
            if get_in(s, 'disposition', 'default'):
                s_info = (s_info + ' default').strip()
            s_index = get_in(s, 'index')
            s_codec = get_in(s, 'codec_name')
            s_lang = sget_in(s, 'tags', 'language')
            unmark_default = s_index in to_undefault
            
            t = ('  ' if keep else ' -') + '%i %s %s %s %s' % (s_index, s_type, s_codec, s_info, s_lang)
            if not print_:
                click.secho(t, fg=('white' if keep else 'red'), nl=False)
                if mark_default:
                    click.secho(' + DEFAULT', fg='green')
                elif unmark_default:
                    click.secho(' - DEFAULT', fg='red')
                else:
                    click.echo()
            if keep:
                if not (hardsub and mark_default and s_type == 'subtitle'):
                    cmd += ['-map', '0:%i'%s_index]
                output_stream_counter[s_type] += 1
                if force_stereo and s_type == 'audio' and get_in(s, 'channel_layout') not in ('stereo', 'mono'):
                    cmd += [
                      '-filter:a:%i' % output_stream_counter[s_type],
                      'pan=stereo|FL < 1.0*FL + 0.707*FC + 0.707*BL|FR < 1.0*FR + 0.707*FC + 0.707*BR'
                    ] if get_in(s, 'channel_layout') == '5.1' else [
                      '-ac:a:%i' % output_stream_counter[s_type],
                      '2'
                    ]
                    cmd += [
                      '-c:a:%i' % output_stream_counter[s_type], acodec or 'aac',
                      '-b:a:%i' % output_stream_counter[s_type], abitrate
                    ]
                elif acodec:
                    cmd += [
                      '-c:a:%i' % output_stream_counter[s_type], acodec or 'aac',
                      '-b:a:%i' % output_stream_counter[s_type], abitrate
                    ]
                if s_type == 'video' and vcodec:
                    cmd += [
                      '-c:v', 'hevc_videotoolbox' if vcodec == 'hevc' else 'h264_videotoolbox' if (hardware and platform == 'darwin') else 'libx265' if vcodec == 'hevc' else 'libx264',
                      '-preset', 'fast'
                    ]
                    cmd += ['-b:v', '%s' % vbitrate] if vbitrate else ['-crf', '%d' % crf]
                if unmark_default:
                    cmd += [
                        '-disposition:%s:%i' % (s_type[0], output_stream_counter[s_type]), '0'
                    ]
                elif hardsub and mark_default and s_type == 'subtitle':
                    vfilter += [
                        'subtitles=%s:si=%i' % (escape_video_filter_param(f), s_index_type)
                    ]
                elif mark_default:
                    cmd += [
                        '-disposition:%s:%i' % (s_type[0], output_stream_counter[s_type]), 'default'
                    ]
        base, ext = os.path.splitext(f)
        if vfilter: cmd += ['-vf', ', '.join(vfilter)]
        cmd += ['out__%s%s' % (base, ext)]
        
        output_command = ' '.join((escape_cmd(c) for c in cmd))
        output += [output_command]
        if print_:
            click.echo(output_command)

    if apply:
        confirmed = click.confirm('Do you want to continue?', abort=True)
        if confirmed:
            for cmd in output:
                os.system(cmd)

if __name__ == '__main__':
    ffsel()
