import os
import json
import shutil
import sys
import pathlib

import click
from xdg import BaseDirectory
from podman import PodmanClient

from podman.errors import NotFound, APIError

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
DATABASE_DIR = os.path.join(BaseDirectory.xdg_data_home, 'tb/')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'data.json')
DATABASE_PATH_BACKUP = DATABASE_PATH + '.backup'


def toolboxContainerExists(name: str, pc: PodmanClient):
    try:
        pc.containers.get(name)
        return True
    except NotFound:
        return False
    except APIError as e:
        click.echo('Error locating toolbox with name {name} due to:\n{e}')
        return False

def ensure_database():
    if pathlib.Path(DATABASE_PATH).is_file():
        return
    else:
        os.makedirs(DATABASE_DIR, exist_ok=True)
        write_database({}, skip_backup=True)

def get_database():
    with open(DATABASE_PATH, 'rb') as input:
        return json.loads(input.read())

def write_database(database, skip_backup=False):
    if not skip_backup:
        shutil.copy2(DATABASE_PATH, DATABASE_PATH_BACKUP)
    database_str = json.dumps(database)
    with open(DATABASE_PATH, "w") as output:
        output.write(database_str)


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.option('--podman-url', envvar='PODMAN_URL', show_default=True, default=f'unix:///run/user/{os.getuid()}/podman/podman.sock', help='URL to access Podman service')
@click.pass_context
def cli(ctx, podman_url):
    """Shortcut tool for Toolbox (https://containertoolbx.org/) that can associated diretories with a toolbox.
    
    \b
    Features, Feedback, and Bugs: https://github.com/bostrt/tb
    """
    try:
        ctx.ensure_object(dict)
        ensure_database()
        ctx.obj = {"database": get_database()}
    except Exception as e:
        click.echo(f'Error getting database due to:\n{e}')
        sys.exit(1)

    try:
        pc = PodmanClient(base_url=podman_url)
        ctx.obj["podman"] = pc
    except ValueError as e:
        click.echo(f'Error initializing podman client due to:\n{e}')
        sys.exit(1)
    
    if ctx.invoked_subcommand is None:
        _do_enter_toolbox(ctx, '.')

@cli.command('enter', help='Enter a linked toolbox for a directory', )
@click.argument('directory', nargs=1, default='.', type=click.Path(exists=True, file_okay=False))
@click.pass_context
def enter_toolbox_for(ctx, directory):
    _do_enter_toolbox(ctx, directory)

def _do_enter_toolbox(ctx, directory):
    pc = ctx.obj["podman"]
    db = ctx.obj["database"]

    d_path = str(pathlib.Path(directory).resolve())
    if d_path in db:
        container = db[d_path]
        os.system(f'/usr/bin/toolbox enter {container}')
    else:
        click.echo('No linked toolbox found for current directory (try: tb --help)')

@cli.command(help='Link a directory to Toolbox container')
@click.argument('toolbox')
@click.argument('directories', nargs=-1, type=click.Path(exists=True, file_okay=False))
@click.pass_context
def add(ctx, toolbox, directories):
    pc = ctx.obj["podman"]
    db = ctx.obj["database"]

    if len(directories) == 0:
        directories = ('.')  # Default to CWD

    # Ensure toolbox container exists
    if not toolboxContainerExists(toolbox, pc):
        return click.echo(f'Unable to find toolbox named {toolbox}')
    
    changes = False
    for d in directories:
        d_path = pathlib.Path(d).resolve()
        db[str(d_path)] = toolbox
        click.echo(f'Added link: {toolbox} => {d_path}')
        changes = True

    try:
        write_database(db)
    except:
        click.echo('Error writing database')

@cli.command(help='Remove link for directory')
@click.argument('directories', nargs=-1, type=click.Path(exists=True))
@click.pass_context
def rm(ctx, directories):
    pc = ctx.obj["podman"]
    db = ctx.obj["database"]

    if len(directories) == 0:
        directories = ('.')  # Default to CWD

    changes = False
    for d in directories:
        d_path = str(pathlib.Path(d).resolve())
        if d_path in db:
            linked_toolbox = db[d_path]
            del db[d_path]
            click.echo(f'Removed link: {linked_toolbox} => {d_path}')
            changes = True
        else:
            click.echo(f'Skipping due to no link present for {d_path}')

    if not changes:
        return

    try:
        write_database(db)
    except:
        click.echo('Error writing database') 

@cli.command(help='List all toolbox/directory links')
@click.pass_context
def list(ctx):
    pc = ctx.obj["podman"]
    db = ctx.obj["database"]

    for k in iter(db):
        click.echo(f'{db[k]} => {k}')