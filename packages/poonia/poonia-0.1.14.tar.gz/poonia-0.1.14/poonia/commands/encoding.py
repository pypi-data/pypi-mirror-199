# -*- coding: utf-8 -*-
import os.path
import codecs
import click
from . import pglob

import unicodedata
def strip_accents(s):
  s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
  s = s.replace('ł', 'l').replace('Ł', 'L')
  return s

def fix_encoding(text, encoding='utf-8'):
  grade = lambda s: sum([s.count(c) for c in u'ąćńłżźę'])
  try:
    decoded = []
    for e in ['windows-1250', 'iso-8859-2', 'utf-8', 'utf-16', 'utf-32']:
      try:
        decoded.append(text.decode(e, 'ignore'))
      except:
        pass
    text = sorted(decoded, key=grade, reverse=True)[0]
  except:
    pass
  text = text[3:] if text[0:3] == codecs.BOM_UTF8 else text
  if encoding == 'ascii':
    return strip_accents(text).encode('utf-8')
  return text.encode(encoding)

@click.command(help='Fix encoding')
@click.option('-ext', '--extension', default='srt,txt,ass')
@click.option('-e', '--encoding', default='utf-8')
@click.option('-r', '--recurse', is_flag=True)
def encoding(extension, encoding, recurse):
    exts = set(extension.split(','))
    to_fix = []
    for fn in pglob('*', recurse=recurse):
        _, ext = os.path.splitext(fn)
        if ext[1:] not in exts: continue
        with open(fn, 'rb') as f:
            text = f.read()
        fixed = fix_encoding(text, encoding)
        if fixed != text: to_fix.append([fn, fixed])
    if not to_fix:
        click.echo('nothing to process')
        return
    click.echo('\n'.join(x[0] for x in to_fix))
    if click.confirm('do you want to continue?'):
        for fn, content in to_fix:
            with open(fn, 'wb') as f:
                f.write(content)
        click.echo('success')