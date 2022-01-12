from pkg_resources import resource_filename
from click import command, Choice, File, argument, option
from lxml import etree as ET

from .convert import TranskribusToPrima, NS

CONVERTERS = [func[8:] for func in dir(TranskribusToPrima)
              if callable(getattr(TranskribusToPrima, func)) and func.startswith('convert_')]
CONVERTERDOCS = [func + ': ' + getattr(TranskribusToPrima, 'convert_' + func).__doc__ for func in CONVERTERS]
CONVERTERS.append('namespace')
CONVERTERDOCS.append('namespace: Also convert PAGE namespace version from 2013 to 2019.')


@command(context_settings={'help_option_names': ['-h', '--help']})
@option('-f', '--converters', help="Conversions to apply. Repeatable [default: all].\n\n" + "\n\n".join(CONVERTERDOCS),
        default=CONVERTERS, type=Choice(CONVERTERS), multiple=True)
@option('-I', '--prefer-imgurl', help="use TranskribusMetadata/@imgUrl for @imageFilename if available", is_flag=True)
@option('-V', '--validate', help="Validate output against schema.", is_flag=True)
@argument('input-file', type=File('r'), nargs=1)
@argument('output-file', default='-', type=File('w'), nargs=1)
def cli(converters, prefer_imgurl, validate, input_file, output_file):
    """
    Transform (Transkribus PAGE) INPUT_FILE to (PRImA PAGE) OUTPUT_FILE under the chosen converters.
    """
    converter = TranskribusToPrima(ET.parse(input_file), prefer_imgurl)
    for convert in [f for f in converters if f != 'namespace']:
        getattr(converter, f'convert_{convert}')()
    as_str = converter.tostring()
    if 'namespace' in converters:
        as_str = as_str.replace(NS['p2013'], NS['p2019'])
    if validate:
        if 'namespace' not in converters and converter.tree.getroot().tag == "{%s}PcGts" % NS['p2013']:
            schema = resource_filename(__name__, 'page2013.xsd')
        else:
            schema = resource_filename(__name__, 'page2019.xsd')
        schema = ET.parse(schema)
        schema = ET.XMLSchema(schema)
        #schema.assertValid(converter.tree) # may need namespace converter
        schema.assertValid(ET.fromstring(as_str.encode('utf-8')))
    output_file.write(as_str)

if __name__ == "__main__":
    cli() # pylint: disable=no-value-for-parameter
