from click import command, Choice, File, argument, option
from lxml import etree as ET

from .fixer import TranskribusFixer, NS

@command(context_settings={'help_option_names': ['-h', '--help']})
@option('-f', '--fixes', help="Fixes to apply. Repeatable [default: all].",
        default=['reading_order', 'table', 'metadata', 'namespace'],
        type=Choice(['reading_order', 'table', 'metadata', 'namespace']), multiple=True)
@argument('input-file', type=File('r'), nargs=1)
@argument('output-file', default='-', type=File('w'), nargs=1)
def cli(fixes, input_file, output_file):
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
    output_file.write(as_str)

if __name__ == "__main__":
    cli()
