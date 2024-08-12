from rich.table import Table
from rich.console import Console

def table()
        console = Console()
        table = Table(title="Exemple de Tableau")

        table.add_column("Nom", justify="right", style="cyan", no_wrap=True)
        table.add_column("Âge", style="magenta")
        table.add_column("Ville", justify="right", style="green")

        table.add_row("Alice", "24", "Paris")
        table.add_row("Bob", "30", "Lyon")
        table.add_row("Charlie", "28", "Marseille")

        console.print(table)