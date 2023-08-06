import click



@click.group()
def main():
    pass

from .commands.encoding import encoding
main.add_command(encoding)
from .commands.pairdel import pairdel
main.add_command(pairdel)
from .commands.pairmatch import pairmatch
main.add_command(pairmatch)
from .commands.run import run
main.add_command(run)
from .commands.sdel import sdel
main.add_command(sdel)
from .commands.which import which
main.add_command(which)
from .commands.pn import pn
main.add_command(pn)
from .commands.flatten import flatten
main.add_command(flatten)
from .commands.rename import rename
main.add_command(rename)
from .commands.duration import duration
main.add_command(duration)
from .commands.ffbook import ffbook
main.add_command(ffbook)
from .commands.ffsel import ffsel
main.add_command(ffsel)
from .commands.foldertag import foldertag
main.add_command(foldertag)
from .commands.moveup import moveup
main.add_command(moveup)
from .commands.booksplit import booksplit
main.add_command(booksplit)
from .commands.bookmerge import bookmerge
main.add_command(bookmerge)
from .commands.processfile import processfile
main.add_command(processfile)
from .commands.tpl import tpl
main.add_command(tpl)

if __name__ == '__main__':
    main()
