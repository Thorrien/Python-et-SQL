from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.table import Table
from datetime import datetime
import re
from rich.columns import Columns


class ContractView:
    def __init__(self):
        pass

    def logcontracts(self, user, contrats, userDAO):
        """
        Affiche la liste des contrats divisée en trois catégories :
        - Mes contrats : Contrats gérés par l'utilisateur.
        - Contrats sans commercial : Contrats sans utilisateur attitré.
        - Autres contrats : Contrats gérés par d'autres utilisateurs.

        Permet à l'utilisateur de choisir une action en fonction de ses autorisations.

        Entrées:
        - user: L'utilisateur courant.
        - contrats: Liste des contrats à afficher.
        - userDAO: Objet permettant de récupérer les informations supplémentaires sur les entreprises et les utilisateurs.

        Retourne:
        - Le choix de l'utilisateur pour l'action à entreprendre.
        """
        console = Console()
        console.rule("Contrats")
        console.print("")

        mycontracts = []
        Withousalesman = []
        otherscontracts = []
        liste_choix = []
        liste_interdit = []
        liste_sans_choix = []
        liste_choix_entreprise = []
        liste_sans_choix_entreprise = []
        liste_interdit_entreprise = []

        for contrat in contrats:
            if contrat.user_id == user.id:
                mycontracts.append(contrat)
                liste_choix.append(contrats.index(contrat))
                liste_choix_entreprise.append(contrat.compagny_id)
            elif contrat.user_id is None:
                Withousalesman.append(contrat)
                liste_sans_choix.append(contrats.index(contrat))
                liste_sans_choix_entreprise.append(contrat.compagny_id)
            elif contrat.user_id != user.id:
                otherscontracts.append(contrat)
                liste_interdit.append(contrats.index(contrat))
                liste_interdit_entreprise.append(contrat.compagny_id)

        def create_table(liste, car):
            if car == "MY":
                table = Table(title="Mes contrats", box=None)
            elif car == "OT":
                table = Table(title="Autres contrats", box=None)
            elif car == "NO":
                table = Table(title="Contrats sans commercial", box=None)
            if car == "MY":
                table.add_column("Contrat", justify="center",
                                 style="green", no_wrap=True)
            else:
                table.add_column("Contrat", justify="center",
                                 style="#FFA500", no_wrap=True)
            table.add_column("Entreprise", justify="left", style="white")
            table.add_column("Etat", justify="left", style="white")
            table.add_column("Taux de paiement", justify="left", style="white")
            table.add_row("", "")
            for contrat in liste:
                if contrat.sign:
                    Etat = "Signé"
                else:
                    Etat = "Non signé"  
                Taux = f"{round(((contrat.current_amont / contrat.total_amont )*100), 2)} %"
                entreprise = f"{contrat.compagny_id} - {userDAO.get_company(contrat.compagny_id).company_name}"
                table.add_row(f"{contrats.index(contrat)}",
                              entreprise, Etat, Taux)

            return table

        table1 = create_table(mycontracts, "MY")
        table2 = create_table(otherscontracts, "OT")
        table3 = create_table(Withousalesman, "NO")

        console.print(Columns([table1, table3, table2], padding=(0, 5)))
        console.print("")
        console.print("-" * console.width)
        centered_text = Text("Choix d'actions", style="bold green")
        console.print(Align.center(centered_text))

        tablechoix = Table(box=None)
        tablechoix.add_column("Choix", justify="center",
                              style="green", no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")

        tablechoix.add_row("", "")
        if user.authorisation('Sale'):
            tablechoix.add_row("CR<id>", "Créer un nouveau "
                               "contrat pour la société <id>")
            tablechoix.add_row("A<id>", "Afficher le détail d'un contrat<id>")
            tablechoix.add_row("E<id>",
                               "Afficher le détail d'une entreprise<id>")
            tablechoix.add_row("S<id>", "[blue]Suprimer "
                               "définitivement [/blue]le contrat<id>")
        else:
            tablechoix.add_row("[red][strike]CR<id>[/red][/strike]",
                               "[red]Créer un nouveau contrat pour"
                               " la société <id>[/red]🔒")
            tablechoix.add_row("A<id>", "Afficher le détail "
                               "d'un contrat <id>")
            tablechoix.add_row("E<id>", "Afficher le détail "
                               "d'une entreprise<id>")
            tablechoix.add_row("[red][strike]S<id>[/red][/strike]",
                               "[red]Suprimer définitivement "
                               "le contrat<id>[/red]🔒")
        tablechoix.add_row("RET", "Retour au menu principal")
        tablechoix.add_row("QUIT", "Quitter l'application")
        console.print("")
        console.print(tablechoix)
        console.print("")
        if user.authorisation('Sale'):
            valid_choices = ["RET", "QUIT"]
        else:
            valid_choices = ["RET", "QUIT"]
        invalid_choices = []
        console.print("")

        for element in liste_choix:
            valid_choices.append(f"A{element}")
            valid_choices.append(f"S{element}")
        for element in liste_interdit:
            valid_choices.append(f"A{element}")
            invalid_choices.append(f"S{element}")
        for element in liste_sans_choix:
            valid_choices.append(f"A{element}")
            invalid_choices.append(f"S{element}")
        for element in liste_choix_entreprise:
            valid_choices.append(f"CR{element}")
            valid_choices.append(f"E{element}")
        for element in liste_interdit_entreprise:
            invalid_choices.append(f"CR{element}")
            valid_choices.append(f"E{element}")
        for element in liste_sans_choix_entreprise:
            valid_choices.append(f"E{element}")
            invalid_choices.append(f"CR{element}")

        while True:
            console.print("Votre choix [#AAAAAA]( CR, "
                          "A18, E9 ...)[/#AAAAAA] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            elif choix in invalid_choices:
                console.print("[red]Ce n'est pas une "
                              "de vos entreprises.[/red]")
            else:
                console.print("[red]Choix invalide. "
                              "Veuillez essayer à nouveau.[/red]")

    def createcontract(self, user, company):
        """
        Permet à un utilisateur autorisé de créer un nouveau contrat pour une entreprise spécifique.
        Recueille les informations sur le contrat, les confirme, puis les retourne.

        Entrées:
        - user: L'utilisateur courant.
        - company: L'entreprise pour laquelle créer un contrat.

        Retourne:
        - Tuple (total_amont, current_amont, sign): Les données saisies pour le nouveau contrat.
        """
        if company.user_id == user.id:
            choix = None
            while choix != 'Oui':
                console = Console()
                pattern = re.compile(r"^\d+(.\d{1,2})?$")
                console.rule("Création d'un nouveau contrat ")
                console.print("")

                while True:
                    console.print("[green] Montant total du"
                                " contrat (Sans le €) [/green]")
                    total_amont = input('==>')
                    if pattern.match(total_amont):
                        break
                    else:
                        console.print("[red]Entrée invalide. Veuillez "
                                    "entrer uniquement des chiffres "
                                    "et un point.[/red]")

                while True:
                    console.print("[green] Montant actuellement"
                                " payé (Sans le €) [/green]")
                    current_amont = input('==>')
                    if pattern.match(current_amont):
                        break
                    else:
                        console.print("[red]Entrée invalide. "
                                    "Veuillez entrer uniquement des chiffres "
                                    "et un point.[/red]")

                console.print("[green] Le contrat est il"
                            " signé ? (Oui / Non)[/green]")
                valid_role = ["Oui", "Non"]
                role = None
                while role not in valid_role:
                    role = input('==>')
                    if role == "Oui":
                        sign = True
                    elif role == "Non":
                        sign = False
                    else:
                        console.print("[red]Choix invalide. "
                                    "Veuillez essayer à nouveau.[/red]")

                console.rule("Résumé de votre saisie pour confirmation")
                console.print("")
                tableconfirmation = Table(box=None)
                tableconfirmation.add_column("Type", justify="left",
                                            style="green", no_wrap=True)
                tableconfirmation.add_column("Vos saisies",
                                            justify="left", style="white")
                tableconfirmation.add_row("", "")
                tableconfirmation.add_row("Entreprise", f"{company.company_name}")
                tableconfirmation.add_row("Gestionnaire", "Vous")
                tableconfirmation.add_row("Montant total", f"{total_amont}")
                tableconfirmation.add_row("Montant actuel", f"{current_amont}")
                tableconfirmation.add_row("Contrat Signé", f"{role}")
                console.print(tableconfirmation)

                console.print("")
                console.print("-" * console.width)
                centered_text = Text("Confirmez vous votre saisie ?",
                                    style="bold green")
                console.print(Align.center(centered_text))

                console.print("[green] Oui ou Non [/green]")
                valid_role = ["Oui", "Non"]
                while True:
                    choix = input('==>')
                    if choix in valid_role:
                        if choix == "Oui":
                            return total_amont, current_amont, sign
                        else:
                            break
                    else:
                        console.print("[red]Choix invalide. "
                                    "Veuillez essayer à nouveau.[/red]")

    def contractview(sel, user, company, contrat, events, userDAO):
       """
        Affiche les détails d'un contrat spécifique et les événements associés pour une entreprise.
        Propose un menu d'actions que l'utilisateur peut entreprendre en fonction de ses autorisations.

        Entrées:
        - user: L'utilisateur courant.
        - company: L'entreprise associée au contrat.
        - contrat: Le contrat à afficher.
        - events: Liste des événements associés au contrat.
        - userDAO: Objet permettant de récupérer les informations supplémentaires sur les utilisateurs.

        Retourne:
        - Le choix de l'utilisateur pour l'action à entreprendre.
        """
        console = Console()
        console.rule(f"Détail complet du contrat {contrat.id}"
                     f" de l'entreprise {company.company_name}")
        console.print("")

        events_id = []

        def create_table(liste, car):
            if car == "Données contrat":
                table = Table(title=f"{car}", box=None)
                table.add_column("Type", justify="left",
                                 style="green", no_wrap=True)
                table.add_column("Donnée", justify="left", style="white")
                table.add_row("", "")
                table.add_row("Entreprise", f"{company.company_name}")
                if user.id == company.user_id:
                    table.add_row("Gestionnaire", "Vous")
                else:
                    table.add_row("Gestionnaire",
                                  f"{userDAO.get_user(contrat.user_id).nom}")
                table.add_row("Montant total", f"{contrat.total_amont} €")
                table.add_row("Montant versé", f"{contrat.current_amont} €")
                table.add_row("Date de création",
                              f"{contrat.creation_date.strftime(
                                  "%Y-%m-%d %H:%M:%S")}")
                table.add_row("Date de modification",
                              f"{contrat.update_date.strftime(
                                  "%Y-%m-%d %H:%M:%S")}")
                if contrat.sign:
                    signe = "Oui"
                else:
                    signe = "Non"
                table.add_row("Contrat signé", f"{signe}")
                return table
            elif car == "Evènements":
                table = Table(title=f"{car} de l'entreprise", box=None)
                table.add_column("Id", justify="center",
                                 style="green", no_wrap=True)
                table.add_column("Date de début",
                                 justify="left", style="white")
                table.add_column("Date de fin", justify="left", style="white")
                table.add_column("Localisation", justify="left", style="white")
                table.add_row("", "")
                for element in liste:
                    table.add_row(str(element.id),
                                  element.event_date_start.strftime(
                                      '%Y-%m-%d %H:%M:%S'),
                                  element.event_date_end.strftime(
                                      '%Y-%m-%d %H:%M:%S'),
                                  element.location)
                    events_id.append(element.id)
                return table

        table1 = create_table(contrat, "Données contrat")
        table4 = create_table(events, "Evènements")

        vertical_line = Text("\n".join("|" for _ in range(10)), style="green")

        console.print(Columns([table1, vertical_line, table4], padding=(0, 5)))
        console.print("")
        console.print("-" * console.width)
        centered_text = Text("Choix d'actions", style="bold green")
        console.print(Align.center(centered_text))

        tablechoix = Table(box=None)
        tablechoix.add_column("Choix", justify="left",
                              style="green", no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")

        tablechoix.add_row("", "")
        if company.user_id == user.id and user.authorisation('Sale'):
            tablechoix.add_row("CR", "Créer un nouvel évènement")
            tablechoix.add_row("A<id>",
                               "Afficher le détail de l'évènement <id>")
            tablechoix.add_row("MT <Nouvelle donnée>", "Modifier le montant "
                               "total du contrat par <Nouvelle donnée>")
            tablechoix.add_row("MV <Nouvelle donnée>", "Modifier le montant"
                               " versé du contrat par <Nouvelle donnée>")
            tablechoix.add_row("MS SI/NS", "Modifier l'état du contrat : SI = "
                               "Signé / NS = Non Signé ")
            tablechoix.add_row("SUPPRIMER", "[blue]Supprimer définitivement"
                               "[/blue] le contrat")
            tablechoix.add_row("RET", "Retour au menu principal")
            tablechoix.add_row("QUIT", "Quitter le programme")
            console.print("")
        else:
            tablechoix.add_row("[red][strike]CR[/red][/strike]", "[red]Créer "
                               "un nouvel évènement[/red]🔒")
            tablechoix.add_row("A<id>", "Afficher le détail de l'évènement ")
            tablechoix.add_row("[red][strike]MT <Nouvelle donnée>"
                               "[/red][/strike]", "[red]Modifier le montant "
                               "total du contrat par <Nouvelle donnée>[/red]🔒")
            tablechoix.add_row("[red][strike]MV <Nouvelle donnée>[/red]"
                               "[/strike]", "[red]Modifier le montant versé du"
                               " contrat par <Nouvelle donnée>[/red]🔒")
            tablechoix.add_row("[red][strike]MS SI/NS[/red][/strike]",
                               "[red]Modifier l'état du contrat : SI = "
                               "Signé / NS = Non Signé[/red]🔒")
            tablechoix.add_row("[red][strike]SUPPRIMER[/red][/strike]",
                               "[red]Suprimer définitivement "
                               "le contrat[/red]🔒")
            tablechoix.add_row("RET", "Retour au menu principal")
            tablechoix.add_row("QUIT", "Quitter le programme")
            console.print("")

        console.print(tablechoix)
        console.print("")
        if company.user_id == user.id and user.authorisation('Sale'):
            valid_choices = ["CR", "RET", "QUIT",
                             "SUPPRIMER", "MS SI", "MS NS"]
            invalid_choices = []
            valid_choices_with_id = ["MT", "MV"]
        elif company.user_id is None:
            valid_choices = ["RET", "QUIT"]
            invalid_choices = ["CR", "SUPPRIMER",
                               "SUPPRIMER", "MS SI", "MS NS"]
            valid_choices_with_id = []
        else:
            valid_choices = ["RET", "QUIT"]
            invalid_choices = ["CR", "SUPPRIMER",
                               "SUPPRIMER", "MS SI", "MS NS"]
            valid_choices_with_id = []

        console.print("")

        if company.user_id == user.id:
            for element in events_id:
                valid_choices.append(f"A{element}")
        else:
            for element in events_id:
                valid_choices.append(f"A{element}")

        while True:
            console.print("Votre choix [#AAAAAA]( CR, "
                          "A18, D9 ...)[/#AAAAAA] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            elif any(choix.startswith(c) for c in valid_choices_with_id):
                if choix.startswith("MT ") or choix.startswith("MV "):
                    try:
                        float(choix[3:])
                    except ValueError:
                        print("Erreur : La partie après 'MT,  MV' doit être "
                              "un nombre valide ( chiffres et"
                              " point seulement).")
                    else:
                        return choix
            elif choix in invalid_choices:
                console.print("[red]Ce n'est pas une de "
                              "vos entreprises.[/red]")
            else:
                console.print("[red]Choix invalide. Veuillez "
                              "essayer à nouveau.[/red]")

    def createevent(self, company, user, supports):
        """
        Permet à un utilisateur autorisé de créer un nouvel événement pour une entreprise spécifique.
        Recueille les informations sur l'événement, les confirme, puis les retourne.

        Entrées:
        - company: L'entreprise pour laquelle créer un événement.
        - user: L'utilisateur courant.
        - supports: Liste des supports disponibles pour l'événement.

        Retourne:
        - Tuple (event_date_start, event_date_end, location, support_id, attendees, notes): 
          Les données saisies pour le nouvel événement.
        """
        if company.user_id == user.id:
            choix = None
            while choix != 'Oui':
                console = Console()
                pattern = re.compile(r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$")
                console.rule("Création d'un nouvel évènement")
                console.print("")

                while True:
                    console.print("[green] Date et heure de début de l'évènement "
                                "(format : JJ/MM/AAAA HH:MM) : [/green]")
                    event_start = input('==>')
                    if pattern.match(event_start):
                        event_date_start = datetime.strptime(event_start,
                                                            "%d/%m/%Y %H:%M")
                        break
                    else:
                        console.print("[red]Entrée invalide. Veuillez entrer "
                                    "uniquement des chiffres et un point.[/red]")

                while True:
                    console.print("[green] Date et heure de fin de l'évènement "
                                "(format : JJ/MM/AAAA HH:MM) : [/green]")
                    event_end = input('==>')
                    if pattern.match(event_end):
                        event_date_end = datetime.strptime(event_end,
                                                        "%d/%m/%Y %H:%M")
                        break
                    else:
                        console.print("[red]Entrée invalide. Veuillez entrer "
                                    "uniquement des chiffres et un point.[/red]")

                console.print("[green] Lieu de l'évènement : [/green]")
                location = input('==>')

                console.print("[green] Nombre de personnes : [/green]")
                attendees = input('==>')

                console.print("[green] Notes : [/green]")
                notes = input('==>')

                console.print("[green] Liste des supports disponibles : [/green]")
                valid_role = []
                for element in supports:
                    valid_role.append(element.id)
                    console.print(f"[green]{element.id}[/green]     {element.nom}")
                console.print("")
                console.print("[green] Id du support chargé "
                            "de l'évènement [/green]")
                role = None
                print(valid_role)
                while role not in valid_role:
                    role = int(input('==>'))
                    if role in valid_role:
                        support_id = role
                    else:
                        console.print("[red]Choix invalide. Veuillez "
                                    "essayer à nouveau.[/red]")

                console.rule("Résumé de votre saisie pour confirmation")
                console.print("")
                tableconfirmation = Table(box=None)
                tableconfirmation.add_column("Type", justify="left", style="green",
                                            no_wrap=True)
                tableconfirmation.add_column("Vos saisies", justify="left",
                                            style="white")
                tableconfirmation.add_row("", "")
                tableconfirmation.add_row("Entreprise", f"{company.company_name}")
                tableconfirmation.add_row("Gestionnaire", "xxxxxxxxxxxxxxxxx")
                tableconfirmation.add_row("Date et heure de début de l'évènement",
                                        f"{event_date_start.strftime(
                                            '%Y-%m-%d %H:%M:%S')}")
                tableconfirmation.add_row("Date et heure de fin de l'évènement",
                                        f"{event_date_end.strftime(
                                            '%Y-%m-%d %H:%M:%S')}")
                tableconfirmation.add_row("Lieu de l'évènement", f"{location}")
                tableconfirmation.add_row("Nombre de personnes", f"{attendees}")
                tableconfirmation.add_row("Notes", f"{notes}")
                console.print(tableconfirmation)

                console.print("")
                console.print("-" * console.width)
                centered_text = Text("Confirmez vous votre saisie ?",
                                    style="bold green")
                console.print(Align.center(centered_text))

                console.print("[green] Oui ou Non [/green]")
                valid_role = ["Oui", "Non"]
                while True:
                    choix = input('==>')
                    if choix in valid_role:
                        if choix == "Oui":
                            return event_date_start, event_date_end, location, support_id, attendees, notes
                        else:
                            break
                    else:
                        console.print("[red]Choix invalide. Veuillez"
                                    " essayer à nouveau.[/red]")
