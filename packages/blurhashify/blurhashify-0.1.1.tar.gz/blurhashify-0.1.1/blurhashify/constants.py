# https://note.nkmk.me/en/python-long-string/
# https://beta.ruff.rs/docs/configuration/#command-line-interface

PUNCH_HELP_MSG: str = (
    "The punch of output images. "
    "This design option adjusts the contrast in output images. "
    "Smaller values make the effect more subtle, while larger values make it stronger."
)
VERBOSE_HELP_MSG: str = "Enable verbose logging."

# https://github.com/vega/vega-embed
SCALE_HELP_MSG: str = (
    "The number to multiply the width and height of the output images by."
)

# https://github.com/pallets/click/blob/8.1.3/src/click/termui.py#L58
# https://github.com/pallets/click/blob/8.1.3/src/click/core.py#L2776
# https://github.com/pallets/click/blob/8.1.3/src/click/core.py#L2792
WIDTH_HELP_MSG: str = (
    "The width of the output images (in px).  [default: input image width]"
)
HEIGHT_HELP_MSG: str = (
    "The height of the output images (in px).  [default: input image height]"
)

MIN_COMPONENTS: int = 1
MAX_COMPONENTS: int = 9

XY_SEP: str = "×"  # noqa: RUF001
