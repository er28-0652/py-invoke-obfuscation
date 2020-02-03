import click
from pathlib import Path

from invoke_obfuscation.encoded_ascii_command import EncodedAsciiCommand


@click.command(help='Encode PowerShell script.')
@click.option('-f', '--file', 'file_', type=click.Path(exists=True), help='')
def encode(file_):
    if file_ is None:
        target_ps_code = click.get_text_stream('stdin').read().strip()
    else:
        target_ps_code = Path(file_).read_text()
    click.echo(EncodedAsciiCommand.invoke(target_ps_code))


def main():
    encode()

if __name__ == '__main__':
    main()