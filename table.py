from rich.console import Console
from rich.table import Table

table = Table(title="--Menu--")

table.add_column("num", style="cyan")
table.add_column("activity", style="magenta")

table.add_row("1.", "Add expense")
table.add_row("2.", "View budget")
table.add_row("3.", "View balance")
table.add_row("4.", "Finish")
console = Console()

def menu():
    console.print(table)

