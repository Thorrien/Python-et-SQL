from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.layout import Layout
from rich.text import Text
from rich.table import Table
from datetime import datetime
from time import sleep
from rich.columns import Columns


class View :
    def __init__(self):
        pass
    
    def ascii(self):
        rprint("[bold green]      ___           ___                     ___           ___                        ___           ___                 [/bold green]")
        rprint("[bold green]     /  /\         /  /\      ___          /  /\         /  /\          ___         /  /\         /__/\          ___   [/bold green]")
        rprint("[bold green]    /  /:/_       /  /::\    /  /\        /  /:/        /  /:/_        /__/\       /  /:/_        \  \:\        /  /\  [/bold green]")
        rprint("[bold green]   /  /:/ /\     /  /:/\:\  /  /:/       /  /:/        /  /:/ /\       \  \:\     /  /:/ /\        \  \:\      /  /:/  [/bold green]")
        rprint("[bold green]  /  /:/ /:/_   /  /:/~/:/ /__/::\      /  /:/  ___   /  /:/ /:/_       \  \:\   /  /:/ /:/_   _____\__\:\    /  /:/   [/bold green]")
        rprint("[bold green] /__/:/ /:/ /\ /__/:/ /:/  \__\/\:\__  /__/:/  /  /\ /__/:/ /:/ /\  ___  \__\:\ /__/:/ /:/ /\ /__/::::::::\  /  /::\   [/bold green]")
        rprint("[bold green] \  \:\/:/ /:/ \  \:\/:/      \  \:\/\ \  \:\ /  /:/ \  \:\/:/ /:/ /__/\ |  |:| \  \:\/:/ /:/ \  \:\~~\~~\/ /__/:/\:\  [/bold green]")
        rprint("[bold green]  \  \::/ /:/   \  \::/        \__\::/  \  \:\  /:/   \  \::/ /:/  \  \:\|  |:|  \  \::/ /:/   \  \:\  ~~~  \__\/  \:\ [/bold green]")
        rprint("[bold green]   \  \:\/:/     \  \:\        /__/:/    \  \:\/:/     \  \:\/:/    \  \:\__|:|   \  \:\/:/     \  \:\           \  \:\ [/bold green]")
        rprint("[bold green]    \  \::/       \  \:\       \__\/      \  \::/       \  \::/      \__\::::/     \  \::/       \  \:\           \__\/[/bold green]")
        rprint("[bold green]     \__\/         \__\/                   \__\/         \__\/           ~~~~       \__\/         \__\/                [/bold green]")
        print("")
        print("")
        print("")
        
    def login(self):
       pass
   
    def title(self, user):
        console = Console()
        title_text = Text("EpicEvent", style="bold white on green", justify="center")
        title_panel = Panel(Align.center(title_text), style="bold")
        console.print(title_panel)
        current_date = datetime.now().strftime("%d/%m/%Y")
        current_time = datetime.now().strftime("%H:%M:%S")
        first_line = f"id : 12564{' ' * (console.width - len('id : 12564') - len(current_date))}{current_date}"
        console.print(first_line)
        second_line = f"[bold green]{user.email}[/bold green]{' ' * (console.width - len(user.email) - len(current_time))}{current_time}"
        console.print(second_line)

    
    def logtrue(self, user):
        self.title(user)
        console = Console()
        console.rule(f"Bienvenue {user.nom}")
        console.print("")
        console.print("Message de la direction : Nous vous informons que le pot de départ de M. Chauvin aura lieu le 19 septembre 2024 en salle 25A. À cette occasion, la direction présentera son successeur, M. Martin. Nous comptons sur votre présence pour partager ce moment convivial.")
        console.print("")
        sleep(3)
        
    def logcontrats(self, user):
        self.title(user)
        console = Console()
        console.rule("Gestion des contrats")
        console.print("")
        console.print("")

    def menuprincipalgestion(self, user):
        console = Console()
        console.rule("Menu principal")
        console.print("")
        table = Table(box=None)
        table.add_column("Choix", justify="center", style="green", no_wrap=True)
        table.add_column("Description", justify="left", style="white")
        
        table.add_row("", "")
        if user.authorisation('Admin') or user.authorisation('Gestion'):
            table.add_row("US", "Gérer les comptes utilisateurs")
        else:
            table.add_row("[red][strike]US[/strike][/red]", "[red]Gérer les comptes utilisateurs[/red]🔒")
        if user.authorisation('Admin') or user.authorisation('Gestion') or user.authorisation('Sale') or user.authorisation('Support'):
            table.add_row("CL", "Gérer les clients")
        else:
            table.add_row("[red][strike]CL[/red][/strike]", "[red]Gérer les clients[/red]🔒")
        if user.authorisation('Admin') or user.authorisation('Gestion') or user.authorisation('Sale') or user.authorisation('Support'):
            table.add_row("CO", "Gérer les contrats")
        else:
            table.add_row("[red][strike]CO[/red][/strike]", "[red]Gérer les contrats[/red]🔒")
        if user.authorisation('Admin') or user.authorisation('Gestion') or user.authorisation('Sale') or user.authorisation('Support'):
            table.add_row("EV", "Gérer les Events")
        else:
            table.add_row("[red][strike]EV[/red][/strike]", "[red]Gérer les Events[/red]🔒")
        if  user.authorisation('Gestion'):
            table.add_row("MO", "Modifier le message d'accueil")
        else:
            table.add_row("[red][strike]MO[/strike][/red]", "[red]Modifier le message d'accueil[/red]🔒")
        table.add_row("QUIT", "Quitter")
        console.print(table)
        valid_choix = ["US", "CO", "EV", "CL", "MO", "QUIT"]
        while True:
            choix = input('Votre choix : ')
            if choix in valid_choix:
                return choix
            else:
                console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")
    
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
            table.add_column("Id", justify="center", style="green", no_wrap=True)
            table.add_column("Nom", justify="left", style="white")
            table.add_column("Role", justify="left", style="white")
            table.add_row("", "")
            for usersolo in users:
                table.add_row(str(usersolo['user_id']), usersolo['user_name'], usersolo['role_name'])
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
        tablechoix.add_column("Choix", justify="center", style="green", no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")
        
        tablechoix.add_row("", "")
        tablechoix.add_row("CR", "Créer un nouvel utilisateur")
        tablechoix.add_row("A<id>", "Afficher le détail d'un utilisateur <id>")
        tablechoix.add_row("M<id>", "Modifier un élément d'un utilisateur <id>")
        tablechoix.add_row("S<id>", "[orange] Suprimer définitivement [/orange] l'utilisateur <id>")
        tablechoix.add_row("RET", "Retour au menu principal")
        console.print("")
        console.print(tablechoix)
        console.print("")
        valid_choices = ["CR", "RET"]
        console.print("")
        for element in liste_choix:
            valid_choices.append(f"A{element}")
            valid_choices.append(f"M{element}")
            valid_choices.append(f"S{element}")
        
        while True:
            console.print("Votre choix [grey]( CR, A18, D9 ...)[/grey] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            else:
                console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")

    def soloUserView(self, user, affiche):
        console = Console()
        console.rule(f"Données de l'utilisateur {affiche.nom} ")
        console.print("")
        tabledonneessolo = Table(box=None)
        tabledonneessolo.add_column("Type", justify="left", style="green", no_wrap=True)
        tabledonneessolo.add_column("Information", justify="left", style="white")
        tabledonneessolo.add_row("", "")
        tabledonneessolo.add_row("Id", f"{affiche.id}")
        tabledonneessolo.add_row("Nom", f"{affiche.nom}")
        tabledonneessolo.add_row("Email", f"{affiche.email}")
        tabledonneessolo.add_row("Service", f"{affiche.role_id}")
        tabledonneessolo.add_row("Date de création", f"{affiche.date_creation}")
        console.print(tabledonneessolo)
        
        console.print("")
        console.print("-" * console.width)
        centered_text = Text("Choix d'actions", style="bold green")
        console.print(Align.center(centered_text))
        tablechoix = Table(box=None)
        tablechoix.add_column("Choix", justify="left", style="green", no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")
        tablechoix.add_row("", "")
        tablechoix.add_row("NO <Nouvelle Donnée>", "Modifier le nom de l'utilisateur par <Nouvelle Donnée>")
        tablechoix.add_row("EM <Nouvelle Donnée>", "Modifier l'Email de l'utilisateur par <Nouvelle Donnée>")
        tablechoix.add_row("RE <Nouvelle Donnée>", "Modifier le mot de passe de l'utilisateur par <Nouvelle Donnée>")
        tablechoix.add_row("SE <AD/VE/GE/SU>", "Modifier le Service de l'utilisateur par AD = Admin, VE = Ventes, GE = Gestion et SU = Support")
        tablechoix.add_row("SUPPRIMER", "[blue]Supprime définitivement[/blue] l'utilisateur de la base de donnée")
        tablechoix.add_row("LIST", "Retour à la liste des utilisateurs")
        tablechoix.add_row("RET", "Retour au menu principal")
        tablechoix.add_row("QUIT", "quitter l'application")
        console.print("")
        console.print(tablechoix)
        console.print("")
        valid_choices = ["CR", "SUPPRIMER", "LIST", "RET", "QUIT", "SE AD", "SE SU", "SE VE", "SE GE"]
        valid_choices_with_id = ["NO", "EM", "RE"]
        console.print("")
        while True:
            console.print("Votre choix [grey]( SE AD, NO Eric, EM martin@tot.fr ...)[/grey] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            elif any(choix.startswith(c) for c in valid_choices_with_id):
                return choix
            else:
                console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")

    def notautorized(self, user):
        console = Console()
        console.rule(f"[red] {user.nom}, vous n'avez pas les droits permettant d'utiliser cette fonctionnalité[/red]")
        sleep(2)

    def base(self):
        console = Console()
        console.rule("Fin de la page")
        
    def createuserview(self):
        console = Console()
        console.rule(f"Création d'un nouvel utilisateur ")
        console.print("")
        console.print("[green] Le nom de l'utilisateur [/green]")
        nom = str(input('==>'))
        console.print("[green] L'Email de l'utilisateur [/green]")
        email = str(input('==>'))
        console.print("[green] Le Mot de passe de l'utilisateur [/green]")
        mot_de_passe = str(input('==>'))
        console.print("[green] Le service de l'utilisateur : 1 (Admin), 2 (Gestion), 3 (Vente), 4 (Support) [/green]")
        role = None
        valid_role = ["1", "2", "3", "4"]
        while True:
            role = input('==>')
            if role in valid_role:
                break
            else:
                console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")

        console.rule(f"Résumé de votre saisie pour confirmation")
        console.print("")
        tableconfirmation = Table(box=None)
        tableconfirmation.add_column("Type", justify="left", style="green", no_wrap=True)
        tableconfirmation.add_column("Vos saisies", justify="left", style="white")
        tableconfirmation.add_row("", "")
        tableconfirmation.add_row("Nom", f"{nom}")
        tableconfirmation.add_row("Email", f"{email}")
        tableconfirmation.add_row("Mot de passe", f"{mot_de_passe}")
        tableconfirmation.add_row("Service", f"{role}")
        console.print(tableconfirmation)

        console.print("")
        console.print("-" * console.width)
        centered_text = Text("Confirmez vous votre saisie ?", style="bold green")
        console.print(Align.center(centered_text))
        
        console.print("[green] Oui ou Non [/green]")
        valid_role = ["Oui", "Non"]
        while True:
            choix = input('==>')
            if choix == "Oui":
                return nom, email, mot_de_passe, role
            else:
                break
            
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
                table.add_column("Id", justify="center", style="green", no_wrap=True)
            else:
                table.add_column("Id", justify="center", style="#FFA500", no_wrap=True)
            table.add_column("Nom de l'entreprise", justify="left", style="white")
            table.add_column("Date de mise à jour", justify="left", style="white")
            table.add_row("", "")
            for company in liste:
                table.add_row(str(company.id), company.company_name, company.update_date.strftime("%Y-%m-%d %H:%M:%S"))
            
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
        tablechoix.add_column("Choix", justify="center", style="green", no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")
        
        tablechoix.add_row("", "")
        if user.authorisation('Sale'):
            tablechoix.add_row("CR", "Créer une nouvelle entreprise")
            tablechoix.add_row("A<id>", "Afficher les contacts d'une entreprise <id>")
            tablechoix.add_row("M<id>", "Modifier les informations d'une entreprise <id>")
            tablechoix.add_row("S<id>", "[blue]Suprimer définitivement [/blue]l'entreprise <id>")
        else: 
            tablechoix.add_row("[red][strike]CR[/red][/strike]", "[red]Créer une nouvelle entreprise[/red]")
            tablechoix.add_row("A<id>", "Afficher les contacts d'une entreprise <id>")
            tablechoix.add_row("[red][strike]M<id>[/red][/strike]", "[red]Modifier les informations d'une entreprise <id>[/red]")
            tablechoix.add_row("[red][strike]S<id>[/red][/strike]", "[red]Suprimer définitivement l'entreprise <id>[/red]")
        tablechoix.add_row("RET", "Retour au menu principal")
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
            console.print("Votre choix [grey]( CR, A18, D9 ...)[/grey] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            elif choix in invalid_choices:
                console.print("[red]Ce n'est pas une de vos entreprises.[/red]")
            else:
                console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")

    def createcompany(self, user):
        if user.authorisation('Sale'):
            console = Console()
            console.rule(f"Création d'une nouvelle société ")
            console.print("")
            console.print("[green] Le nom de la société [/green]")
            nom = str(input('==>'))

            console.rule(f"Résumé de votre saisie pour confirmation")
            console.print("")
            tableconfirmation = Table(box=None)
            tableconfirmation.add_column("Type", justify="left", style="green", no_wrap=True)
            tableconfirmation.add_column("Vos saisies", justify="left", style="white")
            tableconfirmation.add_row("", "")
            tableconfirmation.add_row("Nom", f"{nom}")
            tableconfirmation.add_row("Gestionnaire", "Vous")
            console.print(tableconfirmation)

            console.print("")
            console.print("-" * console.width)
            centered_text = Text("Confirmez vous votre saisie ?", style="bold green")
            console.print(Align.center(centered_text))
            
            console.print("[green] Oui ou Non [/green]")
            valid_role = ["Oui", "Non"]
            while True:
                choix = input('==>')
                if choix in valid_role:
                    if choix == "Oui":
                        return nom
                    else:
                        break
                else:
                    console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")
                
    def totalViewCompagny(self, user, company, contacts, contrats, events):
        console = Console()
        console.rule(f"Détail complet de l'entreprise {company.company_name}")
        console.print("") 

        contact_id = []
        
        def create_table(liste, car):
            if car == "Données entreprise":
                table = Table(title=f"{car}", box=None)
                table.add_column("Type", justify="left", style="green", no_wrap=True)
                table.add_column("Donnée", justify="left", style="white")
                table.add_row("", "")
                table.add_row("Id de l'entreprise", f"{liste.id}")
                table.add_row("Nom de l'entreprise", f"{liste.company_name}")
                table.add_row("Adresse de l'entreprise", f"{liste.address}")
                table.add_row("Date de mise à jour de l'entreprise", f"{liste.update_date.strftime("%Y-%m-%d %H:%M:%S")}")
                return table
            elif car == "Contacts":
                table = Table(title=f"{car} de l'entreprise", box=None)
                table.add_column("Id", justify="center", style="green", no_wrap=True)
                table.add_column("Nom", justify="left", style="white")
                table.add_column("Email", justify="left", style="white")
                table.add_column("Téléphone", justify="left", style="white")
                table.add_column("Signataire", justify="left", style="white")
                table.add_column("Date de mise à jour", justify="left", style="white")
                table.add_row("", "")
                for element in liste:
                    table.add_row(str(element.id), element.name, element.email, element.phone, str(element.signatory), element.update_date.strftime("%Y-%m-%d %H:%M:%S"))
                    contact_id.append(element.id)
                return table
            elif car == "Contrats":
                table = Table(title=f"{car} de l'entreprise", box=None)
                return table
            elif car == "Evènements":
                table = Table(title=f"{car} de l'entreprise", box=None)
                return table

        table1 = create_table(company, "Données entreprise")
        table2 = create_table(contacts, "Contacts")
        table3 = create_table(contrats, "Contrats")
        table4 = create_table(events, "Evènements")
        
        vertical_line = Text("\n".join("|" for _ in range(7)), style="green")
        
        console.print(Columns([table1, vertical_line, table2, table3, table4], padding=(0, 5)))
        console.print("")
        console.print("-" * console.width)
        centered_text = Text("Choix d'actions", style="bold green")
        console.print(Align.center(centered_text))
        
        tablechoix = Table(box=None)
        tablechoix.add_column("Choix", justify="left", style="green", no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")
        
        tablechoix.add_row("", "")
        if company.user_id == user.id and user.authorisation('Sale'):
            tablechoix.add_row("CR", "Créer un nouveau contact")
            tablechoix.add_row("A<id>", "Afficher le contact <id> de l'entreprise")
            tablechoix.add_row("MN <Nouvelle donnée>", "Modifier le nom de l'entreprise par <Nouvelle donnée>")
            tablechoix.add_row("MA <Nouvelle donnée>", "Modifier l'adresse de l'entreprise par <Nouvelle donnée>")
            tablechoix.add_row("SUPPRIMER", "[blue]Supprimer définitivement[/blue] l'entreprise et ses contacts")
            tablechoix.add_row("RET", "Retour au menu principal")
            tablechoix.add_row("QUIT", "Quitter le programme")
            console.print("")
        else:
            tablechoix.add_row("[red][strike]CR[/red][/strike]", "[red]Créer un nouveau contact[/red]")
            if company.user_id is None: 
                tablechoix.add_row("RECUPERER", "Récupérer le dossier de l'entreprise")
            tablechoix.add_row("A<id>", "Afficher le contact <id> de l'entreprise")
            tablechoix.add_row("[red][strike]MN <Nouvelle donnée>[/red][/strike]", "[red]Modifier le nom de l'entreprise par <Nouvelle donnée>[/red]")
            tablechoix.add_row("[red][strike]MA <Nouvelle donnée>[/red][/strike]", "[red]Modifier l'adresse de l'entreprise par <Nouvelle donnée>[/red]")
            tablechoix.add_row("[red][strike]SUPPRIMER[/red][/strike]", "[red]Suprimer définitivement l'entreprise et ses contacts[/red]")
            tablechoix.add_row("RET", "Retour au menu principal")
            tablechoix.add_row("QUIT", "Quitter le programme")
            console.print("") 
        
        console.print(tablechoix)
        console.print("")
        if company.user_id == user.id and user.authorisation('Sale') :
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
        
        if company.user_id == user.id :
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
                console.print("[red]Ce n'est pas une de vos entreprises.[/red]")
            else:
                console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")


        
    def createcontact(self, company, user):
        if company.user_id == user.id :
            console = Console()
            console.rule(f"Création d'un nouveau contact ")
            console.print("")
            console.print("[green] Le nom du contact [/green]")
            name = str(input('==>'))
            console.print("[green] L'email du contact [/green]")
            email = str(input('==>'))
            console.print("[green] Le numéro de téléphone du contact [/green]")
            phone = str(input('==>'))
            console.print("[green] Le contact est il le principal signataire ? (Oui / Non)[/green]")
            valid_role = ["Oui", "Non"]
            role = None
            while role not in valid_role:
                role = input('==>')
                if role == "Oui":
                    signatory = True
                elif role == "Non":
                    signatory = False
                else:
                    console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")

            console.rule(f"Résumé de votre saisie pour confirmation")
            console.print("")
            tableconfirmation = Table(box=None)
            tableconfirmation.add_column("Type", justify="left", style="green", no_wrap=True)
            tableconfirmation.add_column("Vos saisies", justify="left", style="white")
            tableconfirmation.add_row("", "")
            tableconfirmation.add_row("Nom", f"{name}")
            tableconfirmation.add_row("Email", f"{email}")
            tableconfirmation.add_row("Telephone", f"{phone}")
            tableconfirmation.add_row("Signataire", f"{role}")
            console.print(tableconfirmation)

            console.print("")
            console.print("-" * console.width)
            centered_text = Text("Confirmez vous votre saisie ?", style="bold green")
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
                    console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")
                
    def detailedContact(self, contact, company):
        console = Console()
        console.rule(f"Données du {contact.name} de l'entreprise : {company.company_name} ")
        console.print("")
        tabledonneessolo = Table(box=None)
        tabledonneessolo.add_column("Type", justify="left", style="green", no_wrap=True)
        tabledonneessolo.add_column("Information", justify="left", style="white")
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
        tabledonneessolo.add_row("Date de création", f"{contact.creation_date}")
        tabledonneessolo.add_row("Date de modification", f"{contact.update_date}")
        console.print(tabledonneessolo)
        
        console.print("")
        console.print("-" * console.width)
        centered_text = Text("Choix d'actions", style="bold green")
        console.print(Align.center(centered_text))
        tablechoix = Table(box=None)
        tablechoix.add_column("Choix", justify="left", style="green", no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")
        tablechoix.add_row("", "")
        tablechoix.add_row("NO <Nouvelle Donnée>", "Modifier le nom du contact par <Nouvelle Donnée>")
        tablechoix.add_row("EM <Nouvelle Donnée>", "Modifier l'Email du contact par <Nouvelle Donnée>")
        tablechoix.add_row("TE <Nouvelle Donnée>", "Modifier le téléphone du contact par <Nouvelle Donnée>")
        tablechoix.add_row("SI <Oui/Non>", "Modifier le role du contact par : Oui = Signataire, Non = Non signataire")
        tablechoix.add_row("SUPPRIMER", "[blue]Supprime définitivement[/blue] l'utilisateur de la base de donnée")
        tablechoix.add_row("ENTR", "Retour au détail de l'entreprise")
        tablechoix.add_row("RET", "Retour au menu principal")
        tablechoix.add_row("QUIT", "quitter l'application")
        console.print("")
        console.print(tablechoix)
        console.print("")
        valid_choices = ["CR", "SUPPRIMER", "ENTR", "RET", "QUIT", "SI Oui", "SI Non"]
        valid_choices_with_id = ["NO", "EM", "TE"]
        console.print("")
        while True:
            console.print("Votre choix [grey]( SI Non, NO Eric, EM martin@tot.fr ...)[/grey] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            elif any(choix.startswith(c) for c in valid_choices_with_id):
                return choix
            else:
                console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")