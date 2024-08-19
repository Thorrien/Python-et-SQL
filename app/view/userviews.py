
from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.table import Table
from time import sleep
from rich.columns import Columns


class UserView:
    def __init__(self):
        pass

    def logutilisateurs(self, user, users):
        console = Console()
        console.rule("Comptes utilisateurs")
        console.print("")
        third = len(users) // 3
        first_third = users[:third]
        second_third = users[third:2*third]
        third_third = users[2*third:]
        liste_choix = []

        def create_table(users):
            table = Table(box=None)
            table.add_column("Id", justify="center", style="green",
                             no_wrap=True)
            table.add_column("Nom", justify="left", style="white")
            table.add_column("Role", justify="left", style="white")
            table.add_row("", "")
            for usersolo in users:
                table.add_row(str(usersolo['user_id']), usersolo['user_name'],
                              usersolo['role_name'])
                liste_choix.append(str(usersolo['user_id']))

            return table

        table1 = create_table(first_third)
        table2 = create_table(second_third)
        table3 = create_table(third_third)

        console.print(Columns([table1, table2, table3], padding=(0, 10)))
        console.print("")
        console.print("-" * console.width)
        centered_text = Text("Choix d'actions", style="bold green")
        console.print(Align.center(centered_text))

        tablechoix = Table(box=None)
        tablechoix.add_column("Choix", justify="center", style="green",
                              no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")

        tablechoix.add_row("", "")
        tablechoix.add_row("CR", "Créer un nouvel utilisateur")
        tablechoix.add_row("A<id>", "Afficher le détail d'un utilisateur <id>")
        tablechoix.add_row("M<id>", "Modifier un élément "
                           "d'un utilisateur <id>")
        tablechoix.add_row("S<id>", "[orange] Suprimer "
                           "définitivement [/orange] l'utilisateur <id>")
        tablechoix.add_row("RET", "Retour au menu précédent")
        tablechoix.add_row("QUIT", "quitter l'application")
        console.print("")
        console.print(tablechoix)
        console.print("")
        valid_choices = ["CR", "RET", "QUIT"]
        console.print("")
        for element in liste_choix:
            valid_choices.append(f"A{element}")
            valid_choices.append(f"M{element}")
            valid_choices.append(f"S{element}")

        while True:
            console.print("Votre choix [#AAAAAA]( CR, "
                          "A18, D9 ...)[/#AAAAAA] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            else:
                console.print("[red]Choix invalide. Veuillez "
                              "essayer à nouveau.[/red]")

    def soloUserView(self, user, affiche):
        console = Console()
        console.rule(f"Données de l'utilisateur {affiche.nom} ")
        console.print("")
        tabledonneessolo = Table(box=None)
        tabledonneessolo.add_column("Type", justify="left",
                                    style="green", no_wrap=True)
        tabledonneessolo.add_column("Information", justify="left",
                                    style="white")
        tabledonneessolo.add_row("", "")
        tabledonneessolo.add_row("Id", f"{affiche.id}")
        tabledonneessolo.add_row("Nom", f"{affiche.nom}")
        tabledonneessolo.add_row("Email", f"{affiche.email}")
        tabledonneessolo.add_row("Service", f"{affiche.role_id}")
        tabledonneessolo.add_row("Date de création",
                                 f"{affiche.date_creation}")
        console.print(tabledonneessolo)

        console.print("")
        console.print("-" * console.width)
        centered_text = Text("Choix d'actions", style="bold green")
        console.print(Align.center(centered_text))
        tablechoix = Table(box=None)
        tablechoix.add_column("Choix", justify="left", style="green",
                              no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")
        tablechoix.add_row("", "")
        tablechoix.add_row("NO <Nouvelle Donnée>", "Modifier le nom de "
                           "l'utilisateur par <Nouvelle Donnée>")
        tablechoix.add_row("EM <Nouvelle Donnée>", "Modifier l'Email de"
                           " l'utilisateur par <Nouvelle Donnée>")
        tablechoix.add_row("RE <Nouvelle Donnée>", "Modifier le mot de passe"
                           " de l'utilisateur par <Nouvelle Donnée>")
        tablechoix.add_row("SE <AD/VE/GE/SU>", "Modifier le Service de "
                           "l'utilisateur par AD = Admin, VE = Ventes, "
                           "GE = Gestion et SU = Support")
        tablechoix.add_row("SUPPRIMER", "[blue]Supprime définitivement[/blue] "
                           "l'utilisateur de la base de donnée")
        tablechoix.add_row("RET", "Retour au menu précédent")
        tablechoix.add_row("QUIT", "quitter l'application")
        console.print("")
        console.print(tablechoix)
        console.print("")
        valid_choices = ["CR", "SUPPRIMER", "RET", "QUIT",
                         "SE AD", "SE SU", "SE VE", "SE GE"]
        valid_choices_with_id = ["NO", "EM", "RE"]
        console.print("")
        while True:
            console.print("Votre choix [#AAAAAA]( SE AD, NO Eric, "
                          "EM martin@tot.fr ...)[/#AAAAAA] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            elif any(choix.startswith(c) for c in valid_choices_with_id):
                return choix
            else:
                console.print("[red]Choix invalide. Veuillez essayer "
                              "à nouveau.[/red]")

    def notautorized(self, user):
        console = Console()
        console.rule(f"[red] {user.nom}, vous n'avez pas les droits "
                     "permettant d'utiliser cette fonctionnalité[/red]")
        sleep(2)

    def base(self):
        console = Console()
        console.rule("Fin de la page")

    def createuserview(self):
        choix = None
        while choix != 'Oui':
            console = Console()
            console.rule("Création d'un nouvel utilisateur ")
            console.print("")
            console.print("[green] Le nom de l'utilisateur [/green]")
            nom = str(input('==>'))
            console.print("[green] L'Email de l'utilisateur [/green]")
            email = str(input('==>'))
            console.print("[green] Le Mot de passe de l'utilisateur [/green]")
            mot_de_passe = str(input('==>'))
            console.print("[green] Le service de l'utilisateur : 1 (Admin), "
                        "2 (Gestion), 3 (Vente), 4 (Support) [/green]")
            role = None
            valid_role = ["1", "2", "3", "4"]
            while True:
                role = input('==>')
                if role in valid_role:
                    break
                else:
                    console.print("[red]Choix invalide. Veuillez "
                                "essayer à nouveau.[/red]")

            console.rule("Résumé de votre saisie pour confirmation")
            console.print("")
            tableconfirmation = Table(box=None)
            tableconfirmation.add_column("Type", justify="left",
                                        style="green", no_wrap=True)
            tableconfirmation.add_column("Vos saisies", justify="left",
                                        style="white")
            tableconfirmation.add_row("", "")
            tableconfirmation.add_row("Nom", f"{nom}")
            tableconfirmation.add_row("Email", f"{email}")
            tableconfirmation.add_row("Mot de passe", f"{mot_de_passe}")
            tableconfirmation.add_row("Service", f"{role}")
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
                if choix == "Oui":
                    return nom, email, mot_de_passe, role
                else:
                    break

    def logWithoutUser(self, user, events, companys):
        console = Console()
        console.rule("Détail de tous les éléments non attribués ")
        console.print("")

        valid_choices = ["RET", "QUIT"]

        def create_table2(liste, text):
            table = Table(title=f"{text}", box=None)
            if text == 'Evènements':
                table.add_column("id", justify="left", style="white",
                                 no_wrap=True)
                table.add_column("Participants", justify="left",
                                 style="white", no_wrap=True)
                table.add_column("Date de début", justify="left",
                                 style="white", no_wrap=True)
            else:
                table.add_column("id", justify="left", style="white",
                                 no_wrap=True)
                table.add_column("Nom", justify="left", style="white",
                                 no_wrap=True)
            table.add_row("", "")
            for element in liste:
                if text == 'Evènements':
                    table.add_row(str(element.id), str(element.attendees),
                                  element.event_date_start.strftime(
                                      "%Y-%m-%d %H:%M:%S"))
                    valid_choices.append(f"AE{element.id}")
                else:
                    table.add_row(str(element.id), element.company_name)
                    valid_choices.append(f"AC{element.id}")

            return table
        table1 = create_table2(events, 'Evènements')
        table2 = create_table2(companys, 'Entreprises')

        console.print("-" * console.width)

        console.print(Columns([table1, table2], padding=(0, 10)))
        console.print("")
        console.print("-" * console.width)
        centered_text = Text("Choix d'actions", style="bold green")
        console.print(Align.center(centered_text))

        tablechoix = Table(box=None)
        tablechoix.add_column("Choix", justify="left", style="green",
                              no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")

        tablechoix.add_row("", "")
        tablechoix.add_row("AE<id>", "Attribuer l'évènement <id>")
        tablechoix.add_row("AC<id>", "Attribuer l'entreprise <id>")
        tablechoix.add_row("RET", "Retour au menu précédent")
        tablechoix.add_row("QUIT", "Quitter le programme")
        console.print("")

        console.print(tablechoix)
        console.print("")

        while True:
            console.print("Votre choix [#AAAAAA](RET, AE5 ...)[/#AAAAAA] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            else:
                console.print("[red]Choix invalide. Veuillez"
                              " essayer à nouveau.[/red]")

    def chooseUser(self, users):
        console = Console()
        console.rule("Liste des persones correpondantes")
        console.print("")
        valid_choices = ["RET", "QUIT"]

        def create_table(liste):
            table = Table(title="Utilisateurs", box=None)
            table.add_column("id", justify="left", style="white", no_wrap=True)
            table.add_column("Nom", justify="left", style="white",
                             no_wrap=True)
            table.add_column("Email", justify="left", style="white",
                             no_wrap=True)
            table.add_row("", "")
            for element in liste:
                table.add_row(str(element.id), element.nom, element.email)
                valid_choices.append(f"A{element.id}")
            return table

        table1 = create_table(users)

        console.print("-" * console.width)
        console.print(table1)
        console.print("")
        console.print("-" * console.width)
        centered_text = Text("Choix d'actions", style="bold green")
        console.print(Align.center(centered_text))

        tablechoix = Table(box=None)
        tablechoix.add_column("Choix", justify="left", style="green",
                              no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")

        tablechoix.add_row("", "")
        tablechoix.add_row("A<id>", "Attribuer l'évènement a <id>")
        tablechoix.add_row("RET", "Retour au menu précédent")
        tablechoix.add_row("QUIT", "Quitter le programme")
        console.print("")

        console.print(tablechoix)
        console.print("")

        while True:
            console.print("Votre choix [#AAAAAA](A5, QUIT ...)[/#AAAAAA] :")
            choix = input('==>')
            if choix in valid_choices:
                if choix.startswith('A'):
                    return choix[1:]
                else:
                    return choix
            else:
                console.print("[red]Choix invalide. "
                              "Veuillez essayer à nouveau.[/red]")
