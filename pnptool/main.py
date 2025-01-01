import sys
from pathlib import Path

import cloup
from cloup import Context, HelpFormatter, HelpTheme
from PIL import Image

import pnptool
from pnptool import pocketmod as pm

from .constants import Offset
from .utils import IntTupleType, common_options, status

_CONTEXT = Context.settings(
    help_option_names=("-h", "--help"),
    formatter_settings=HelpFormatter.settings(theme=HelpTheme.dark()),
)


@cloup.group(context_settings=_CONTEXT)
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
    "--pdf-pages",
    type=IntTupleType(),
    default="1",
    help="Comma separated list of PDF page numbers.",
    show_default=True,
)
@cloup.option(
    "--ordering",
    type=IntTupleType(),
    default="8,1,2,3,4,5,6,7",
    help="Comma separated list of pocketmod page numbers. This setting is important to reorder the pocketmod pages. Pocketmod PDF page has following structure: [5,6,7,8 | 4,3,2,1]",
    show_default=True,
)
@cloup.option_group(
    "Offset options",
    cloup.option(
        "--offset-top", type=int, default="0", help="Top offset.", show_default=True
    ),
    cloup.option(
        "--offset-bottom",
        type=int,
        default="0",
        help="Bottom offset.",
        show_default=True,
    ),
    cloup.option(
        "--offset-left", type=int, default="0", help="Left offset.", show_default=True
    ),
    cloup.option(
        "--offset-right", type=int, default="0", help="Right offset.", show_default=True
    ),
)
@common_options
def split(
    input_file: Path,
    pdf_pages: tuple[int, ...],
    ordering: tuple[int, ...],
    offset_top: int,
    offset_bottom: int,
    offset_left: int,
    offset_right: int,
):
    """Split pocketmod to separate images."""
    images = pm.parse_images(input_file, pages=pdf_pages)
    images = pm.split(
        images,
        offset=Offset(
            top=offset_top,
            bottom=offset_bottom,
            left=offset_left,
            right=offset_right,
        ),
    )
    images = pm.reorder(images, order=ordering)
    pm.save_images(images, prefix=f"{input_file.stem}-")


@pocketmod.command()
@cloup.option(
    "-o",
    "--output",
    default="booklet.pdf",
    help="Output PDF filename.",
    show_default=True,
)
@cloup.argument("images", nargs=-1, required=True)
@common_options
def book(output: str, images: tuple[str]) -> None:
    """Create a booklet PDF."""
    if images == ("-",):
        images = tuple(line.rstrip("\n") for line in sys.stdin.readlines())

    with status("Loading images"):
        images = [Image.open(img) for img in images]
    with status("Generating booklet PDF"):
        pm.booklet_pdf(images, file=output)
