#!/usr/bin/python3
import click
import subprocess
import re
import os
from itertools import takewhile
import locale

PANDOC_CMD = 'pandoc -t markdown-auto_identifiers --wrap=none'.split(' ')
def pandoc_to_markdown(fn):
    try:
        fn = fn.encode(locale.getpreferredencoding())
        r = subprocess.check_output(PANDOC_CMD + [fn], stderr=subprocess.STDOUT)
        return r.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return str(e.output)

def safe_filename(s):
    s = re.sub('(\w)(: +)', r'\1 - ', s)
    for c in '/\\:': s = s.replace(c, '-')
    s = s.replace('"', "'")
    for c in '?<>|*': s = s.replace(c, '_')
    return s.strip()

def until_unchanged(s, f):
    s1 = s
    while True:
        s2 = f(s1)
        if s2 == s1:
            break
        s1 = s2
    return s2

def re_first_match_or_empty(regexp, s):
    m = re.findall(regexp, s)
    return m[0] if m else ''

markdown_header_level = lambda s: len(s)-len(s.lstrip('#'))
def markdown_title(s):
    orig = '/'+s
    s = s.replace('\xa0', ' ') # replace non-breaking space
    invisible_title = re_first_match_or_empty('{.*title="(.+?)".*}', s)
    s = re.sub('(^#+\s+|{.+?})', '', s) # delete header and attributes
    s = re.sub('[\[\]]', '', s)
    s = re.sub('\s+', ' ', s)
    s = s.rstrip()
    s = until_unchanged(s, lambda s: s[1:-1] if s.startswith('[') and s.endswith(']') else s)
    s = until_unchanged(s, lambda s: s[1:-1] if s.startswith('*') and s.endswith('*') else s)
    return s or invisible_title or orig

def list_val_order(lst):
    i = 0
    mapping = {}
    for e in lst:
        if e in mapping: continue
        i += 1
        mapping[e] = i
    return mapping

def find_chapters(src):
    p = re.compile("^#+.+$", re.MULTILINE)
    chapters = [(m.start(), markdown_title(m.group()), markdown_header_level(m.group())) for m in p.finditer(src)]
    if len(chapters) < 2: # try calibre formatting
        p = re.compile("^.+$", re.MULTILINE)
        chapters = [(m.start(), m.group()) for m in p.finditer(src)]
        def calibre_level(s):
            classes = re.findall('{(.+?)}', s)
            if not '.bold' in classes: return 0
            nums = [re.sub('[^\d]', '', c) for c in classes]
            nums = [int(e) for e in nums if e]
            return max(nums)
        chapters = [(c[0], markdown_title(c[1]), calibre_level(c[1])) for c in chapters if calibre_level(c[1])]
    if len(chapters) < 2: # try bold lines
        p = re.compile("^\*\*.+\*\*$", re.MULTILINE)
        chapters = [(m.start(), m.group(), 1) for m in p.finditer(src)]
        font_size = lambda s: int(re_first_match_or_empty('font-size\s*:\s*(\d+)', s.lower()) or '1')
        chapter_font_size = [font_size(c[1]) for c in chapters]
        font_size_order = list_val_order(chapter_font_size)
        chapter_rank = [font_size_order[c] for c in chapter_font_size]
        chapters = [(c[0], markdown_title(c[1]), r) for c, r in zip(chapters, chapter_rank)]
    return chapters

@click.command(help='Select chapters to new markdown file')
@click.argument('filename', type=click.Path(exists=True, dir_okay=False))
@click.option('-i', '--include-filename', is_flag=True, help='Include source file name')
def booksplit(filename, include_filename):
    pandoc_src = pandoc_to_markdown(filename)
    chapters = find_chapters(pandoc_src)
    for i, c in enumerate(chapters, 1):
        next_level = chapters[i][2] if len(chapters) > i else 0
        click.secho(u'% 3d: ' % i, nl=False)
        tree = ''.join(['├─' if next_level > level else '└─' for level in range(1, c[2])])
        click.secho(tree, fg='red', bold=True, nl=False)
        click.secho(c[1], fg='green')
    
    while True:
        selected_index = click.prompt('Select chapter to extract', type=click.IntRange(1, len(chapters)))-1
        selected_level = chapters[selected_index][2]
        selected_chapters = [chapters[selected_index]] + list(takewhile(lambda c: c[2] > selected_level, chapters[selected_index+1:]))
        start_pos = selected_chapters[0][0]
        end_pos = chapters[selected_index+len(selected_chapters)][0] if len(chapters) > selected_index+len(selected_chapters) else len(pandoc_src)

        target_filename = selected_chapters[0][1]
        if len(selected_chapters) <= 3:
            target_filename = ' - '.join(c[1] for c in selected_chapters if c[1] and not c[1].startswith('/'))
        if include_filename:
            base, _ = os.path.splitext(filename)
            target_filename = u'%s - %s' % (base, target_filename)

        target_filename = safe_filename(target_filename + '.md')
        target_filename = click.prompt('Target filename', type=str, default=target_filename)
        with open(target_filename, 'w') as f:
            f.write(pandoc_src[start_pos:end_pos])

if __name__ == '__main__':
    booksplit()