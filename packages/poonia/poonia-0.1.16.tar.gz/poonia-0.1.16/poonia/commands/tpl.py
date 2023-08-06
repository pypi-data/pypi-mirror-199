import click
import os, re, locale, subprocess, sys

def include(path):
    text = open(path, encoding='utf-8').read()
    return text

def exec_cmd(command, wd=None):
    if isinstance(command, str):
        command = command.split(u' ')
    try:
        command = list(c.encode(locale.getpreferredencoding()) for c in command)
        r = subprocess.check_output(command, stderr=subprocess.STDOUT, cwd=wd)
        return r.decode('utf-8').strip()
    except Exception as e:
        return str(e)

def find_file(directory, pattern):
    files = list(f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)))
    for f in files:
        if re.findall(pattern, f):
            return os.path.join(directory, f)
    click.echo('Not found file matching pattern ', nl=False)
    click.secho(pattern, fg='yellow', nl=False)
    click.echo(' in directory ', nl=False)
    click.secho(directory, fg='yellow')
    click.echo('Folder contains following files:')
    for f in files:
        click.secho(f, fg='yellow')
    sys.exit(1)


func_dict = {
    "include": include,
    "exec": exec_cmd,
    "find_file": find_file,
}

def _re_matches(pattern, text):
    out = []
    for m in re.finditer(pattern, text):
        out.append((m.start(), m.end()),)
    return out

def between(text, start_regex, end_regex):
    for start in _re_matches(start_regex, text):
        for end in _re_matches(end_regex, text):
            if start[1] < end[0]:
                return text[start[1]:end[0]].strip()
    return ''

def indent(text, n):
    lines = [n*' '+x.strip() for x in text.splitlines()]
    return '\n'.join(lines).strip()


filters_dict = {
    "between": between,
    "indent": indent,
}

@click.command(help='Render jinja2 template')
@click.argument('template_path', nargs=1, type=click.Path(exists=True, dir_okay=False))
def tpl(template_path):
    try:
        from jinja2 import Environment, FileSystemLoader
    except ModuleNotFoundError:
        click.secho('error: install jinja2 package before using this command', fg='red')
        sys.exit(1)
    path, file = os.path.split(template_path)
    env = Environment(loader=FileSystemLoader(path))
    env.filters.update(filters_dict)
    jinja_template = env.get_template(file)
    jinja_template.globals.update(func_dict)
    template_string = jinja_template.render()
    click.echo(template_string)


if __name__ == '__main__':
    tpl()