import click
import os, sys, glob

# ['.EXE', '.BAT']
executable_extensions = lambda: [e for e in os.environ.get('PATHEXT', '').split(os.pathsep) if e]

@click.command(help='Search PATH')
@click.argument('pattern')
def which(pattern):
    path_dirs = os.environ.get('PATH', '').split(os.pathsep)
    for d in path_dirs:
        for f in glob.glob(os.path.join(d, pattern)):
            click.echo(f)
