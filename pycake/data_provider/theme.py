import sys
import time
from rich.console import Console
from rich.rule import Rule
from rich.text import Text
from rich.style import Style

console = Console()

cli_colors = {
    "col_red": "#b5535b",
    "col_gold": "#cc9d31",
    "col_brown": "#5c3232",
    "col_pink": "#b3446c",
}

cli_theme = {
    "pkg": Style(color=cli_colors["col_red"], bold=True, italic=False),
}


def print_logo():
    logo_lines = [
        "  \u2588\u2588\u2588\u2588\u2588\u2588  \u2588\u2588\u2588\u2588\u2588  \u2588\u2588   \u2588\u2588 \u2588\u2588\u2588\u2588\u2588\u2588\u2588",
        " \u2588\u2588      \u2588\u2588   \u2588\u2588 \u2588\u2588  \u2588\u2588  \u2588\u2588     ",
        " \u2588\u2588      \u2588\u2588\u2588\u2588\u2588\u2588\u2588 \u2588\u2588\u2588\u2588\u2588   \u2588\u2588\u2588\u2588\u2588  ",
        " \u2588\u2588      \u2588\u2588   \u2588\u2588 \u2588\u2588  \u2588\u2588  \u2588\u2588     ",
        "  \u2588\u2588\u2588\u2588\u2588\u2588 \u2588\u2588   \u2588\u2588 \u2588\u2588   \u2588\u2588 \u2588\u2588\u2588\u2588\u2588\u2588\u2588"
    ]
    console.print(Rule(style="black"))
    console.print()
    for line in logo_lines:
        console.print(Text(line, style=cli_colors["col_red"]))
    heading = Text("served by Datenbäcker GmbH", style=cli_colors["col_red"])
    console.print(Rule(heading, style="black"))


def set_cake_progress_bar_style(style="cake"):
    styles = {
        "cake": "\U0001F370",
        "birthday_cake": "\U0001F382",
        "cookie": "\U0001F36A",
        "donut": "\U0001F369",
        "bread": "\U0001F35E",
        "croissant": "\U0001F950"
    }
    if style not in styles:
        raise ValueError(f"Invalid style '{style}'. Must be one of: {', '.join(styles.keys())}")

    return styles[style]


def cake_progress_bar(total_steps, style="cake"):
    symbol = set_cake_progress_bar_style(style)
    start_time = time.time()

    def update(progress):
        elapsed = time.time() - start_time
        if progress > 0:
            est_total_time = (elapsed / progress) * total_steps
            eta = int(est_total_time - elapsed)
        else:
            eta = 0

        percent = round((progress / total_steps) * 100)
        complete = symbol * progress
        incomplete = "  " * (total_steps - progress)

        sys.stdout.write(f"\rProcessing request {complete}{incomplete} {percent}% | ETA: {eta}s")
        sys.stdout.flush()
    return update



