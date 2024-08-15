import calendar
import locale
from datetime import datetime
from rich.console import Console
from rich.text import Text

# Initialisation de rich
console = Console()

# Configuration de la locale pour le français
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Liste des jours avec des événements (par exemple, le 3, 14 et 25 du mois)
evenement_jours = [10, 10]

# Obtenir l'année et le mois en cours
now = datetime.now()
year = now.year
month = now.month
today = now.day


cal = calendar.monthcalendar(year, month)


console.print(f"[bold underline]Calendrier  {calendar.month_name[month]} :[/]")
console.print("Lu Ma Me Je Ve Sa Di", style="bold green")

for week in cal:
    line = Text()
    for day in week:
        if day == 0:
            line.append("   ")
        elif day == today:
            line.append(f"{day:2} ", style="bold white on blue")
        elif day in evenement_jours:
            line.append(f"{day:2} ", style="bold green")
        else:
            line.append(f"{day:2} ", style="white")
    console.print(line)