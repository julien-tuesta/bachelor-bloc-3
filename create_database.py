import sqlite3
import random


# création table client
table_client = '''CREATE TABLE client (
                        id_client INTEGER PRIMARY KEY,
                        nb_enfants INTEGER,
                        csp TEXT,
                        montant DECIMAL(10, 2),
                        id_collecte INTEGER,
                        FOREIGN KEY (id_collecte) REFERENCES collecte(id_collecte),
                        FOREIGN KEY (montant) REFERENCES collecte(montant)
                    )'''

# création table 
table_collecte = '''CREATE TABLE collecte (
                        id_collecte INTEGER PRIMARY KEY,
                        montant DECIMAL(10, 2),
                        alimentaire DECIMAL(10, 2),
                        textile DECIMAL(10, 2),
                        multimedia DECIMAL(10, 2),
                        bazar DECIMAL(10, 2),
                        jardin DECIMAL(10, 2)
                    )'''

# commande pour inserer les données dans les tables
insert_client = '''INSERT INTO client (id_client, nb_enfants, csp, montant, id_collecte) VALUES (?, ?, ?, ?, ?)'''

insert_collecte = '''INSERT INTO collecte (id_collecte, montant, alimentaire, textile, multimedia, bazar, jardin) VALUES (?, ?, ?, ?, ?, ?, ?)'''


a=1000
clients = []
for i in range(a):
    id_client = i+1
    nb_enfants = random.randint(0,5)
    csp = random.choice(["Agriculteurs", "Cadres", "Employés", "Ouvriers", "Artisans-Commerçants", "Professions intermédiaires", "Retraités", "Sans activité"])  # Choix aléatoire d'une csp
    montant = round(random.uniform(1.00, 500.00), 2)
    id_collecte  = i+1
    clients.append((id_client, nb_enfants, csp, montant, id_collecte))

collectes = []
for i in range (a):
    id_collecte=clients[i][0]
    montant=clients[i][3]
    alimentaire=round(random.uniform(0.00, montant), 2)
    textile=round(random.uniform(0.00, montant-alimentaire), 2)
    multimedia = round(random.uniform(0.00, montant-alimentaire-textile), 2)
    bazar = round(random.uniform(0.00, montant-alimentaire-textile-multimedia), 2)
    jardin= round(montant-alimentaire-textile-multimedia-bazar,2)
    collectes.append((id_collecte, montant, alimentaire, textile, multimedia, bazar, jardin))



# connexion et création des tables
with sqlite3.connect('goldenline.db') as conn:
    conn.execute(table_client)
    conn.execute(table_collecte)

        
    # Insertion des données dans la table client
    for client in clients:
        conn.execute(insert_client, client)

    # Insertion des données dans la table collecte
    for collecte in collectes:
        conn.execute(insert_collecte, collecte)

    # Validation de la transaction et fermeture de la connexion
    conn.commit()

    print("la base de données a été générée avec succès")