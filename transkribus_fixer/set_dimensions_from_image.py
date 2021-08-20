from lxml import etree as ET
from click import command, argument
from subprocess import check_output

@command()
@argument('inpage')
@argument('image')
@argument('outpage')
def cli(inpage, image, outpage):
    width, height = check_output(['identify', '-format',  '%w %h', image], encoding='utf-8').split(' ')
    tree = ET.parse(inpage)
    el_page = tree.xpath('*[local-name()="Page"]')[0]
    el_page.set('imageWidth', width)
    el_page.set('imageHeight', height)
    tree.write(outpage, encoding='utf-8')

