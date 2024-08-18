from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.table import Table
from datetime import datetime
import re
from rich.columns import Columns
import calendar
import locale


class EventView:
    def __init__(self):
        pass

                                   
    def eventview(self, user, event, userDAO):
        console = Console()
        console.rule(f"Données de l'évènement {event.id} ")
        console.print("")
        tabledonneessolo = Table(box=None)
        tabledonneessolo.add_column("Type", justify="left", style="green", no_wrap=True)
        tabledonneessolo.add_column("Information", justify="left", style="white")
        tabledonneessolo.add_row("", "")
        tabledonneessolo.add_row("Id", f"{event.id}")
        if user.id == event.id_user :
            tabledonneessolo.add_row("Gestionnaire", "Vous")
        else:
            tabledonneessolo.add_row("Gestionnaire", f"{userDAO.get_user(event.id_user).nom}")
        tabledonneessolo.add_row("Date de début", f"{event.event_date_start.strftime('%Y-%m-%d %H:%M:%S')}")
        tabledonneessolo.add_row("Date de fin", f"{event.event_date_end.strftime('%Y-%m-%d %H:%M:%S')}")
        tabledonneessolo.add_row("Localisation", f"{event.location}")
        tabledonneessolo.add_row("Participants", f"{event.attendees}")
        tabledonneessolo.add_row("Notes", f"{event.notes}")
        console.print(tabledonneessolo)
        
        console.print("")
        console.print("-" * console.width)
        centered_text = Text("Choix d'actions", style="bold green")
        console.print(Align.center(centered_text))
        tablechoix = Table(box=None)
        tablechoix.add_column("Choix", justify="left", style="green", no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")
        tablechoix.add_row("", "")
        if event.id_user == user.id and user.authorisation('Support'):
            tablechoix.add_row("MS <Nouvelle Donnée>", "Modifier la date de début <Nouvelle Donnée au format : JJ/MM/AAAA HH:MM>")
            tablechoix.add_row("ME <Nouvelle Donnée>", "Modifier la date de fin <Nouvelle Donnée au format : JJ/MM/AAAA HH:MM>")
            tablechoix.add_row("ML <Nouvelle Donnée>", "Modifier la localisation par <Nouvelle Donnée>")
            tablechoix.add_row("MA <Nouvelle Donnée>", "Modifier le nombre de participants par <Nouvelle Donnée>")
            tablechoix.add_row("MN <Nouvelle Donnée>", "Modifier les notes par <Nouvelle Donnée>")
            tablechoix.add_row("SUPPRIMER", "[blue]Supprime définitivement[/blue] l'évènement ")
        else : 
            tablechoix.add_row("[red][strike]MS <Nouvelle Donnée>[/red][/strike]", "[red]Modifier la date de début <Nouvelle Donnée au format : JJ/MM/AAAA HH:MM>[/red]🔒")
            tablechoix.add_row("[red][strike]ME <Nouvelle Donnée>[/red][/strike]", "[red]Modifier la date de fin <Nouvelle Donnée au format : JJ/MM/AAAA HH:MM>[/red]🔒")
            tablechoix.add_row("[red][strike]ML <Nouvelle Donnée>[/red][/strike]", "[red]Modifier la localisation par <Nouvelle Donnée>[/red]🔒")
            tablechoix.add_row("[red][strike]MA <Nouvelle Donnée>[/red][/strike]", "[red]Modifier le nombre de participants par <Nouvelle Donnée>[/red]🔒")
            tablechoix.add_row("[red][strike]MN <Nouvelle Donnée>[/red][/strike]", "[red]Modifier les notes par <Nouvelle Donnée>[/red]🔒")
            tablechoix.add_row("[red][strike]SUPPRIMER[/red][/strike]", "[red]Supprime définitivement l'évènement [/red]🔒")
        tablechoix.add_row("LIST", "Retour à la liste des utilisateurs")
        tablechoix.add_row("RET", "Retour au menu principal")
        tablechoix.add_row("QUIT", "quitter l'application")
        console.print("")
        console.print(tablechoix)
        console.print("")
        if event.id_user == user.id and user.authorisation('Support'):
            valid_choices = ["SUPPRIMER", "LIST", "RET", "QUIT"]
            valid_choices_with_id = ["MS ", "ME ", "ML ", "MA ", "MN "]
        else : 
            valid_choices = ["LIST", "RET", "QUIT"]
            valid_choices_with_id = []
        console.print("")
        pattern = re.compile(r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$")
        while True:
            console.print("Votre choix [#AAAAAA]( MA 563, MN Mes notes, MS 25/12/2025 15:50 ...)[/#AAAAAA] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            elif choix == "LIST" :
                return choix
            elif any(choix.startswith(c) for c in valid_choices_with_id):
                if choix.startswith("MS ") or choix.startswith("ME "): 
                    date_str = choix[3:].strip()
                    if not pattern.match(date_str):
                        print("Erreur : Format de la date non valide. Format accepté : JJ/MM/AAAA HH:MM")
                    try:
                        date_obj = datetime.strptime(date_str, "%d/%m/%Y %H:%M")
                        return choix
                    except ValueError:
                        print("")
            else:
                console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")


    def myMensualEvents(self, user, events):
        if user.authorisation('Support'):
            console = Console()
            console.rule(f"Détail des évènements du mois")
            console.print("") 
            current_date = datetime.now()
            current_month = datetime.now().month
            current_year = datetime.now().year
            current_day = datetime.now().day
            if current_date.month == 12:
                next_month = 1
                next_year = current_date.year + 1
            else:
                next_month = current_date.month + 1
                next_year = current_date.year
            events_id = []
            events_days = []
            valid_choices = ["TO", "TT", "RET", "QUIT"]
            events_du_mois = [
                event for event in events
                if event['event_date_start'].month == current_month and event['event_date_start'].year == current_year
            ]
            events_du_mois_apres = [
                event for event in events
                if event['event_date_start'].month == next_month and event['event_date_start'].year == next_year
            ]
            
            def create_table(liste, car):
                if car == "MY":
                    table = Table(title=f"Evènements du mois {calendar.month_name[current_month]}", box=None)
                else:
                    table = Table(title=f"Evènements du mois {calendar.month_name[next_month]}", box=None)
                table.add_column("id", justify="left", style="green", no_wrap=True)
                table.add_column("Entreprise", justify="left", style="white", no_wrap=True)
                table.add_column("Date de début", justify="left", style="white", no_wrap=True )
                table.add_column("Participants", justify="left", style="white")
                table.add_row("", "")
                for event in liste:
                    if (event["id_user"] if isinstance(event, dict) else event.id_user) == user.id:
                        event_id = event["event_id"] if isinstance(event, dict) else event.event_id
                        valid_choices.append(f"A{event_id}")
                        company_name = event["company_name"] if isinstance(event, dict) else event.company_name
                        event_date_start = event["event_date_start"] if isinstance(event, dict) else event.event_date_start
                        attendees = event["attendees"] if isinstance(event, dict) else event.attendees
                        table.add_row(str(event_id), company_name, event_date_start.strftime("%Y-%m-%d %H:%M:%S"),str(attendees))                
                        if car == "MY":
                            event_day = int(event_date_start.day)
                            events_days.append(int(event_day))
                return table
            table1 = create_table(events_du_mois, "MY")
            table2 = create_table(events_du_mois_apres, "MA")

            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
            cal = calendar.monthcalendar(current_year, current_month)
            console.print(f"[bold underline]Calendrier  {calendar.month_name[current_month]} :[/]")
            console.print("Lu Ma Me Je Ve Sa Di", style="bold green")
            for week in cal:
                line = Text()
                for day in week:
                    if day == 0:
                        line.append("   ")
                    elif day == current_day:
                        line.append(f"{day:2} ", style="bold white on blue")
                    elif day in events_days:
                        line.append(f"{day:2} ", style="bold green")
                    else:
                        line.append(f"{day:2} ", style="white")
                console.print(line)
                
                

            vertical_line = Text("\n".join("|" for _ in range(10)), style="green")
            console.print("-" * console.width)
            
            console.print(Columns([table1, table2], padding=(0, 10)))
            console.print("")
            console.print("-" * console.width)
            centered_text = Text("Choix d'actions", style="bold green")
            console.print(Align.center(centered_text))
            
            tablechoix = Table(box=None)
            tablechoix.add_column("Choix", justify="left", style="green", no_wrap=True)
            tablechoix.add_column("Description", justify="left", style="white")
            
            tablechoix.add_row("", "")
            tablechoix.add_row("TO", "Voir tous vos évènements")
            tablechoix.add_row("TT", "Voir tous les évènements")
            tablechoix.add_row("A<id>", "Afficher le détail de l'évènement <id>")
            tablechoix.add_row("RET", "Retour au menu principal")
            tablechoix.add_row("QUIT", "Quitter le programme")
            console.print("")

            
            console.print(tablechoix)
            console.print("")

            while True:
                console.print("Votre choix [#AAAAAA]( TO, TT, A5 ...)[/#AAAAAA] :")
                choix = input('==>')
                if choix in valid_choices:
                    return choix
                else:
                    console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")


    def myTotalEvents(self, user, events):
        if user.authorisation('Support'):
            console = Console()
            console.rule(f"Détail de tous vos évènements")
            console.print("") 

            events_id = []
            valid_choices = ["TT", "RET", "QUIT"]
            myEvents = [
                event for event in events
                if event['id_user']  == user.id
            ]
            
            third = len(myEvents) // 3
            first_third = myEvents[:third]
            second_third = myEvents[third:2*third]
            third_third = myEvents[2*third:]
        
            def create_table(liste):
                table = Table(title=f"Evènements", box=None)
                table.add_column("id", justify="left", style="green", no_wrap=True)
                table.add_column("Entreprise", justify="left", style="white", no_wrap=True)
                table.add_column("Date de début", justify="left", style="white", no_wrap=True )
                table.add_row("", "")
                for event in liste:
                    if (event["id_user"] if isinstance(event, dict) else event.id_user) == user.id:
                        event_id = event["event_id"] if isinstance(event, dict) else event.event_id
                        valid_choices.append(f"A{event_id}")
                        company_name = event["company_name"] if isinstance(event, dict) else event.company_name
                        event_date_start = event["event_date_start"] if isinstance(event, dict) else event.event_date_start
                        table.add_row(str(event_id), company_name, event_date_start.strftime("%Y-%m-%d %H:%M:%S"))
                return table
            
            table1 = create_table(first_third)
            table2 = create_table(second_third)
            table3 = create_table(third_third)

            console.print("-" * console.width)
            
            console.print(Columns([table1, table2, table3], padding=(0, 5)))
            console.print("")
            console.print("-" * console.width)
            centered_text = Text("Choix d'actions", style="bold green")
            console.print(Align.center(centered_text))
            
            tablechoix = Table(box=None)
            tablechoix.add_column("Choix", justify="left", style="green", no_wrap=True)
            tablechoix.add_column("Description", justify="left", style="white")
            
            tablechoix.add_row("", "")
            tablechoix.add_row("TT", "Voir tous les évènements")
            tablechoix.add_row("A<id>", "Afficher le détail de l'évènement <id>")
            tablechoix.add_row("RET", "Retour au menu principal")
            tablechoix.add_row("QUIT", "Quitter le programme")
            console.print("")

            console.print(tablechoix)
            console.print("")

            while True:
                console.print("Votre choix [#AAAAAA](TT, A5 ...)[/#AAAAAA] :")
                choix = input('==>')
                if choix in valid_choices:
                    return choix
                else:
                    console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")

    
    def TotalEvents(self, user, events):
        console = Console()
        console.rule(f"Détail de tous les évènements ")
        console.print("") 

        events_id = []
        valid_choices = ["RET", "QUIT"]

        
        third = len(events) // 3
        first_third = events[:third]
        second_third = events[third:2*third]
        third_third = events[2*third:]
    
        def create_table(liste):
            table = Table(title=f"Evènements", box=None)
            table.add_column("id", justify="left", style="white", no_wrap=True)
            table.add_column("Entreprise", justify="left", style="white", no_wrap=True)
            table.add_column("Date de début", justify="left", style="white", no_wrap=True )
            table.add_row("", "")
            for event in liste:
                event_id = event["event_id"] if isinstance(event, dict) else event.event_id
                valid_choices.append(f"A{event_id}") 
                company_name = event["company_name"] if isinstance(event, dict) else event.company_name
                event_date_start = event["event_date_start"] if isinstance(event, dict) else event.event_date_start
                if (event["id_user"] if isinstance(event, dict) else event.id_user) == user.id:
                    table.add_row(str(event_id), company_name, event_date_start.strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    table.add_row(f"{str(event_id)}🔒", company_name, event_date_start.strftime("%Y-%m-%d %H:%M:%S"))
            return table
        
        table1 = create_table(first_third)
        table2 = create_table(second_third)
        table3 = create_table(third_third)

        console.print("-" * console.width)
        
        console.print(Columns([table1, table2, table3], padding=(0, 5)))
        console.print("")
        console.print("-" * console.width)
        centered_text = Text("Choix d'actions", style="bold green")
        console.print(Align.center(centered_text))
        
        tablechoix = Table(box=None)
        tablechoix.add_column("Choix", justify="left", style="green", no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")
        
        tablechoix.add_row("", "")
        tablechoix.add_row("A<id>", "Afficher le détail de l'évènement <id>")
        tablechoix.add_row("RET", "Retour au menu principal")
        tablechoix.add_row("QUIT", "Quitter le programme")
        console.print("")

        console.print(tablechoix)
        console.print("")

        while True:
            console.print("Votre choix [#AAAAAA](RET, A5 ...)[/#AAAAAA] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            else:
                console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")
