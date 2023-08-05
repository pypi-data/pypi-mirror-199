import click
import subprocess

@click.command(help='Process file with a command')
@click.argument('command', nargs=1, required=True)
@click.argument('files', type=click.Path(exists=True, dir_okay=False), nargs=-1)
def processfile(command, files):
    for file in files:
        click.secho("Start processing '%s'" % file, fg='yellow', err=True)
        with open(file, 'r+b') as f:
            content = f.read()
            output = subprocess.check_output(command.split(' '), stderr=subprocess.STDOUT, input=content)
            f.seek(0)
            f.write(output)
            f.truncate()
        click.secho("File '%s' saved succesfully" % file, fg='green', err=True)