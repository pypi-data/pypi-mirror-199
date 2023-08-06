import pathlib
from itertools import product
from typing import Optional

import blurhash
import click
from joblib import Parallel, delayed
from PIL import Image

from . import __version__
from .constants import (
    HEIGHT_HELP_MSG,
    MAX_COMPONENTS,
    MIN_COMPONENTS,
    PUNCH_HELP_MSG,
    SCALE_HELP_MSG,
    VERBOSE_HELP_MSG,
    WIDTH_HELP_MSG,
    XY_SEP,
)


def generate_blurhash_img(
    x_components: int,
    y_components: int,
    verbose: bool,
    width: int,
    height: int,
    punch: int,
    file_path: pathlib.Path,
) -> None:
    img_hash = blurhash.encode(
        file_path,
        x_components=x_components,
        y_components=y_components,
    )

    if verbose:
        click.echo(
            f"BlurHash string ({x_components} {XY_SEP} {y_components}): {img_hash}",
        )

    output_img = blurhash.decode(img_hash, width=width, height=height, punch=punch)
    # click.echo(output_img.mode)

    output_img.save(f"output_{x_components}x{y_components}.png", format="PNG")


# https://click.palletsprojects.com/en/8.1.x/documentation/#documenting-arguments
# https://click.palletsprojects.com/en/8.1.x/api/#click.Path
# https://github.com/pallets/click/issues/405#issuecomment-324987608
# https://click.palletsprojects.com/en/8.1.x/options/
# https://click.palletsprojects.com/en/8.1.x/api/#types
# https://click.palletsprojects.com/en/8.1.x/advanced/#forwarding-unknown-options
# https://click.palletsprojects.com/en/8.1.x/api/#click.Option
# https://click.palletsprojects.com/en/8.1.x/documentation/#help-parameter-customization
# https://click.palletsprojects.com/en/8.1.x/api/#click.help_option
# https://click.palletsprojects.com/en/8.1.x/api/#context
@click.command(context_settings={"max_content_width": 88})
@click.argument(
    "file_path",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        path_type=pathlib.Path,
    ),
)
@click.option("-w", "--width", type=click.INT, help=WIDTH_HELP_MSG)
@click.option("-h", "--height", type=click.INT, help=HEIGHT_HELP_MSG)
@click.option("-s", "--scale", default=1, show_default=True, help=SCALE_HELP_MSG)
@click.option("-p", "--punch", default=1, show_default=True, help=PUNCH_HELP_MSG)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help=VERBOSE_HELP_MSG,
)
@click.version_option(__version__)
def cli(
    file_path: pathlib.Path,
    width: Optional[int],
    height: Optional[int],
    scale: int,
    punch: int,
    verbose: bool,
) -> None:
    """Generate BlurHash images from an existing image."""
    input_img = Image.open(file_path)

    output_width = width if width else input_img.width
    output_height = height if height else input_img.height

    scaled_output_width = output_width * scale
    scaled_output_height = output_height * scale

    # click.echo(os.cpu_count())

    if verbose:
        output_width_to_print = (
            f"{output_width}px"
            if scale == 1
            else f"{scaled_output_width}px ({output_width}px {XY_SEP} {scale})"
        )
        output_height_to_print = (
            f"{output_height}px"
            if scale == 1
            else f"{scaled_output_height}px ({output_height}px {XY_SEP} {scale})"
        )

        click.echo(f"Output width: {output_width_to_print}")
        click.echo(f"Output height: {output_height_to_print}")
        click.echo(f"Scale: {scale}")
        click.echo(f"Punch: {punch}")

    # https://realpython.com/python-timer/#python-timers
    # Rough estimates (using `06_IMG_1974.jpg`):
    # 2284.1630 seconds vs.
    # 499.9434 seconds (joblib via `Parallel(n_jobs=-1)`) vs.
    # 655.4252 seconds (joblib via `Parallel(n_jobs=-1, prefer="threads")`)
    # tic = time.perf_counter()
    # for x, y in product(range(MIN_COMPONENTS, MAX_COMPONENTS + 1), repeat=2):
    #     generate_blurhash_img(
    #         x_components=x,
    #         y_components=y,
    #         verbose=verbose,
    #         width=scaled_output_width,
    #         height=scaled_output_height,
    #         punch=punch,
    #         file_path=file_path,
    #     )
    # https://joblib.readthedocs.io/en/latest/parallel.html#common-usage
    # https://joblib.readthedocs.io/en/latest/generated/joblib.Parallel.html
    # https://joblib.readthedocs.io/en/latest/parallel.html#thread-based-parallelism-vs-process-based-parallelism
    # https://github.com/joblib/joblib/blob/1.2.0/joblib/_store_backends.py#L148
    component_pairs = product(range(MIN_COMPONENTS, MAX_COMPONENTS + 1), repeat=2)
    Parallel(n_jobs=-1)(
        delayed(generate_blurhash_img)(
            x_components=x,
            y_components=y,
            verbose=verbose,
            width=scaled_output_width,
            height=scaled_output_height,
            punch=punch,
            file_path=file_path,
        )
        for x, y in component_pairs
    )
    # toc = time.perf_counter()
    # click.echo(f"{toc - tic:0.4f} seconds")

    click.echo("Done!")
