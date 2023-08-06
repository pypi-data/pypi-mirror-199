
import click
import os
import sys
import PyPDF2
import time
from rich.console import Console
from .functions_pdf import pages_pdf
from .functions_pdf import extract_png_pdf
from .blur import blur
from .stack import stack
from .topng import topng


@click.command(
        help="Converts pdf pages into pngs"
        )
@click.option(
        '-i',
        '--inputfile',
        type=click.Path(),
        default="./main.pdf",
        show_default=True,
        help="Input file name"
        )
@click.option(
        '-o',
        '--outputfile',
        type=click.Path(),
        default="./main.png",
        show_default=True,
        help="Output file name"
        )
@click.option(
        '-d',
        '--dpi',
        default=320,
        type=click.INT,
        show_default=True,
        help="DPI -> density per inch for png"
        )
@click.option(
        '-t',
        '--transparent',
        is_flag=True,
        default=False,
        show_default=True,
        help="Use this flag for transparent png"
        )
@click.option(
        '-r',
        '--ranges',
        nargs=2,
        default=([1, 1]),
        type=click.Tuple([int, int]),
        show_default=True,
        help="Page range to be converted into png"
        )
@click.option(
        '-p',
        '--pages',
        default=False,
        is_flag = True,
        show_default=True,
        help="Shows no of pages in a pdf file"
        )
@click.pass_context
def instagram(ctx, inputfile, outputfile, dpi, transparent, ranges, pages):
    ctx.invoke(topng, inputfile=inputfile, ranges=ranges)
    for i in range(ranges[0], ranges[1]+1):
        ctx.invoke(blur, inputfile=f'main-{i}.png', outputfile=f'main-{i}b.png', opacity=0.35, radius=2)
