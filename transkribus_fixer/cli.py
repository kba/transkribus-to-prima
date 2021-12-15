from pkg_resources import resource_filename
from click import command, Choice, File, argument, option
from lxml import etree as ET

from .fixer import TranskribusFixer, NS

FIXERS = [func[4:] for func in dir(TranskribusFixer)
          if callable(getattr(TranskribusFixer, func)) and func.startswith('fix_')]
FIXERDOCS = [func + ': ' + getattr(TranskribusFixer, 'fix_' + func).__doc__ for func in FIXERS]
FIXERS.append('namespace')


@command(context_settings={'help_option_names': ['-h', '--help']})
@option('-f', '--fixes', help="Fixes to apply. Repeatable [default: all].\n\n" + "\n\n".join(FIXERDOCS),
        default=FIXERS, type=Choice(FIXERS), multiple=True)
@option('-V', '--validate', help="Validate output against schema.", is_flag=True)
@argument('input-file', type=File('r'), nargs=1)
@argument('output-file', default='-', type=File('w'), nargs=1)
def cli(fixes, validate, input_file, output_file):
    """
    Transform (Transkribus PAGE) INPUT_FILE to (PRImA PAGE) OUTPUT_FILE under the chosen fixes.

    Also convert PAGE namespace version from 2013 to 2019.
    """
    fixer = TranskribusFixer(ET.parse(input_file))
    for fix in [f for f in fixes if f != 'namespace']:
        getattr(fixer, f'fix_{fix}')()
    as_str = fixer.tostring()
    if 'namespace' in fixes:
        as_str = as_str.replace(NS['p2013'], NS['p2019'])
    if validate:
        if 'namespace' not in fixes and fixer.tree.getroot().tag == "{%s}PcGts" % NS['p2013']:
            schema = resource_filename(__name__, 'page2013.xsd')
        else:
            schema = resource_filename(__name__, 'page2019.xsd')
        schema = ET.parse(schema)
        schema = ET.XMLSchema(schema)
        #schema.assertValid(fixer.tree) # may need namespace fixer
        schema.assertValid(ET.fromstring(as_str.encode('utf-8')))
    output_file.write(as_str)

if __name__ == "__main__":
    cli()
