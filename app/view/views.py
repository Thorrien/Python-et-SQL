from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.layout import Layout
from rich.text import Text
from rich.table import Table
from datetime import datetime
from time import sleep
import re
from rich.columns import Columns
import calendar
import locale

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

    
    def logtrue(self, user, text):
        self.title(user)
        console = Console()
        console.rule(f"Bienvenue {user.nom}")
        console.print("")
        console.print(f"Message de la direction : {text}")
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
        if  user.authorisation('Gestion'):
            table.add_row("SU", "Gestion des éléments non attribués")
        else:
            table.add_row("[red][strike]SU[/strike][/red]", "[red]Gestion des éléments non attribués[/red]🔒")
        table.add_row("QUIT", "Quitter")
        console.print(table)
        if user.authorisation('Gestion') :
            invalid_choix = []
            valid_choix = ["US", "CO", "EV", "CL", "MO", "SU", "QUIT"]
        elif user.authorisation('Admin') :
            invalid_choix = [ "MO", "SU"]
            valid_choix = ["US", "CO", "EV", "CL", "QUIT"]
        else:
            invalid_choix = ["US", "MO", "SU"]
            valid_choix = ["CO", "EV", "CL", "QUIT"]
            
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
            console.print("Votre choix [#AAAAAA]( CR, A18, D9 ...)[/#AAAAAA] :")
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
            console.print("Votre choix [#AAAAAA]( SE AD, NO Eric, EM martin@tot.fr ...)[/#AAAAAA] :")
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
            tablechoix.add_row("[red][strike]CR[/red][/strike]", "[red]Créer une nouvelle entreprise[/red]🔒")
            tablechoix.add_row("A<id>", "Afficher les contacts d'une entreprise <id>")
            tablechoix.add_row("[red][strike]M<id>[/red][/strike]", "[red]Modifier les informations d'une entreprise <id>[/red]🔒")
            tablechoix.add_row("[red][strike]S<id>[/red][/strike]", "[red]Suprimer définitivement l'entreprise <id>[/red]🔒")
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
            console.print("Votre choix [#AAAAAA]( CR, A18, D9 ...)[/#AAAAAA] :")
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
                
    def totalViewCompagny(self, user, company, contacts):
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

        table1 = create_table(company, "Données entreprise")
        table2 = create_table(contacts, "Contacts")
        vertical_line = Text("\n".join("|" for _ in range(7)), style="green")
        
        console.print(Columns([table1, vertical_line, table2], padding=(0, 5)))
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
            if company.user_id is None and user.authorisation('Sale'): 
                tablechoix.add_row("RECUPERER", "Récupérer le dossier de l'entreprise")
            tablechoix.add_row("A<id>", "Afficher le contact <id> de l'entreprise")
            tablechoix.add_row("[red][strike]MN <Nouvelle donnée>[/red][/strike]", "[red]Modifier le nom de l'entreprise par <Nouvelle donnée>[/red]🔒")
            tablechoix.add_row("[red][strike]MA <Nouvelle donnée>[/red][/strike]", "[red]Modifier l'adresse de l'entreprise par <Nouvelle donnée>[/red]🔒")
            tablechoix.add_row("[red][strike]SUPPRIMER[/red][/strike]", "[red]Suprimer définitivement l'entreprise et ses contacts[/red]🔒")
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
            console.print("Votre choix [#AAAAAA]( SI Non, NO Eric, EM martin@tot.fr ...)[/#AAAAAA] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            elif any(choix.startswith(c) for c in valid_choices_with_id):
                return choix
            else:
                console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")

    def logcontracts( self, user, contrats, userDAO):
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
                table.add_column("Contrat", justify="center", style="green", no_wrap=True)
            else:
                table.add_column("Contrat", justify="center", style="#FFA500", no_wrap=True)
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
                table.add_row(f"{contrats.index(contrat)}", entreprise, Etat, Taux)
            
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
        tablechoix.add_column("Choix", justify="center", style="green", no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")
        
        tablechoix.add_row("", "")
        if user.authorisation('Sale'):
            tablechoix.add_row("CR<id>", "Créer un nouveau contrat pour la société <id>")
            tablechoix.add_row("A<id>", "Afficher le détail d'un contrat<id>")
            tablechoix.add_row("E<id>", "Afficher le détail d'une entreprise<id>")
            tablechoix.add_row("S<id>", "[blue]Suprimer définitivement [/blue]le contrat<id>")
        else: 
            tablechoix.add_row("[red][strike]CR<id>[/red][/strike]", "[red]Créer un nouveau contrat pour la société <id>[/red]🔒")
            tablechoix.add_row("A<id>", "Afficher le détail d'un contrat <id>")
            tablechoix.add_row("E<id>", "Afficher le détail d'une entreprise<id>")
            tablechoix.add_row("[red][strike]S<id>[/red][/strike]", "[red]Suprimer définitivement le contrat<id>[/red]🔒")
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
            console.print("Votre choix [#AAAAAA]( CR, A18, E9 ...)[/#AAAAAA] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            elif choix in invalid_choices:
                console.print("[red]Ce n'est pas une de vos entreprises.[/red]")
            else:
                console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")
                

    def createcontract(self, user, company):
        if company.user_id == user.id :
            console = Console()
            pattern = re.compile(r"^\d+(.\d{1,2})?$")
            console.rule(f"Création d'un nouveau contrat ")
            console.print("")
            
            while True:
                console.print("[green] Montant total du contrat (Sans le €) [/green]")
                total_amont = input('==>')
                if pattern.match(total_amont):
                    break
                else:
                    console.print("[red]Entrée invalide. Veuillez entrer uniquement des chiffres et un point.[/red]")

            while True:
                console.print("[green] Montant actuellement payé (Sans le €) [/green]")
                current_amont = input('==>')
                if pattern.match(current_amont):
                    break
                else:
                    console.print("[red]Entrée invalide. Veuillez entrer uniquement des chiffres et un point.[/red]")

            console.print("[green] Le contrat est il signé ? (Oui / Non)[/green]")
            valid_role = ["Oui", "Non"]
            role = None
            while role not in valid_role:
                role = input('==>')
                if role == "Oui":
                    sign = True
                elif role == "Non":
                    sign = False
                else:
                    console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")

            console.rule(f"Résumé de votre saisie pour confirmation")
            console.print("")
            tableconfirmation = Table(box=None)
            tableconfirmation.add_column("Type", justify="left", style="green", no_wrap=True)
            tableconfirmation.add_column("Vos saisies", justify="left", style="white")
            tableconfirmation.add_row("", "")
            tableconfirmation.add_row("Entreprise", f"{company.company_name}")
            tableconfirmation.add_row("Gestionnaire", "Vous")
            tableconfirmation.add_row("Montant total", f"{total_amont}")
            tableconfirmation.add_row("Montant actuel", f"{current_amont}")
            tableconfirmation.add_row("Contrat Signé", f"{role}")
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
                        return total_amont, current_amont, sign
                    else:
                        break
                else:
                    console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")

    def contractview(sel, user, company, contrat, events, userDAO):
        
        console = Console()
        console.rule(f"Détail complet du contrat {contrat.id} de l'entreprise {company.company_name}")
        console.print("") 

        events_id = []
        
        def create_table(liste, car):
            if car == "Données contrat":
                table = Table(title=f"{car}", box=None)
                table.add_column("Type", justify="left", style="green", no_wrap=True)
                table.add_column("Donnée", justify="left", style="white")
                table.add_row("", "")
                table.add_row("Entreprise", f"{company.company_name}")
                if user.id == company.user_id :
                    table.add_row("Gestionnaire", "Vous")
                else: 
                    table.add_row("Gestionnaire", f"{userDAO.get_user(contrat.user_id).nom}")
                table.add_row("Montant total", f"{contrat.total_amont} €")
                table.add_row("Montant versé", f"{contrat.current_amont} €")
                table.add_row("Date de création", f"{contrat.creation_date.strftime("%Y-%m-%d %H:%M:%S")}")
                table.add_row("Date de modification", f"{contrat.update_date.strftime("%Y-%m-%d %H:%M:%S")}")
                if contrat.sign : 
                    signe = "Oui"
                else: 
                    signe = "Non"
                table.add_row("Contrat signé", f"{signe}")
                return table
            elif car == "Evènements":
                table = Table(title=f"{car} de l'entreprise", box=None)
                table.add_column("Id", justify="center", style="green", no_wrap=True)
                table.add_column("Date de début", justify="left", style="white")
                table.add_column("Date de fin", justify="left", style="white")
                table.add_column("Localisation", justify="left", style="white")
                table.add_row("", "")
                for element in liste:
                    table.add_row(str(element.id), element.event_date_start.strftime('%Y-%m-%d %H:%M:%S'), element.event_date_end.strftime('%Y-%m-%d %H:%M:%S'), element.location)
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
        tablechoix.add_column("Choix", justify="left", style="green", no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")
        
        tablechoix.add_row("", "")
        if company.user_id == user.id and user.authorisation('Sale'):
            tablechoix.add_row("CR", "Créer un nouvel évènement")
            tablechoix.add_row("A<id>", "Afficher le détail de l'évènement <id>")
            tablechoix.add_row("MT <Nouvelle donnée>", "Modifier le montant total du contrat par <Nouvelle donnée>")
            tablechoix.add_row("MV <Nouvelle donnée>", "Modifier le montant versé du contrat par <Nouvelle donnée>")
            tablechoix.add_row("MS SI/NS", "Modifier l'état du contrat : SI = Signé / NS = Non Signé ")
            tablechoix.add_row("SUPPRIMER", "[blue]Supprimer définitivement[/blue] le contrat")
            tablechoix.add_row("RET", "Retour au menu principal")
            tablechoix.add_row("QUIT", "Quitter le programme")
            console.print("")
        else:
            tablechoix.add_row("[red][strike]CR[/red][/strike]", "[red]Créer un nouvel évènement[/red]🔒")
            tablechoix.add_row("A<id>", "Afficher le détail de l'évènement ")
            tablechoix.add_row("[red][strike]MT <Nouvelle donnée>[/red][/strike]", "[red]Modifier le montant total du contrat par <Nouvelle donnée>[/red]🔒")
            tablechoix.add_row("[red][strike]MV <Nouvelle donnée>[/red][/strike]", "[red]Modifier le montant versé du contrat par <Nouvelle donnée>[/red]🔒")
            tablechoix.add_row("[red][strike]MS SI/NS[/red][/strike]", "[red]Modifier l'état du contrat : SI = Signé / NS = Non Signé[/red]🔒")
            tablechoix.add_row("[red][strike]SUPPRIMER[/red][/strike]", "[red]Suprimer définitivement le contrat[/red]🔒")
            tablechoix.add_row("RET", "Retour au menu principal")
            tablechoix.add_row("QUIT", "Quitter le programme")
            console.print("")
        
        console.print(tablechoix)
        console.print("")
        if company.user_id == user.id and user.authorisation('Sale') :
            valid_choices = ["CR", "RET", "QUIT", "SUPPRIMER", "MS SI", "MS NS"]
            invalid_choices = []
            valid_choices_with_id = ["MT", "MV"]
        elif company.user_id is None:
            valid_choices = ["RET", "QUIT"]
            invalid_choices = ["CR", "SUPPRIMER", "SUPPRIMER", "MS SI", "MS NS"]
            valid_choices_with_id = []
        else: 
            valid_choices = ["RET", "QUIT"]
            invalid_choices = ["CR", "SUPPRIMER", "SUPPRIMER", "MS SI", "MS NS"]
            valid_choices_with_id = []

        console.print("")
        
        if company.user_id == user.id :
            for element in events_id:
                valid_choices.append(f"A{element}")
        else:
            for element in events_id:
                valid_choices.append(f"A{element}")
                
        while True:
            console.print("Votre choix [#AAAAAA]( CR, A18, D9 ...)[/#AAAAAA] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
            elif any(choix.startswith(c) for c in valid_choices_with_id):
                if choix.startswith("MT ") or choix.startswith("MV "):
                    try :
                        float(choix[3:])
                    except ValueError:
                        print("Erreur : La partie après 'MT,  MV' doit être un nombre valide ( chiffres et point seulement).")
                    else:
                        return choix
            elif choix in invalid_choices:
                console.print("[red]Ce n'est pas une de vos entreprises.[/red]")
            else:
                console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")


    def createevent(self, company, user, supports):
        if company.user_id == user.id :
            console = Console()
            pattern = re.compile(r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$")
            console.rule(f"Création d'un nouvel évènement")
            console.print("")
            
            while True:
                console.print("[green] Date et heure de début de l'évènement (format : JJ/MM/AAAA HH:MM) : [/green]")
                event_start = input('==>')
                if pattern.match(event_start):
                    event_date_start = datetime.strptime(event_start, "%d/%m/%Y %H:%M")
                    break
                else:
                    console.print("[red]Entrée invalide. Veuillez entrer uniquement des chiffres et un point.[/red]")

            while True:
                console.print("[green] Date et heure de fin de l'évènement (format : JJ/MM/AAAA HH:MM) : [/green]")
                event_end = input('==>')
                if pattern.match(event_end):
                    event_date_end = datetime.strptime(event_end, "%d/%m/%Y %H:%M")
                    break
                else:
                    console.print("[red]Entrée invalide. Veuillez entrer uniquement des chiffres et un point.[/red]")

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
            console.print("[green] Id du support chargé de l'évènement [/green]")
            role = None
            print(valid_role)
            while role not in valid_role:
                role = int(input('==>'))
                if role in valid_role:
                    support_id = role
                else:
                    console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")

            console.rule(f"Résumé de votre saisie pour confirmation")
            console.print("")
            tableconfirmation = Table(box=None)
            tableconfirmation.add_column("Type", justify="left", style="green", no_wrap=True)
            tableconfirmation.add_column("Vos saisies", justify="left", style="white")
            tableconfirmation.add_row("", "")
            tableconfirmation.add_row("Entreprise", f"{company.company_name}")
            tableconfirmation.add_row("Gestionnaire", "xxxxxxxxxxxxxxxxx")
            tableconfirmation.add_row("Date et heure de début de l'évènement", f"{event_date_start.strftime('%Y-%m-%d %H:%M:%S')}")
            tableconfirmation.add_row("Date et heure de fin de l'évènement", f"{event_date_end.strftime('%Y-%m-%d %H:%M:%S')}")
            tableconfirmation.add_row("Lieu de l'évènement", f"{location}")
            tableconfirmation.add_row("Nombre de personnes", f"{attendees}")
            tableconfirmation.add_row("Notes", f"{notes}")
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
                        return event_date_start, event_date_end, location, support_id, attendees, notes
                    else:
                        break
                else:
                    console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")
                    
                    
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



    def LiteViewCompagny(self, user, company, contacts):
        console = Console()
        console.rule(f"Récapitulatif de l'entreprise {company.company_name}")
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

        table1 = create_table(company, "Données entreprise")
        table2 = create_table(contacts, "Contacts")
        vertical_line = Text("\n".join("|" for _ in range(7)), style="green")
        
        console.print(Columns([table1, vertical_line, table2], padding=(0, 5)))
        console.print("")
        console.print("-" * console.width)
        centered_text = Text("Choix d'actions", style="bold green")
        console.print(Align.center(centered_text))
        
        tablechoix = Table(box=None)
        tablechoix.add_column("Choix", justify="left", style="green", no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")
        
        tablechoix.add_row("", "")
        tablechoix.add_row("LIST", "Retour a la liste")
        tablechoix.add_row("RET", "Retour au menu principal")
        tablechoix.add_row("QUIT", "Quitter le programme")
        console.print("")
    
        valid_choices = ["LIST", "RET", "QUIT"]
        console.print(tablechoix)
        console.print("")

        while True:
            console.print("Votre choix [#AAAAAA]( LIST, RET, QUIT ...)[/#AAAAAA] :")
            choix = input('==>')
            if choix in valid_choices:
                return choix
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


    def getText(self, user) :
        if user.authorisation("Gestion"):
            console = Console()
            console.rule(f"Création d'un nouveau message de la direction")
            console.print("")
            console.print("Votre message de la direction : ")
            data = str(input('==>'))
            return data
        
    def logWithoutUser(self, user, events, companys):
        console = Console()
        console.rule(f"Détail de tous les éléments non attribués ")
        console.print("") 

        events_id = []
        companys_id = []
        valid_choices = ["RET", "QUIT"]

        def create_table(liste, text):
            table = Table(title=f"{text}", box=None)
            if text == 'Evènements':
                table.add_column("id", justify="left", style="white", no_wrap=True)
                table.add_column("Participants", justify="left", style="white", no_wrap=True)
                table.add_column("Date de début", justify="left", style="white", no_wrap=True )
            else : 
                table.add_column("id", justify="left", style="white", no_wrap=True)
                table.add_column("Nom", justify="left", style="white", no_wrap=True)
            table.add_row("", "")
            for element in liste:
                if text == 'Evènements':
                    table.add_row(str(element.id), str(element.attendees), element.event_date_start.strftime("%Y-%m-%d %H:%M:%S"))
                    valid_choices.append(f"AE{element.id}")
                else:
                    table.add_row(str(element.id), element.company_name)
                    valid_choices.append(f"AC{element.id}")

            return table
        
        table1 = create_table(events, 'Evènements')
        table2 = create_table(companys, 'Entreprises')

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
        tablechoix.add_row("AE<id>", "Attribuer l'évènement <id>")
        tablechoix.add_row("AC<id>", "Attribuer l'entreprise <id>")
        tablechoix.add_row("RET", "Retour au menu principal")
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
                console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")
                
    def chooseUser(self, users):
        console = Console()
        console.rule(f"Liste des persones correpondantes")
        console.print("") 
        valid_choices = ["RET", "QUIT"]

        def create_table(liste):
            table = Table(title="Utilisateurs", box=None)
            table.add_column("id", justify="left", style="white", no_wrap=True)
            table.add_column("Nom", justify="left", style="white", no_wrap=True)
            table.add_column("Email", justify="left", style="white", no_wrap=True )
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
        tablechoix.add_column("Choix", justify="left", style="green", no_wrap=True)
        tablechoix.add_column("Description", justify="left", style="white")
        
        tablechoix.add_row("", "")
        tablechoix.add_row("A<id>", "Attribuer l'évènement a <id>")
        tablechoix.add_row("RET", "Retour au menu principal")
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
                console.print("[red]Choix invalide. Veuillez essayer à nouveau.[/red]")