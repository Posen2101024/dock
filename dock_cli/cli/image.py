import configparser
import itertools
import click
from dock_cli.utils import callback as cb
from dock_cli.utils import commands as cmd
from dock_cli.utils import helpers as hlp
from dock_cli.utils.schema import ImageConfigOptions as Image, SectionType
from dock_cli.utils.utils import update_config, set_config_option, print_image_config

@click.group(name='image', cls=hlp.OrderedGroup)
@click.pass_obj
def cli(obj):
    """Manage images

    This is a command line interface for manage images
    """
    obj.helper = hlp.ImageHelper(obj.config, obj.config_dir, obj.command)

@cli.command(name='list',
             help='List all images')
@click.pass_obj
def image_list(obj):
    for section in obj.helper.get_images():
        click.echo(section)

@cli.command(name='diff',
             help='List all images that have been changed between commits')
@click.pass_obj
@click.argument('commit1', required=False, type=str, default='HEAD')
@click.argument('commit2', required=False, type=str)
def image_diff(obj, commit1, commit2):
    for section in obj.helper.get_updated_images(commit1, commit2):
        click.echo(section)

@cli.command(name='show',
             help='Show detailed information about a specific image')
@click.pass_obj
@click.argument('section', required=True, type=str, callback=cb.validate_section)
@click.argument('tag', required=False, type=str, default='latest')
def image_show(obj, section, tag):
    click.echo(obj.helper.get_image(section, tag))

@cli.command(name='build',
             help='Build images')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True, type=str, callback=cb.validate_section)
@click.option('--tag', 'tags', multiple=True, type=str, default=['latest'], show_default=True,
              help='Specify one or multiple tags for the image')
def image_build(obj, sections, tags):
    for section in sections:
        cmd.run([obj.command.docker, 'build', obj.helper.get_section_path(section),
                 '--file', obj.helper.get_section_file(section),
                 *itertools.chain(*[('--tag', obj.helper.get_image(section, tag)) for tag in tags])])

@cli.command(name='push',
             help='Push images')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True, type=str, callback=cb.validate_section)
@click.option('--tag', 'tags', multiple=True, type=str, default=['latest'], show_default=True,
              help='Specify one or multiple tags for the image')
def image_push(obj, sections, tags):
    for section in sections:
        obj.helper.validate_section(section)
        for tag in tags:
            cmd.run([obj.command.docker, 'push', obj.helper.get_image(section, tag)])

@cli.command(name='clean',
             help='Clean images')
@click.pass_obj
@click.argument('sections', nargs=-1, required=True, type=str, callback=cb.validate_section)
@click.option('--tag', 'tags', multiple=True, type=str, default=['latest'], show_default=True,
              help='Specify one or multiple tags for the image')
def image_clean(obj, sections, tags):
    for section in sections:
        obj.helper.validate_section(section)
        for tag in tags:
            cmd.run([obj.command.docker, 'rmi', '--force', obj.helper.get_image(section, tag)])

@cli.group(name='config', invoke_without_command=True, cls=hlp.OrderedGroup)
@click.pass_context
def config_cli(ctx):
    """Manage images' configuration

    This is a command line interface for manage images' configuration
    """
    if ctx.invoked_subcommand is None:
        for section in ctx.obj.helper.get_images():
            print_image_config(section)
        ctx.call_on_close(update_config)

@config_cli.command(name='init',
                    help='Initialize image default settings in the configuration')
@click.pass_context
@click.option('--registry', required=False, type=str, default='namespace',
              help='Default registry for all images.')
def config_init(ctx, registry):
    set_config_option(configparser.DEFAULTSECT, Image.REGISTRY, registry)
    for section in ctx.obj.helper.get_images():
        print_image_config(section)
    ctx.call_on_close(update_config)

@config_cli.command(name='add',
                    help='Add or update an image section in the configuration')
@click.pass_context
@click.argument('section', required=True, type=click.Path(exists=True, file_okay=False),
                callback=cb.transform_to_section)
@click.option('--file', required=False, type=str, default='Dockerfile', show_default=True,
              help='Name of the Dockerfile for this section.')
@click.option('--name', required=False, type=str,
              help='Name of the image for this section.')
@click.option('--depends-on', required=False, multiple=True,
              type=click.Path(exists=True, file_okay=False),
              callback=cb.multiline_sections,
              help='List of sections or paths that this section depends on.')
def config_add(ctx, section, file, name, depends_on):
    # pylint: disable=too-many-arguments
    if ctx.obj.config.has_section(section) is False:
        ctx.obj.config.add_section(section)
    set_config_option(section, Image.FILE, file)
    set_config_option(section, Image.NAME, name)
    set_config_option(section, Image.DEPENDS_ON, depends_on)
    set_config_option(section, Image.TYPE, SectionType.IMAGE)
    ctx.obj.helper.validate_section(section)
    print_image_config(section)
    ctx.call_on_close(update_config)
