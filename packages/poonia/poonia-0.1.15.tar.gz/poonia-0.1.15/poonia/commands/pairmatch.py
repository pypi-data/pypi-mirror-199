import click
import functools
import os
import re
from collections import defaultdict

def tokenize(s):
    s = s.replace("'", '')
    return [x.strip().lstrip('0') for x in re.split('(\d+|\W+)', s.lower()) if x and not re.findall('^([^a-z0-9]+)$', x)]

def base(fn):
    b, _ = os.path.splitext(fn)
    return b

def ext(fn):
    _, e = os.path.splitext(fn)
    return e

def hasext(fn, ext):
    _, fileext = os.path.splitext(fn)
    return fileext.lstrip('.').lower() in ext

def get_files_with_extensions(exts):
    extensions = set(e.lower() for e in exts)
    return sorted([f for f in os.listdir('.') if os.path.isfile(f) and hasext(f, extensions)])

def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def highrank(arr, key=None):
    if not arr: return []
    if not key: key = lambda x: x
    s = sorted(arr, key=key, reverse=True)
    highkey = key(s[0])
    return [x for x in arr if key(x) == highkey]

def tokenize_unique(arr):
    tokenized = [tokenize(e) for e in arr]
    common = set(functools.reduce(lambda x,y : x.intersection(y), (set(e) for e in tokenized)))
    for c in common:
        for e in tokenized:
            e.remove(c)
    return tokenized

def common_elements(l1, l2):
    return len([x for x in l1 if x in l2])

@click.command(help='Rename files to closest match')
@click.argument('change', type=str, default='srt')
@click.argument('match', type=str, default='mkv,avi,mp4')
def pairmatch(change, match):
    to_match = [x for x in get_files_with_extensions(match.split(','))]
    to_match = list(zip(to_match, tokenize_unique(base(f) for f in to_match)))

    files_to_change = [x for x in get_files_with_extensions(change.split(','))]
    tokens = tokenize_unique(base(e) for e in files_to_change)
    used = set()
    to_rename = []
    for f, t in zip(files_to_change, tokens):
        ranked = [(x[0], common_elements(t, x[1])) for x in to_match if x[0] not in used]
        high = highrank(ranked, key=lambda x: x[1])
        if len(high) == 1:
            new_fn = high[0][0]
            used.add(new_fn)
            to_rename.append([f, base(new_fn) + ext(f)])
        else:
            to_rename.append([f, None])

    errors = {f[1] for f in to_rename if not f[1] or os.path.exists(f[1])}
    to_rename = [(a,b,b in errors) for a,b in to_rename]
    click.echo('Files to rename:')
    for src, dst, err in to_rename:
        click.secho('  %s' % src, nl=False, fg='red' if err else 'blue')
        click.echo(' -> ', nl=False)
        click.secho(dst, fg='green')
    click.echo()
    to_rename = [(a,b) for a,b,c in to_rename if not c]
    if click.confirm('Rename listed files [%d]?' % len(to_rename)):
        for a, b in to_rename:
            os.rename(a, b)