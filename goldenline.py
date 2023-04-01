import pandas as pd
import numpy as np
import streamlit as st
import sqlite3
from pathlib import Path


# Define the paths
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
database_path = current_dir / "goldenline.db"

# hash des mots de passe
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# connection à la database
conn = sqlite3.connect(database_path)

#gestion de la base de données utilisateurs
c = conn.cursor()
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def login_admin(username,password):
	c.execute('SELECT * FROM admintable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

# première requete
query = '''
SELECT csp, avg(montant) as panier_moyen
FROM client
GROUP BY csp
'''
df = pd.read_sql_query(query, conn).set_index(['csp'])

#deuxième requete
query = '''
SELECT csp, avg(alimentaire) as alimentaire, avg(textile) as textile, avg(multimedia) as multimedia, avg(bazar) as bazar, avg(jardin) as jardin
FROM client INNER JOIN collecte ON client.id_collecte=collecte.id_collecte
GROUP BY csp 
'''
df2 = pd.read_sql_query(query, conn)


# pages

def page_admin(): 
    st.subheader("Bienvenue sur la page Administrateur")
    st.write('****')
    task = st.selectbox("Que voulez vous faire ?",["Voir la liste des utilisateurs","Ajouter un utilisateur"])
    if task == "Ajouter un utilisateur":
        st.subheader(":pencil2: Ajouter un nouvel utilisateur")
        new_user = st.text_input("username")
        new_password = st.text_input("password",type='password')
        if st.button("Ajouter"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("Le nouvel utilisateur a été ajouté avec succès")
                           
    elif task == "Voir la liste des utilisateurs":
        st.subheader(":eyes: Liste des utilisateurs")
        user_result = view_all_users()
        clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
        st.dataframe(clean_db)

def page_user():
    st.subheader("Bienvenue sur la page Utilisateurs")
    st.write('***')  
    
    #premier graphique
    st.subheader('Montant du panier moyen en fonction de la catégorie socioprofessionnelle')
    st.bar_chart(df)
    st.write('***')
   
    #deuxième graphique
    st.subheader('Dépense par catégorie en fonction de la catégorie socioprofessionnelle')
    cat = st.selectbox('Sélectionnez la CSP à afficher', ("Agriculteurs", "Artisans-Commerçants", "Cadres", "Employés", "Ouvriers", "Professions intermédiaires", "Retraités", "Sans activité"))
    df_csp= df2.query('csp == @cat' ).set_index(['csp'])
    df_t=df_csp.T
    st.bar_chart(df_t)
    st.write('***')

    #export de données 
    st.subheader('Export de la table de collecte')
    b=st.number_input('Combien de lignes de la table souhaitez vous exporter ?', 0, 1000, 10)
    query = f"SELECT * FROM collecte LIMIT {b}"
    df_export = pd.read_sql_query(query, conn).set_index(['id_collecte'])
    df_export

    st.download_button(
        label="télécharger les données en csv",
        data=df_export.to_csv().encode('utf-8'),
        file_name='données_exportées.csv',
        mime='text/csv',
    )      



# haut de page
st.title('Goldenline')
st.header(':bar_chart: :blue[Visualisation des données]')
st.write('***')    

pages={
"administrateur": page_admin,
"utilisateurs" : page_user
}

#sidebar
menu = ["Administrateur","Utilisateurs"]
choice = st.sidebar.selectbox("Se connecter en tant que :",menu)

if choice == "Administrateur":
	username = st.sidebar.text_input("Identifiant")
	password = st.sidebar.text_input("Mot de passe",type='password')
	if st.sidebar.checkbox("Login"):
		hashed_pswd = make_hashes(password)
		result = login_admin(username,check_hashes(password,hashed_pswd))
		if result:
			st.sidebar.success("Bonjour {}".format(username))
			page_admin()

		else:
			st.sidebar.warning("l'identifiant ou le mot de passe est incorrect")

elif choice == "Utilisateurs":
	username = st.sidebar.text_input("Identifiant")
	password = st.sidebar.text_input("Mot de passe",type='password')
	if st.sidebar.checkbox("Login"):
		create_usertable()
		hashed_pswd = make_hashes(password)
		result = login_user(username,check_hashes(password,hashed_pswd))
		if result:
			st.sidebar.success("Bonjour {}".format(username))
			page_user()
			
		else:
			st.sidebar.warning("l'identifiant ou le mot de passe est incorrect")


# fermer la connexion
conn.close()









