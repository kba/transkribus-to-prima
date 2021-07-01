from click import command, Choice, argument, option
from lxml import etree as ET

from .fixer import TranskribusFixer

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
