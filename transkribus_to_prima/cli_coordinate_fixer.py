from click import command, argument
from lxml import etree as ET

from .convert import TranskribusToPrima, NS

@command()
@argument('infile')
@argument('outfile')
def cli(infile, outfile):
    """
    Due to how PAGE-XML interprets pixels (the center of the pixel, not its
    bottom-right corner), max height is imageHeight - 1, max width is imageWidth -1

    This CLI clips all Coords accordinly.
    """
    tree = ET.parse(infile)
    el_page = tree.xpath("//*[local-name()='Page']")[0]
    imageWidth = int(el_page.get('imageWidth'))
    imageHeight = int(el_page.get('imageHeight'))
    for el_coord in tree.xpath('//*[local-name()="Coords"]'):
        new_coords = []
        for coord_pair in el_coord.get('points').split(' '):
            x, y = [int(x) for x in coord_pair.split(',')]
            x = min(x, imageWidth - 1)
            y = min(y, imageHeight - 1)
            new_coords.append(f'{x},{y}')
        el_coord.set('points', ' '.join(new_coords))
    tree.write(outfile, encoding='utf-8')
    # with open(outfile, 'w', encoding='utf-8') as f:
        # f.write(ET.tostring(tree).decode('utf-8'))
