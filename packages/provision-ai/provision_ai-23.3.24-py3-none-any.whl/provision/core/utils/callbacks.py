"""Custom Lightning callbacks."""

import os

import rich.box
from lightning.pytorch.callbacks import RichModelSummary
from lightning.pytorch.utilities.model_summary.model_summary import (
    get_human_readable_count,
)
from rich import get_console
from rich.console import Group
from rich.panel import Panel
from rich.table import Table

from .logging import info_bold

COLOR = {
    "LAYER": "#ff79c6",
    "METRIC": "#50FA7B",
    "COUNT": "#8be9fd",
}


class CustomRichModelSummary(RichModelSummary):
    """Customized version of the Lightning RichModelSummary callback."""

    @staticmethod
    def summarize(  # # noqa: CCR001
        summary_data: list[tuple[str, list[str]]],  # noqa: TAE002
        total_parameters: int,
        trainable_parameters: int,
        model_size: float,
    ) -> None:
        """Summarize the model layers."""
        console = get_console()

        table = Table(header_style="bold yellow", box=rich.box.SIMPLE, border_style="yellow")
        table.add_column(" ", style="dim")
        table.add_column("Name", justify="left", no_wrap=True)
        table.add_column("Type")
        table.add_column("Params", justify="right")

        column_names = list(zip(*summary_data))[0]

        for column_name in ["In sizes", "Out sizes"]:
            if column_name in column_names:
                table.add_column(column_name, justify="right", style="white")

        rows: list[tuple[str, ...]] = list(zip(*(arr[1] for arr in summary_data)))
        for row in rows:
            idx, name, type, params = row
            level = name.count(".")
            is_metric = name.startswith("metrics")

            if is_metric:
                name = f"[{COLOR['METRIC']}]{name}[/]"
            else:
                name = f"[{COLOR['LAYER']}]{name}[/]"

            if level == 0:
                name = f"[bold]{name}[/]"
                type = f"[bold yellow]{type}[/]" if not is_metric else f"[bold]{type}[/]"
                params = f"[bold {COLOR['COUNT']}]{params}[/]"
            else:
                params = f"[{COLOR['COUNT']}]{params}[/]"

            indented_name = "  " * level + name
            table.add_row(idx, indented_name, type, params)

        parameters: list[str] = []
        for param in [trainable_parameters, total_parameters - trainable_parameters, total_parameters, model_size]:
            parameters.append("{:<{}}".format(get_human_readable_count(int(param)), 10))

        # TODO: Adjust parameter count formatting

        grid = Table.grid(expand=True)
        grid.add_column()
        grid.add_column()

        grid.add_row(f"[bold]Trainable params[/]: {parameters[0]}")
        grid.add_row(f"[bold]Non-trainable params[/]: {parameters[1]}")
        grid.add_row(f"[bold]Total params[/]: {parameters[2]}")
        grid.add_row(f"[bold]Total estimated model params size (MB)[/]: {parameters[3]}")

        console.print(
            Panel(
                Group(table, grid),
                title="System summary",
                border_style="bold yellow",
                subtitle=os.getenv("RUN_NAME"),
            )
        )

        info_bold("Commencing training... ")
