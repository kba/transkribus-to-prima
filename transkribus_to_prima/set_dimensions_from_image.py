from lxml import etree as ET
from click import command, argument, option, Path
from PIL import Image


@command(context_settings={'help_option_names': ['-h', '--help']})
@option('-F', '--replace-filename', help="also update the @imageFilename", is_flag=True)
@argument('inpage', type=Path(exists=True, dir_okay=False, allow_dash=True))
@argument('image', type=Path(exists=True, dir_okay=False))
@argument('outpage', type=Path(exists=False, dir_okay=False, allow_dash=True))
def cli(replace_filename, inpage, image, outpage):
    """
    Reads a PAGE-XML file INPAGE, and respective image file IMAGE,
    updates the Page/@imageWidth and @imageHeight from the image,
    then writes the resulting PAGE-XML file OUTPAGE.
    """
    width, height = Image.open(image).size
    tree = ET.parse(inpage)
    el_page = tree.xpath('*[local-name()="Page"]')[0]
    el_page.set('imageWidth', str(width))
    el_page.set('imageHeight', str(height))
    if replace_filename:
        el_page.set('imageFilename', image)
    tree.write(outpage, encoding='utf-8')

