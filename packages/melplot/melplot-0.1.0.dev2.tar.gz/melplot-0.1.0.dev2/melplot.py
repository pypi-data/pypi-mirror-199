"""
Melodeon layout diagrams
"""
from __future__ import annotations

from typing import Optional

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

try:
    import typer
except ImportError:
    have_typer = False
else:
    have_typer = True

__version__ = "0.1.0.dev2"

PI = np.pi
DEBUG = False

_TRAN_ABC_TO_UNICODE = str.maketrans("#b=0123456789-", "♯♭♮₀₁₂₃₄₅₆₇₈₉−")

_DEFAULT_BUTTON_TEXT_KWARGS = dict(
    va="center", ha="center", fontfamily="sans-serif", color="darkgoldenrod", size=12
)

ButtonNotes_T = tuple[str, str]
Row_T = list[Optional[ButtonNotes_T]]


def plot_button(
    pos: tuple[float, float],
    notes: ButtonNotes_T,
    *,
    ax: mpl.axes.Axes,
    radius: float = 0.02,
    rotation: float = -90,
    text_kwargs: dict | None = None,
) -> None:
    """
    Parameters
    ----------
    rotation
        Rotation of the push/pull separation line (degrees). Positive is anti-clockwise.
    """
    xc, yc = pos
    r = radius
    note_push, note_pull = (note.translate(_TRAN_ABC_TO_UNICODE) for note in notes)
    if text_kwargs is None:
        text_kwargs = {}
    text_kwargs = {**_DEFAULT_BUTTON_TEXT_KWARGS, **text_kwargs}

    # Button edge (circle)
    p = mpl.patches.Circle(pos, radius=radius, facecolor="none", edgecolor="blue")
    ax.add_patch(p)

    # Label push and pull notes
    t0 = PI / 2
    rot = np.deg2rad(rotation)
    ax.plot(
        [xc + r * np.cos(t0 + rot), xc + r * np.cos(t0 - rot)],
        [yc + r * np.sin(t0 + rot), yc - r * np.sin(t0 - rot)],
        "-",
        color="forestgreen",
        solid_capstyle="butt",
        zorder=0,
    )
    r2 = r / 2
    ax.text(
        xc + r2 * np.cos(PI + rot),
        yc + r2 * np.sin(PI + rot),
        note_push.rstrip("*"),
        **text_kwargs,
        weight="bold" if note_push.endswith("*") else None,
    )
    ax.text(xc + r2 * np.cos(rot), yc + r2 * np.sin(rot), note_pull, **text_kwargs)


# TODO: look into PolyCollection instead individual patches for speed?


_EXAMPLES_TO_KEY: dict[str, tuple[str, ...]] = {
    # Standard 21-key D/G
    """\
D+|A+ D|A G+|D+ G|D
B+|E- B|E C+|C+ C|C
---
F5|Eb5 D4|F#4 G4|A B|C D|E G5|F# B|A D|C G6|E B|F#
G#4|Bb4 A3|C#4 D4*|E F#|G A|B D5*|C# F#|E A|G D6*|B F#|C# A|E
""": (
        "D/G",
        "DG",
        "DG21",
    ),
    # Elye's new layout
    """\
Eb+|F#- Eb|F# D+|A+ D|A G+|D+ G|D
Bb+|F+  Bb|F  B-|E- B|E C+|C+ C|C
---
Bb3|F3 Eb|D F|F Bb|G# C|D Eb|Eb E*|F Bb|G# Eb|D E*|F
G3|A B|C4 E4*|F#4 G4|A B|C D|E G5|F# B|A D|C G6|E B|F#
D3|E F#|B A3|C#4 D4|E F#|G A|B D5|C# F#|E A|G D6|B F#|C# A|E
""": (
        "Elye",
        "Elye new",
    ),
    # B/C layout with McComiskey bass
    """\
G+|D+ G|D C+|G+ C|G
E+|A+ E|A D+|F+ D|F
---
E3|A3 G3|B3 C4|D4 E4|F4 G4|A4 C5|B5 E5|D5 G5|F5 C6|A5 E6|B5
D#3|G#3 F#3|A#3 B3|C#4 D#4|E4 F#4|G#4 B4|A#4 D#5|C#5 F#5|E5 B5|G#5 D#6|A#5 F#6|C#6
""": (
        "B/C",
        "BC",
    ),
    # Paul Young 21 + 5 D/G
    """\
Eb+|F#- Eb|F# D+|A+ D|A G+|D+ G|D
Bb+|F+ Bb|F B-|E- B|E C+|C+ C|C
---
x x F4|F4 Bb4|G#4 Eb5|D5 F5|F5 Bb5|G#5
Eb4|D4 B3|C4 D4|F#4 G4|A4 B4|C5 D5|E5 G5|F#5 B5|A5 D6|C6 G6|E6
Bb3|B3 G3|A3 A3|C#4 D4|E4 F#4|G4 A4|B4 D5|C#5 F#5|E5 A5|G5 D6|B6 F#6|C#6
""": (
        "Paul Young DG",
        "Paul Young D/G",
        "Paul Young DG21.5",
    ),
    #
}
"""Mapping of layout spec to accepted name keys."""

EXAMPLES: dict[str, str] = {
    name: layout_spec for layout_spec, names in _EXAMPLES_TO_KEY.items() for name in names
}
"""Mapping of name/ID to layout spec string."""

EXAMPLES["DG21 treb"] = "\n".join(EXAMPLES["DG21"].splitlines()[3:])


def split_button(s: str, *, sep: str = "|") -> ButtonNotes_T | None:
    """Split button into two note strings with validation.
    If button has only one note, it will be doubled.
    """
    if s == "x":  # placeholder
        return None

    notes = s.split(sep)
    n = len(notes)
    if n > 2:
        raise ValueError(f"invalid button {s!r}, splitting on {sep!r} found >2 notes")
    elif n == 1:
        print(f"note: doubling detected single note {notes[0]!r}")
        notes.append(notes[0])

    return (notes[0], notes[1])


def read_layout(s: str, *, button_sep: str = "|") -> tuple[list[Row_T], list[Row_T]]:
    bass_rows = []
    treb_rows = []
    bass = True
    for line in s.splitlines():
        if all(c == "-" for c in line.strip()):  # bellows
            bass = False
            continue

        notes = [split_button(button, sep=button_sep) for button in line.split()]
        if bass:
            bass_rows.append(notes)
        else:
            treb_rows.append(notes)

    # Allow for treble-only diagrams
    if bass:
        treb_rows, bass_rows = bass_rows, []

    return treb_rows, bass_rows


def plot(
    treb_rows: list[Row_T],
    bass_rows: list[Row_T],
    *,
    rotation: float = -90,
    figsize: float = 9,
) -> None:
    nmax = max(len(row) for row in treb_rows)

    # Size settings
    figw = figsize
    drel = 0.32  # button padding relative to radius
    r = 1 / (2 * nmax + (nmax + 1) * drel)  # radius, maximizing horiz space
    d = drel * r  # space between
    dx = 2 * r + d  # button center-to-center horiz distance
    n_bellows = 4
    dy_bellows = 0.03
    w_bellows = 0.5
    pad_bellows = 0.03

    # Vertical offset to make angled/offset treble button spacing same as horiz
    # (equilateral triangle arrangement)
    d2 = np.sqrt((2 * r + d) ** 2 - (r + d / 2) ** 2) - 2 * r

    fig, ax = plt.subplots(figsize=(figw, figw), constrained_layout=True)
    # Constrained layout seems to do a better job of eliminating unused margin space

    if not DEBUG:
        ax.set_axis_off()

    # Compute treble row starting positions??
    # TODO: Probably want to be able to specify this in input
    # ns = [len(row) for row in treb_rows]
    x0s = [0, 0.5, 1]  # just set for now (button-size-relative)

    # Treble buttons
    ys = d + r + np.arange(len(treb_rows)) * (2 * r + d2)
    for x0, y, row in zip(x0s, ys, reversed(treb_rows)):
        xs = np.arange(len(row)) * dx + r + d + x0 * dx
        for x, s in zip(xs, row):
            if s is None:
                continue
            plot_button((x, y), s, radius=r, ax=ax, rotation=rotation)

    # Bellows
    ys2 = ys[-1] + r + pad_bellows + np.arange(n_bellows) * dy_bellows
    for y in ys2:
        ax.plot([0.5 - w_bellows / 2, 0.5 + w_bellows / 2], [y, y], "0.1", lw=1)

    if bass_rows:
        # Bass buttons
        ys3 = ys2[-1] + pad_bellows + r + np.arange(len(bass_rows)) * dx
        x0 = 0.5 - (len(bass_rows[-1]) * dx - d) / 2 + r
        # TODO: also support specifying
        for y, row in zip(ys3, reversed(bass_rows)):
            xs = x0 + np.arange(len(row)) * dx
            for x, s in zip(xs, row):
                if s is None:
                    continue
                plot_button((x, y), s, radius=r, ax=ax, rotation=rotation)

        ymax = ys3[-1] + r + d
    else:
        ymax = ys2[-1] + r + d

    # Legend
    mrot = rotation % 360
    q = 35
    if 0 <= mrot <= q or 360 - q <= mrot < 360 or 180 - q <= mrot <= 180 + q:
        legrot = 90
    else:
        legrot = 0
    plot_button(
        (0.5 * dx, ymax - 0.5 * dx),
        ("Push", "Pull"),
        radius=r,
        ax=ax,
        rotation=rotation,
        text_kwargs=dict(rotation=legrot),
    )
    ax.text(d, ymax - dx, "+ : major chord", va="top")
    ax.text(d, ymax - dx - 0.02, "− : minor chord", va="top")

    ax.axis("scaled")
    ax.set(xlim=(0, 1), ylim=(0, ymax))

    if not DEBUG:
        figw_ = fig.get_figwidth()
        assert figw_ == figw
        fig.set_size_inches((figw_, ymax * figw_ * 1.01))


if have_typer:
    app = typer.Typer(add_completion=False)

    def _version_callback(value: bool):
        if value:
            typer.echo(f"melplot {__version__}")
            raise typer.Exit()

    @app.command()
    def cli(
        example: str = typer.Option("DG21", "-e", "--example", help="Example to plot."),
        rotation: float = typer.Option(
            -90, help="Button rotation (degrees). By default, push is directly above pull"
        ),
        figsize: float = typer.Option(
            9,
            help="Size of figure maximum dimension, usually the width.",
        ),
        debug: bool = typer.Option(DEBUG, help="Show ax spines and debug messages."),
        version: bool = typer.Option(
            False,
            "--version/",
            help="Print version and exit.",
            callback=_version_callback,
            is_eager=True,
        ),
    ):
        """Plot Melodeon diagram."""
        global DEBUG
        DEBUG = debug

        try:
            layout_spec = EXAMPLES[example]
        except KeyError:
            print(
                "error: Invalid example. Valid example keys (some point to the same layout) "
                f"are: {list(EXAMPLES)}"
            )
            raise typer.Exit(2)

        treb_rows, bass_rows = read_layout(layout_spec)

        plot(treb_rows, bass_rows, rotation=rotation, figsize=figsize)
        print("Close plot to exit.")

        plt.show()

else:

    def app():
        print("Install `typer` to use the melplot CLI")
        raise SystemExit(1)


if __name__ == "__main__":
    app()
