from click import command, argument, Path
from lxml import etree as ET

@command(context_settings={'help_option_names': ['-h', '--help']})
@argument('inpage', type=Path(exists=True, dir_okay=False, allow_dash=True))
@argument('outpage', type=Path(exists=False, dir_okay=False, allow_dash=True))
def cli(inpage, outpage):
    """
    Reads a PAGE-XML file INPAGE, iterates over all Coords/@points,
    clipping its values to the allowable range (from zero to image size),
    then writes the resulting PAGE-XML file OUTPAGE.

    Due to how PAGE-XML interprets pixels (the center of the pixel, not its
    bottom-right corner), max height is imageHeight - 1, max width is imageWidth -1
    """
    tree = ET.parse(inpage)
    el_page = tree.xpath("//*[local-name()='Page']")[0]
    imageWidth = int(el_page.get('imageWidth'))
    imageHeight = int(el_page.get('imageHeight'))
    for el_coord in tree.xpath('//*[./@points]'):
        new_coords = []
        for coord_pair in el_coord.get('points').split(' '):
            x, y = [int(x) for x in coord_pair.split(',')]
            x = max(0, min(x, imageWidth - 1))
            y = max(0, min(y, imageHeight - 1))
            new_coords.append(f'{x},{y}')
        el_coord.set('points', ' '.join(new_coords))
    tree.write(outpage, encoding='utf-8')
    # with open(outpage, 'w', encoding='utf-8') as f:
        # f.write(ET.tostring(tree).decode('utf-8'))
