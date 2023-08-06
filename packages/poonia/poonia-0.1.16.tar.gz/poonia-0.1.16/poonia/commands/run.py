import click
import subprocess, locale, sys, os, signal
import multiprocessing
from contextlib import suppress

def get_output(cmd, stdin_bytes=b'', timeout=None, id=None):
    p = None
    def h(signum, frame):
        with suppress(Exception): os.kill(p.pid, signal.SIGKILL)
        with suppress(Exception): os.kill(os.getpid(), signal.SIGKILL)
    signal.signal(signal.SIGINT, h)
    signal.signal(signal.SIGTERM, h)
    cmd = list(c.encode(locale.getpreferredencoding()) for c in cmd)
    n = 0
    while True:
        try:
            n += 1
            p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
            child_pid = p.pid
            stdout, stderr = p.communicate(stdin_bytes, timeout=timeout)
            return id, p.returncode, stdout, stderr
        except subprocess.TimeoutExpired as err:
            p.kill()
            click.secho('[%s.%s] %s' % (id, n, err), err=True, fg='red')

def decode_bytes(s):
    with suppress(Exception): s = s.decode('utf-8', 'ignore')
    return str(s)

def exec(args):
    command, timeout, id = args
    escape_spaces = lambda cmd: " ".join(("\'%s\'" % c if " " in c else c) for c in cmd)
    click.secho('[%s] %s ' % (id, escape_spaces(command)), fg='yellow', underline=True, bold=True, err=True)
    id, status, stdout_bytes, stderr_bytes = get_output(command, timeout=timeout, id=id)
    stdout = decode_bytes(stdout_bytes).strip() if stdout_bytes else ''
    stderr = decode_bytes(stderr_bytes).strip() if stderr_bytes else ''
    return id, status, stdout, stderr

pool = None

@click.command(help='Execute command')
@click.option('--threads', '-j', help='thread count', type=int, default=1)
@click.option('--timeout', '-t', help='timeout in seconds', type=int, default=None)
@click.option('--iterations', '-i', help='number of runs', type=int, default=1)
@click.argument('command', type=str, nargs=-1)
def run(command, threads, timeout, iterations):
    if not command:
        click.secho('missing command', err=True, fg='red')
        sys.exit(1)
    global pool
    finished = 0
    tasks = list((command, timeout, i,) for i in range(iterations + threads - 1))
    pool = multiprocessing.Pool(threads)
    pool.daemon = True
    results = pool.imap_unordered(exec, tasks)
    for id, status, stdout, stderr in results:
        click.secho('[%s] status %s' % (id, status) if status else '[%s] success' % id, fg='black', bg='white', err=True, bold=True)
        if stderr: click.secho(stderr, err=True, fg='red')
        if stdout: click.echo(stdout)
        finished += 1
        if finished == iterations:
            sys.exit()

