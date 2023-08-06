from rich.console import Console
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    TimeElapsedColumn,
    MofNCompleteColumn,
    SpinnerColumn,
)

__all__ = ["Pbar", "console"]

console = Console()

Pbar = Progress(
    SpinnerColumn(),
    TextColumn("[bold cyan]{task.description}", justify="right"),
    "[blue]★[/blue]",
    BarColumn(bar_width=None),
    "[red]★[/red]",
    "[progress.percentage]{task.percentage:>3.0f}%",
    "[yellow]★[/yellow]",
    TimeElapsedColumn(),
    "[magenta]★[/magenta]",
    TimeRemainingColumn(),
    "[pink]★[/pink]",
    MofNCompleteColumn(),
    console=console
)