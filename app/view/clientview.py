from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.table import Table
from rich.columns import Columns


class ClientView:
    def __init__(self):
        pass

    def logclients(self, user, clients):
        console = Console()
        console.rule("Entreprises")
        console.print("")

        mycompany = []
        Withousalesman = []
        othersclient = []
        liste_choix = []
        liste_interdit = []
        liste_sans_choix = []

        for company in clients:
            if company.user_id == user.id:
                mycompany.append(company)
                liste_choix.append(company.id)
            elif company.user_id is None:
                Withousalesman.append(company)
                liste_sans_choix.append(company.id)
            elif company.user_id != user.id:
                othersclient.append(company)
                liste_interdit.append(company.id)

        def create_table(liste, car):
            if car == "MY":
                table = Table(title="Mes entreprises", box=None)
            elif car == "OT":
                table = Table(title="Autres entreprises", box=None)
            elif car == "NO":
                table = Table(title="Entreprises sans commercial", box=None)
            if car == "MY":
                table.add_column("Id", justify="center",
                                 style="green", no_wrap=True)
            else:
                table.add_column("Id", justify="center",
                                 style="#FFA500", no_wrap=True)
            table.add_column("Nom de l'entreprise",
                             justify="left", style="white")
            table.add_column("Date de mise à jour",
                             justify="left", style="white")
            table.add_row("", "")
            for company in liste:
                table.add_row(str(company.id), company.company_name,
                              company.update_date.strftime(
                                  "%Y-%m-%d %H:%M:%S"))
            return table

        table1 = create_table(mycompany, "MY")
        table2 = create_table(othersclient, "OT")
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
            tablechoix.add_row("CR", "Créer une nouvelle entreprise")
            tablechoix.add_row("A<id>", "Afficher les contacts"
                               " d'une entreprise <id>")
            tablechoix.add_row("M<id>", "Modifier les informations"
                               " d'une entreprise <id>")
            tablechoix.add_row("S<id>", "[blue]Suprimer "
                               "définitivement [/blue]l'entreprise <id>")
        else:
            tablechoix.add_row("[red][strike]CR[/red][/strike]",
                               "[red]Créer une nouvelle entreprise[/red]🔒")
            tablechoix.add_row("A<id>", "Afficher les contacts"
                               " d'une entreprise <id>")
            tablechoix.add_row("[red][strike]M<id>[/red][/strike]",
                               "[red]Modifier les informations d'une "
                               "entreprise <id>[/red]🔒")
            tablechoix.add_row("[red][strike]S<id>[/red][/strike]",
                               "[red]Suprimer définitivement "
                               "l'entreprise <id>[/red]🔒")
        tablechoix.add_row("RET", "Retour au menu précédent")
        tablechoix.add_row("QUIT", "Quitter l'application")
        console.print("")
        console.print(tablechoix)
        console.print("")
        if user.authorisation('Sale'):
            valid_choices = ["CR", "RET", "QUIT"]
        else:
            valid_choices = ["RET", "QUIT"]
        invalid_choices = []
        console.print("")

        for element in liste_choix:
            valid_choices.append(f"A{element}")
            valid_choices.append(f"M{element}")
            valid_choices.append(f"S{element}")
        for element in liste_interdit:
            valid_choices.append(f"A{element}")
            invalid_choices.append(f"M{element}")
            invalid_choices.append(f"S{element}")
        for element in liste_sans_choix:
            valid_choices.append(f"A{element}")
            invalid_choices.append(f"M{element}")
            invalid_choices.append(f"S{element}")

        while True:
            console.print("Votre choix [#AAAAAA]( CR, A18,"
                          " D9 ...)[/#AAAAAA] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            elif choix in invalid_choices:
                console.print("[red]Ce n'est pas une de "
                              "vos entreprises.[/red]")
            else:
                console.print("[red]Choix invalide. "
                              "Veuillez essayer à nouveau.[/red]")

    def createcompany(self, user):
        if user.authorisation('Sale'):
            choix = None
            while choix != 'Oui':
                console = Console()
                console.rule("Création d'une nouvelle société ")
                console.print("")
                console.print("[green] Le nom de la société [/green]")
                nom = str(input('==>'))
                console.print("[green] Adresse de la société [/green]")
                adress = str(input('==>'))

                console.rule("Résumé de votre saisie pour confirmation")
                console.print("")
                tableconfirmation = Table(box=None)
                tableconfirmation.add_column("Type", justify="left",
                                            style="green", no_wrap=True)
                tableconfirmation.add_column("Vos saisies", justify="left",
                                            style="white")
                tableconfirmation.add_row("", "")
                tableconfirmation.add_row("Nom", f"{nom}")
                tableconfirmation.add_row("Adresse", f"{adress}")
                tableconfirmation.add_row("Gestionnaire", "Vous")
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
                            return nom, adress
                        else:
                            break
                    else:
                        console.print("[red]Choix invalide. "
                                    "Veuillez essayer à nouveau.[/red]")

    def totalViewCompagny(self, user, company, contacts):
        console = Console()
        console.rule(f"Détail complet de l'entreprise {company.company_name}")
        console.print("")
        contact_id = []

        def create_table(liste, car):
            if car == "Données entreprise":
                table = Table(title=f"{car}", box=None)
                table.add_column("Type", justify="left",
                                 style="green", no_wrap=True)
                table.add_column("Donnée", justify="left", style="white")
                table.add_row("", "")
                table.add_row("Id de l'entreprise", f"{liste.id}")
                table.add_row("Nom de l'entreprise", f"{liste.company_name}")
                table.add_row("Adresse de l'entreprise", f"{liste.address}")
                table.add_row("Date de mise à jour de l'entreprise",
                              f"{liste.update_date.strftime(
                                  "%Y-%m-%d %H:%M:%S")}")
                return table
            elif car == "Contacts":
                table = Table(title=f"{car} de l'entreprise", box=None)
                table.add_column("Id", justify="center", style="green",
                                 no_wrap=True)
                table.add_column("Nom", justify="left", style="white")
                table.add_column("Email", justify="left", style="white")
                table.add_column("Téléphone", justify="left", style="white")
                table.add_column("Signataire", justify="left", style="white")
                table.add_column("Date de mise à jour", justify="left",
                                 style="white")
                table.add_row("", "")
                for element in liste:
                    table.add_row(str(element.id), element.name, element.email,
                                  element.phone, str(element.signatory),
                                  element.update_date.strftime(
                                      "%Y-%m-%d %H:%M:%S"))
                    contact_id.append(element.id)
                return table

        table1 = create_table(company, "Données entreprise")
        table2 = create_table(contacts, "Contacts")
        vertical_line = Text("\n".join("|" for _ in range(7)), style="green")

        console.print(Columns([table1, vertical_line, table2], padding=(0, 5)))
        console.print("")
        console.print("-" * console.width)
        centered_text = Text("Choix d'actions", style="bold green")
        console.print(Align.center(centered_text))

        tablechoix = Table(box=None)
        tablechoix.add_column("Choix", justify="left", style="green",
                              no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")

        tablechoix.add_row("", "")
        if company.user_id == user.id and user.authorisation('Sale'):
            tablechoix.add_row("CR", "Créer un nouveau contact")
            tablechoix.add_row("A<id>", "Afficher le "
                               "contact <id> de l'entreprise")
            tablechoix.add_row("MN <Nouvelle donnée>", "Modifier le nom"
                               " de l'entreprise par <Nouvelle donnée>")
            tablechoix.add_row("MA <Nouvelle donnée>", "Modifier l'adresse "
                               "de l'entreprise par <Nouvelle donnée>")
            tablechoix.add_row("SUPPRIMER", "[blue]Supprimer définitivement"
                               "[/blue] l'entreprise et ses contacts")
            tablechoix.add_row("RET", "Retour au menu précédent")
            tablechoix.add_row("QUIT", "Quitter le programme")
            console.print("")
        else:
            tablechoix.add_row("[red][strike]CR[/red][/strike]", "[red]Créer "
                               "un nouveau contact[/red]")
            if company.user_id is None and user.authorisation('Sale'):
                tablechoix.add_row("RECUPERER", "Récupérer le dossier "
                                   "de l'entreprise")
            tablechoix.add_row("A<id>", "Afficher le contact <id> de"
                               " l'entreprise")
            tablechoix.add_row("[red][strike]MN <Nouvelle "
                               "donnée>[/red][/strike]", "[red]Modifier le "
                               "nom de l'entreprise par "
                               "<Nouvelle donnée>[/red]🔒")
            tablechoix.add_row("[red][strike]MA <Nouvelle donnée>[/red]"
                               "[/strike]", "[red]Modifier l'adresse de "
                               "l'entreprise par <Nouvelle donnée>[/red]🔒")
            tablechoix.add_row("[red][strike]SUPPRIMER[/red][/strike]",
                               "[red]Suprimer définitivement l'entreprise "
                               "et ses contacts[/red]🔒")
            tablechoix.add_row("RET", "Retour au menu précédent")
            tablechoix.add_row("QUIT", "Quitter le programme")
            console.print("")

        console.print(tablechoix)
        console.print("")
        if company.user_id == user.id and user.authorisation('Sale'):
            valid_choices = ["CR", "RET", "QUIT", "SUPPRIMER"]
            invalid_choices = []
            valid_choices_with_id = ["MN", "MA"]
        elif company.user_id is None:
            valid_choices = ["RET", "QUIT", "RECUPERER"]
            invalid_choices = ["CR", "SUPPRIMER"]
            valid_choices_with_id = []
        else:
            valid_choices = ["RET", "QUIT"]
            invalid_choices = ["CR", "SUPPRIMER"]
            valid_choices_with_id = []

        console.print("")

        if company.user_id == user.id:
            for element in contact_id:
                valid_choices.append(f"A{element}")
        else:
            for element in contact_id:
                valid_choices.append(f"A{element}")

        while True:
            console.print("Votre choix [grey]( CR, A18, D9 ...)[/grey] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            elif any(choix.startswith(c) for c in valid_choices_with_id):
                return choix
            elif choix in invalid_choices:
                console.print("[red]Ce n'est pas une de vos "
                              "entreprises.[/red]")
            else:
                console.print("[red]Choix invalide. Veuillez essayer "
                              "à nouveau.[/red]")

    def createcontact(self, company, user):
        if company.user_id == user.id:
            choix = None
            while choix != 'Oui':
                console = Console()
                console.rule("Création d'un nouveau contact ")
                console.print("")
                console.print("[green] Le nom du contact [/green]")
                name = str(input('==>'))
                console.print("[green] L'email du contact [/green]")
                email = str(input('==>'))
                console.print("[green] Le numéro de téléphone du contact [/green]")
                phone = str(input('==>'))
                console.print("[green] Le contact est il le principal "
                            "signataire ? (Oui / Non)[/green]")
                valid_role = ["Oui", "Non"]
                role = None
                while role not in valid_role:
                    role = input('==>')
                    if role == "Oui":
                        signatory = True
                    elif role == "Non":
                        signatory = False
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
                tableconfirmation.add_row("Nom", f"{name}")
                tableconfirmation.add_row("Email", f"{email}")
                tableconfirmation.add_row("Telephone", f"{phone}")
                tableconfirmation.add_row("Signataire", f"{role}")
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
                            return name, email, phone, signatory
                        else:
                            break
                    else:
                        console.print("[red]Choix invalide. Veuillez "
                                    "essayer à nouveau.[/red]")

    def detailedContact(self, contact, company):
        console = Console()
        console.rule(f"Données du {contact.name} de l'entreprise"
                     f" : {company.company_name} ")
        console.print("")
        tabledonneessolo = Table(box=None)
        tabledonneessolo.add_column("Type", justify="left",
                                    style="green", no_wrap=True)
        tabledonneessolo.add_column("Information", justify="left",
                                    style="white")
        tabledonneessolo.add_row("", "")
        tabledonneessolo.add_row("Id", f"{contact.id}")
        tabledonneessolo.add_row("Nom", f"{contact.name}")
        tabledonneessolo.add_row("Email", f"{contact.email}")
        tabledonneessolo.add_row("Téléphone", f"{contact.phone}")
        if contact.signatory:
            role = "Oui"
        else:
            role = "Non"
        tabledonneessolo.add_row("Signataire", f"{role}")
        tabledonneessolo.add_row("Date de création",
                                 f"{contact.creation_date}")
        tabledonneessolo.add_row("Date de modification",
                                 f"{contact.update_date}")
        console.print(tabledonneessolo)

        console.print("")
        console.print("-" * console.width)
        centered_text = Text("Choix d'actions", style="bold green")
        console.print(Align.center(centered_text))
        tablechoix = Table(box=None)
        tablechoix.add_column("Choix", justify="left",
                              style="green", no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")
        tablechoix.add_row("", "")
        tablechoix.add_row("NO <Nouvelle Donnée>", "Modifier le nom "
                           "du contact par <Nouvelle Donnée>")
        tablechoix.add_row("EM <Nouvelle Donnée>", "Modifier l'Email "
                           "du contact par <Nouvelle Donnée>")
        tablechoix.add_row("TE <Nouvelle Donnée>", "Modifier le téléphone "
                           "du contact par <Nouvelle Donnée>")
        tablechoix.add_row("SI <Oui/Non>", "Modifier le role du contact "
                           "par : Oui = Signataire, Non = Non signataire")
        tablechoix.add_row("SUPPRIMER", "[blue]Supprime définitivement"
                           "[/blue] l'utilisateur de la base de donnée")
        tablechoix.add_row("RET", "Retour au menu précédent")
        tablechoix.add_row("QUIT", "quitter l'application")
        console.print("")
        console.print(tablechoix)
        console.print("")
        valid_choices = ["CR", "SUPPRIMER", "RET", "QUIT",
                         "SI Oui", "SI Non"]
        valid_choices_with_id = ["NO", "EM", "TE"]
        console.print("")
        while True:
            console.print("Votre choix [#AAAAAA]( SI Non, NO Eric,"
                          " EM martin@tot.fr ...)[/#AAAAAA] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            elif any(choix.startswith(c) for c in valid_choices_with_id):
                return choix
            else:
                console.print("[red]Choix invalide. "
                              "Veuillez essayer à nouveau.[/red]")

    def LiteViewCompagny(self, user, company, contacts):
        console = Console()
        console.rule(f"Récapitulatif de l'entreprise {company.company_name}")
        console.print("")

        contact_id = []

        def create_table(liste, car):
            if car == "Données entreprise":
                table = Table(title=f"{car}", box=None)
                table.add_column("Type", justify="left",
                                 style="green", no_wrap=True)
                table.add_column("Donnée", justify="left", style="white")
                table.add_row("", "")
                table.add_row("Id de l'entreprise", f"{liste.id}")
                table.add_row("Nom de l'entreprise", f"{liste.company_name}")
                table.add_row("Adresse de l'entreprise", f"{liste.address}")
                table.add_row("Date de mise à jour de l'entreprise",
                              f"{liste.update_date.strftime(
                                  "%Y-%m-%d %H:%M:%S")}")
                return table
            elif car == "Contacts":
                table = Table(title=f"{car} de l'entreprise", box=None)
                table.add_column("Id", justify="center", style="green",
                                 no_wrap=True)
                table.add_column("Nom", justify="left", style="white")
                table.add_column("Email", justify="left", style="white")
                table.add_column("Téléphone", justify="left", style="white")
                table.add_column("Signataire", justify="left", style="white")
                table.add_column("Date de mise à jour", justify="left",
                                 style="white")
                table.add_row("", "")
                for element in liste:
                    table.add_row(str(element.id), element.name,
                                  element.email, element.phone,
                                  str(element.signatory),
                                  element.update_date.strftime(
                                      "%Y-%m-%d %H:%M:%S"))
                    contact_id.append(element.id)
                return table

        table1 = create_table(company, "Données entreprise")
        table2 = create_table(contacts, "Contacts")
        vertical_line = Text("\n".join("|" for _ in range(7)), style="green")

        console.print(Columns([table1, vertical_line, table2], padding=(0, 5)))
        console.print("")
        console.print("-" * console.width)
        centered_text = Text("Choix d'actions", style="bold green")
        console.print(Align.center(centered_text))

        tablechoix = Table(box=None)
        tablechoix.add_column("Choix", justify="left", style="green",
                              no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")

        tablechoix.add_row("", "")
        tablechoix.add_row("RET", "Retour au menu précédent")
        tablechoix.add_row("QUIT", "Quitter le programme")
        console.print("")

        valid_choices = ["RET", "QUIT"]
        console.print(tablechoix)
        console.print("")

        while True:
            console.print("Votre choix [#AAAAAA]( "
                          "RET, QUIT ...)[/#AAAAAA] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            else:
                console.print("[red]Choix invalide. "
                              "Veuillez essayer à nouveau.[/red]")
