import click
import subprocess, locale
from concurrent.futures import ThreadPoolExecutor

def get_output(cmd, stdin_bytes=b'', timeout=None, id=None):
    cmd = list(c.encode(locale.getpreferredencoding()) for c in cmd)
    while True:
        try:
            p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate(stdin_bytes, timeout=timeout)
            return id, p.returncode, stdout, stderr
        except Exception as err:
            click.secho(f'[{id}] {err}', err=True, fg='red')

def _d(s):
    try:
        s = s.decode('utf-8', 'ignore')
    except:
        pass
    return str(s)

def exec(command, timeout, id=0):
    escape_spaces = lambda cmd: " ".join((f"\'{c}\'" if " " in c else c) for c in cmd)
    click.secho(f'[{id}] {escape_spaces(command)} ', fg='yellow', underline=True, bold=True, err=True)
    id, status, stdout_bytes, stderr_bytes = get_output(command, timeout=timeout, id=id)
    stdout = _d(stdout_bytes).strip() if stdout_bytes else ''
    stderr = _d(stderr_bytes).strip() if stderr_bytes else ''
    return id, status, stdout, stderr

@click.command(help='Execute command')
@click.option('--threads', '-j', help='thread count', type=int, default=1)
@click.option('--timeout', '-t', help='timeout in seconds', type=int, default=None)
@click.option('--iterations', '-i', help='number of runs', type=int, default=1)
@click.argument('command', type=str, nargs=-1)
def run(command, threads, timeout, iterations):
    p = ThreadPoolExecutor(max_workers=threads)
    def done(x):
        id, status, stdout, stderr = x.result()
        click.secho(f'[{id}] status {status}' if status else f'[{id}] success', fg='black', bg='white', err=True, bold=True)
        if stdout:
            click.echo(stdout)
        if stderr:
            click.secho(stdout, err=True, fg='red')

    for i in range(iterations):
        f = p.submit(exec, command, timeout, i)
        f.add_done_callback(done)
        