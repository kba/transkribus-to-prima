from lxml import etree as ET
from click import command, Choice, argument, option
import sys

NS2013 = 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'
NS2019 = 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15'
NS = {'p2013': NS2013, 'p2019': NS2019}

class TranskribusFixer():
    """
    Translates Transkribus variant of PAGE to standard-conformant PAGE
    """

    def __init__(self, tree):
        self.tree = tree

    def fix_metadata(self):
        el_metadata = self.tree.find('//p2013:TranskribusMetadata', NS)
        if el_metadata is not None:
            el_metadata.getparent().remove(el_metadata)

    def fix_reading_order(self):
        ro = self.tree.find('//p2013:ReadingOrder/p2013:OrderedGroup', NS)
        relations = self.tree.find('//p2013:Relations', NS)
        for relation in relations.findall('p2013:Relation[@type="link"]', NS):
            region_refs = relation.findall('p2013:RegionRef', NS)
            ro_grp = ET.SubElement(ro, 'OrderedGroupIndexed')
            ro_grp.set('id', 'relation_link_' + '-'.join([x.get('regionRef') for x in region_refs]))
            ro_grp.set('index', str(int(ro.findall('p2013:RegionRefIndexed', NS)[-1].get('index')) + 1))
            for idx, region_ref in enumerate(region_refs):
                ro_region_ref = ET.SubElement(ro_grp, 'RegionRefIndexed')
                ro_region_ref.set('regionRef', region_ref.get('regionRef'))
                ro_region_ref.set('index', str(idx))
            relation.getparent().remove(relation)
        if not relations.findall('*'):
            relations.getparent().remove(relations)

    def fix_table(self):
        for el_table in self.tree.findall('//p2013:TableRegion', NS):
            for el_cell in el_table.findall('p2013:TableCell', NS):
                el_table.remove(el_cell)
                el_region = ET.SubElement(el_table, '{%s}TextRegion' % NS2013)
                el_region.insert(0, el_cell.find('p2013:Coords', NS))
                el_roles = ET.SubElement(el_region, '{%s}Roles' % NS2013)
                el_tablecellrole = ET.SubElement(el_roles, '{%s}TableCellRole' % NS2013)
                el_tablecellrole.set('rowIndex', el_cell.get('row'))
                el_tablecellrole.set('columnIndex', el_cell.get('col'))
                el_tablecellrole.set('rowSpan', el_cell.get('rowSpan'))
                el_tablecellrole.set('colSpan', el_cell.get('colSpan'))
                for att in ['orientation', 'id']:
                    if att in el_cell.attrib:
                        el_region.set(att, el_cell.get(att))
                for el_textline in el_cell.findall('p2013:TextLine', NS):
                    el_region.append(el_textline)

    def tostring(self):
        return ET.tostring(self.tree, pretty_print=True, encoding='utf-8').decode('utf-8').replace(NS2013, NS2019)

@command()
@option('-f', '--fixes', help="Fixes to apply. Repeatable", type=Choice(['reading_order', 'table', 'metadata']), multiple=True)
@argument('input-file', nargs=1)
@argument('output-file', nargs=1)
def cli(fixes, input_file, output_file):
    """
    Apply the fixes to INPUT_FILE.

    Also converts PAGE2013 to PAGE2019 when writing to OUTPUT_FILE.
    """
    fixer = TranskribusFixer(ET.parse(input_file))
    for fix in fixes:
        getattr(fixer, f'fix_{fix}')()
    with open('/dev/stdout' if output_file == '-' else output_file, 'w') as f:
        f.write(fixer.tostring())

if __name__ == "__main__":
    cli()
