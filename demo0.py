#!pip install rich

from rich import print
from rich.console import Console

print(f"Выражение 5 + 5 = {5+5}")

console = Console()

console.print("This is just Text", style = "bold underline")