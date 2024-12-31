from pathlib import Path
from typing import Iterable, Sequence

from PIL.Image import Image
from pypdf import PdfReader

from .constants import (
    POCKETMOD_COLUMNS,
    POCKETMOD_OFFSET,
    POCKETMOD_PAGES_SEQ,
    POCKETMOD_PDF_PAGES,
    POCKETMOD_ROWS,
)
from .utils import print


def parse_images(
    filename: Path | str,
    pages: Sequence[int] = POCKETMOD_PDF_PAGES,
) -> Iterable[Image]:
    """Parse images from PDF file."""
    reader = PdfReader(filename)
    for page in pages:
        for img_object in reader.pages[page].images:
            yield img_object.image


def save_images(images: Iterable[Image], prefix: str = "") -> None:
    """Save images to filesystem."""
    for i, img in enumerate(images):
        filename = f"{prefix}{i}.jpg"
        print(filename)
        img.save(filename)


def split(
    images: Iterable[Image],
    offset: tuple[float, float, float, float] = POCKETMOD_OFFSET,
    rows: int = POCKETMOD_ROWS,
    cols: int = POCKETMOD_COLUMNS,
) -> Iterable[Image]:
    """Split images by given grid and offset."""
    for img in images:
        xsize, ysize = img.size
        offtop, offright, offbottom, offleft = offset
        img = img.crop((offleft, offtop, xsize - offright, ysize - offbottom))

        xsize, ysize = img.size
        for j in range(rows):
            for i in range(cols):
                page = img.crop(
                    (
                        xsize / cols * i,
                        ysize / rows * j,
                        xsize / cols * (i + 1),
                        ysize / rows * (j + 1),
                    )
                )
                yield page


def reorder(
    pages: Iterable[Image],
    order: Sequence[int] = POCKETMOD_PAGES_SEQ,
) -> list[Image]:
    """Reorder image sequence."""
    pages = list(pages)
    output = []
    for n in order:
        output.append(pages[n])
    return output


# canvas = Canvas("output.pdf", pagesize=A4)
# reader = PdfReader(sys.argv[1])
#
# pages = (4, 5, 6, 7, 0, 1, 2, 3)


def merge(img1: Image, img2: Image) -> Image:
    """Merge two images side by side."""
    width = img1.size[0] + img2.size[0]
    height = max(img1.size[1], img2.size[1])
    img = Image.new("RGB", (width, height))

    img.paste(img1)
    img.paste(img2, (img1.size[0], 0))

    return img


def booklet(images: list[Image]) -> list[Image]:
    """Create image pairs in order to form a foldable booklet."""
    assert len(images) % 4 == 0, "Number of pages has to be divisible by 4"
    booklet = []
    while images:
        booklet.append(merge(images.pop(), images.pop(0)))
        booklet.append(merge(images.pop(0), images.pop()))
    return booklet


def booklet_pdf(images: list[Image]) -> None:
    pass


# page = reader.pages[0]
# pages = []
#
#
# images = []
#
# for count, img_object in enumerate(
#     list(reversed(reader.pages[0].images))  #  + list(reversed(reader.pages[1].images))
# ):
#     xsize, ysize = img_object.image.size
#     # offset left 34 top 47 right 37 bottom 0
#     img = img_object.image.crop((34, 47, xsize - 37, ysize - 37))
#
#     xsize, ysize = img.size
#     for i in range(4):
#         page = img.crop((xsize / 4 * i, 0, xsize / 4 * (i + 1), ysize))
#         images.append(page)
#
#
# images = reorder(images, [3, 4, 5, 6, 7, 0, 1, 2])
#
#
# for i, img in enumerate(images):
#     img.save(f"{i}.jpg")
#
#
# book = booklet(images)
#
# xoffset = (A4[0] - 2 * 63 * mm) / 2
# yoffset = (A4[1] - (2 * 88 + 10) * mm) / 2
#
# canvas.drawInlineImage(
#     book[0], xoffset, yoffset + 88 * mm + 10, height=88 * mm, width=2 * 63 * mm
# )
# canvas.drawInlineImage(book[2], xoffset, yoffset, height=88 * mm, width=2 * 63 * mm)
# canvas.showPage()
#
# canvas.drawInlineImage(
#     book[1], xoffset, yoffset + 88 * mm + 10, height=88 * mm, width=2 * 63 * mm
# )
# canvas.drawInlineImage(book[3], xoffset, yoffset, height=88 * mm, width=2 * 63 * mm)
#
# canvas.showPage()
#
# canvas.save()
