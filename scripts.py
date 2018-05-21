"""Runable scripts.

TODO: Make these much more usable + entrypoints on pip install.
"""

import click

from encodji.encoders import encode, decode

@click.command()
@click.option('-o', '--outfile', required=False, help="Output file", type=click.File(mode='w'))
@click.option('-i', '--infile', required=False, help="Input file", type=click.File())
@click.option('-t', '--text', required=False)
@click.argument('command', required=True, type=click.Choice(['encode', 'decode']))
def cli(command, text, infile, outfile):
    if not (text or infile):
        raise click.BadParameter("Required one of '-t' or '-i'")

    # Toggle between encode/decode
    if command == 'encode':
        func = encode
    else:
        func = decode
    # Prepare the input
    if infile:
        to_handle = infile.read()
    else:
        to_handle = text
    # Process the data the same way no matter the fn
    processed = func(to_handle)
    # Either write or print the results
    if outfile:
        outfile.write(processed)
    else:
        click.echo(processed)

if __name__ == '__main__':
    cli()
