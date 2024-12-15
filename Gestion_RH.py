from dbScript import DatabaseHandler


class Employe:
    def __init__(self, id, prenom, nom, age, poste, salaire):
        self.id = id
        self.prenom = prenom
        self.nom = nom
        self.age = age
        self.poste = poste
        self.salaire = salaire

    def __str__(self):
        return f"ID: {self.id}, Prénom: {self.prenom}, Nom: {self.nom}, Age: {self.age}, Poste: {self.poste}, Salaire: {self.salaire}"


class Departement:
    def __init__(self, id, nom, id_manager=None, nom_manager=None, salaire_total=0):
        self.id = id
        self.nom = nom
        self.id_manager = id_manager
        self.nom_manager = nom_manager
        self.salaire_total = salaire_total

    def __str__(self):
        return f"ID: {self.id}, Nom: {self.nom}, Manager: {self.nom_manager}, Salaire Total (TL): {self.salaire_total}"


class SystemeRH:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def ajouter_employe(self, prenom, nom, age, poste, salaire):
        self.db_handler.execute_query(
            "INSERT INTO employes (prenom, nom, age, poste, salaire) VALUES (?, ?, ?, ?, ?)",
            (prenom, nom, age, poste, salaire)
        )

    def obtenir_employe(self, id):
        result = self.db_handler.fetch_query("SELECT * FROM employes WHERE id = ?", (id,))
        if result:
            ligne = result[0]
            return Employe(ligne[0], ligne[1], ligne[2], ligne[3], ligne[4], ligne[5])
        return None

    def ajouter_departement(self, nom, id_manager=None):
        self.db_handler.execute_query(
            "INSERT INTO departements (nom, id_manager) VALUES (?, ?)", (nom, id_manager)
        )

    def obtenir_departement(self, id):
        result = self.db_handler.fetch_query("SELECT * FROM departements WHERE id = ?", (id,))
        if result:
            ligne = result[0]
            if ligne[2]:  # Si le departement a un manager
                manager_result = self.db_handler.fetch_query("SELECT prenom, nom FROM employes WHERE id = ?", (ligne[2],))
                manager = manager_result[0]
                nom_manager = f"{manager[0]} {manager[1]}"
            else:
                nom_manager = "Aucun manager"

            salaire_total_result = self.db_handler.fetch_query("SELECT SUM(salaire) FROM employes WHERE id_manager = ?", (ligne[0],))
            salaire_total = salaire_total_result[0][0] if salaire_total_result[0][0] else 0

            return Departement(ligne[0], ligne[1], ligne[2], nom_manager, salaire_total)
        return None

    def lister_employes(self):
        result = self.db_handler.fetch_query("SELECT * FROM employes")
        return [Employe(ligne[0], ligne[1], ligne[2], ligne[3], ligne[4], ligne[5]) for ligne in result]

    def lister_departements(self):
        result = self.db_handler.fetch_query("SELECT * FROM departements")
        departements = []
        for ligne in result:
            if ligne[2]:  # Si le departement a un manager
                manager_result = self.db_handler.fetch_query("SELECT prenom, nom FROM employes WHERE id = ?", (ligne[2],))
                manager = manager_result[0]
                nom_manager = f"{manager[0]} {manager[1]}"
            else:
                nom_manager = "Aucun manager"

            salaire_total_result = self.db_handler.fetch_query("SELECT SUM(salaire) FROM employes WHERE id_manager = ?", (ligne[0],))
            salaire_total = salaire_total_result[0][0] if salaire_total_result[0][0] else 0

            departement = Departement(ligne[0], ligne[1], ligne[2], nom_manager, salaire_total)
            departements.append(departement)
        return departements

    def fermer(self):
        self.db_handler.fermer()


if __name__ == "__main__":
    # Create the DatabaseHandler instance
    db_handler = DatabaseHandler()

    # Create the SystemeRH instance with the database handler
    systeme_rh = SystemeRH(db_handler)

    # Ajouter des employés avec des prénoms et noms marocains
    systeme_rh.ajouter_employe("Mohamed", "El Amrani", 30, "Ingénieur Informatique", 70000)
    systeme_rh.ajouter_employe("Yassir", "Benkirane", 28, "Développeur Web", 50000)
    systeme_rh.ajouter_employe("Fatima Zahra", "Oufkir", 34, "Responsable RH", 80000)
    systeme_rh.ajouter_employe("Imane", "Berrada", 27, "Chargée de recrutement", 45000)

    # Ajouter des départements
    systeme_rh.ajouter_departement("Technologie", 1)  # Mohamed El Amrani est le manager
    systeme_rh.ajouter_departement("Ressources Humaines", 3)  # Fatima Zahra Oufkir est le manager

    # Obtenir et afficher un employé
    employe = systeme_rh.obtenir_employe(1)
    if employe:
        print(employe)

    # Obtenir et afficher un département
    departement = systeme_rh.obtenir_departement(1)
    if departement:
        print(departement)

    # Lister tous les employés
    print("\nTous les Employés:")
    for emp in systeme_rh.lister_employes():
        print(emp)

    # Lister tous les départements
    print("\nTous les Départements:")
    for dep in systeme_rh.lister_departements():
        print(dep)

    # Fermer la connexion à la base de données
    systeme_rh.fermer()
