from pypdf import PdfReader
import sys
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

canvas = Canvas("output.pdf", pagesize=A4)
reader = PdfReader(sys.argv[1])

pages = (4, 5, 6, 7, 0, 1, 2, 3)


def merge(im1: Image.Image, im2: Image.Image) -> Image.Image:
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGB", (w, h))

    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))

    return im


def reorder(pages: list[Image.Image], order: list[int]) -> list[Image.Image]:
    output = []
    for n in order:
        output.append(pages[n])
    return output


def booklet(pages: list[Image.Image]) -> list[Image.Image]:
    assert len(pages) % 4 == 0
    booklet = []
    while pages:
        booklet.append(merge(pages.pop(), pages.pop(0)))
        booklet.append(merge(pages.pop(0), pages.pop()))
    return booklet


page = reader.pages[0]
pages = []


images = []

for count, img_object in enumerate(
    list(reversed(reader.pages[0].images))  #  + list(reversed(reader.pages[1].images))
):
    xsize, ysize = img_object.image.size
    # offset left 34 top 47 right 37 bottom 0
    img = img_object.image.crop((34, 47, xsize - 37, ysize - 37))

    xsize, ysize = img.size
    for i in range(4):
        page = img.crop((xsize / 4 * i, 0, xsize / 4 * (i + 1), ysize))
        images.append(page)


images = reorder(images, [3, 4, 5, 6, 7, 0, 1, 2])


for i, img in enumerate(images):
    img.save(f"{i}.jpg")


book = booklet(images)

xoffset = (A4[0] - 2 * 63 * mm) / 2
yoffset = (A4[1] - (2 * 88 + 10) * mm) / 2

canvas.drawInlineImage(
    book[0], xoffset, yoffset + 88 * mm + 10, height=88 * mm, width=2 * 63 * mm
)
canvas.drawInlineImage(book[2], xoffset, yoffset, height=88 * mm, width=2 * 63 * mm)
canvas.showPage()

canvas.drawInlineImage(
    book[1], xoffset, yoffset + 88 * mm + 10, height=88 * mm, width=2 * 63 * mm
)
canvas.drawInlineImage(book[3], xoffset, yoffset, height=88 * mm, width=2 * 63 * mm)

canvas.showPage()

canvas.save()
