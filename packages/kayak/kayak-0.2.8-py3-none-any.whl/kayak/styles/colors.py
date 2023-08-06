from textual.design import ColorSystem

ERROR = "#ba3c5b"
GREEN = "#4EBF71"
PRIMARY = "#ff5f00"
SECONDARY = "#0087ff"

DESIGN = {
    "dark": ColorSystem(
        primary=PRIMARY,
        secondary=SECONDARY,
        error=ERROR,
        dark=True,
    ),
    "light": ColorSystem(
        primary=PRIMARY,
        secondary=SECONDARY,
        error=ERROR,
        dark=False,
    ),
}
