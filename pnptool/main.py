from pathlib import Path

import cloup
from cloup import Context, HelpFormatter, HelpTheme

import pnptool
from pnptool import pocketmod as pm

from .utils import common_options, IntTupleType

SETTINGS = Context.settings(
    help_option_names=("-h", "--help"),
    formatter_settings=HelpFormatter.settings(theme=HelpTheme.dark()),
)


@cloup.group(context_settings=SETTINGS)
@cloup.version_option(pnptool.__version__, "-V", "--version")
@cloup.pass_context
def cli(ctx: Context):
    """Print and play toolbox."""
    ctx.ensure_object(dict)


@cli.group()
def pocketmod():
    """PocketMod format manipulation."""


@pocketmod.command()
@cloup.option(
    "-i",
    "--input-file",
    required=True,
    type=cloup.file_path(exists=True),
    help="Input PDF filename.",
)
@cloup.option(
    "--pages",
    type=IntTupleType(),
    default="1",
    help="Comma separated list of page numbers.",
    show_default=True,
)
@common_options
def split(input_file: Path, pages: tuple[int, ...]):
    """Split pocketmod to separate images."""
    images = pm.parse_images(input_file, pages=pages)
    images = pm.split(images)
    # pm.save_images(pm.reorder(images), prefix=f"{input_file.stem}-")
    pm.save_images(images, prefix=f"{input_file.stem}-")


@pocketmod.command()
@common_options
def book():
    """Split pocketmod and create a booklet PDF."""
    ctx = cloup.get_current_context()
    print(ctx.obj["verbosity"])
