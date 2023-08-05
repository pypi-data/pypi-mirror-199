
import click
import os
from PIL import Image, ImageFilter


@click.command(
        help="Adds background to any transparent image"
        )
@click.option(
        '-i', 
        '--inputimage', 
        type=click.Path(),
        default="./main.png",
        show_default=True,
        help="Front Image"
        )
@click.option(
        '-o', 
        '--outputimage', 
        type=click.Path(),
        default="./main_resized.png",
        show_default=True,
        help="Resized output image"
        )
@click.option(
        '-r',
        '--radius',
        type=click.INT,
        default=2,
        show_default=True,
        help='Radius of GaussianBlur'
        )
def blur(inputimage, outputimage, radius):
    inputimage = Image.open(inputimage)
    outputimage = inputimage.filter(ImageFilter.GaussianBlur(radius))
    outputimage.save(outputimage, format="png")

    click.echo(f'{inputimage} is blured to radius {radius} as {outputimage}.')








