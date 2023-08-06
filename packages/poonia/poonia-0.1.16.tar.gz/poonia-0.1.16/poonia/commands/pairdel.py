import click
import os
from collections import defaultdict

def hasext(fn, ext):
    _, fileext = os.path.splitext(fn)
    return fileext.lstrip('.').lower() in ext

def sizeof_fmt(num, suffix='B'):
    num = float(num)
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

@click.command(help='Delete files without pair')
@click.argument('extensions', type=str, default='jpg,rw2')
def pairdel(extensions):
    extensions = set(e.lower() for e in extensions.split(','))
    files = [f for f in os.listdir('.') if os.path.isfile(f) and hasext(f, extensions)]
    filext = defaultdict(set)
    for fn in files:
        name, ext = os.path.splitext(fn)
        filext[name].add(ext)
    todelete = []
    for fn, fes in filext.items():
        accept = True
        for e in extensions:
            if not any(hasext(fn+fe, [e]) for fe in fes):
                accept = False
        if not accept:
            todelete.append([fn, fes])

    total_bytes = 0
    filenames_to_delete = []
    for fn, fes in sorted(todelete):
        for a in [fn+fe for fe in fes]:
            filenames_to_delete.append(a)
            click.echo(a, nl=False)
            click.echo(' [', nl=False)
            fsize = os.path.getsize(a)
            total_bytes += fsize
            click.secho('%s' % sizeof_fmt(fsize), nl=False, fg='red')
            click.echo(']')
    click.echo()
    if click.confirm('Delete listed files [%s]?' % sizeof_fmt(total_bytes)):
        for a in filenames_to_delete:
            os.remove(a)
            