import pandas as pd
import numpy as np
import streamlit as st
import users
import query


# pages

def page_admin(): 
    st.subheader("Bienvenue sur la page Administrateur")
    st.write('****')
    task = st.selectbox("Que voulez vous faire ?",["Voir la liste des utilisateurs","Ajouter un utilisateur"])
    if task == "Ajouter un utilisateur":
        st.subheader(":pencil2: Ajouter un nouvel utilisateur :pencil2:")
        new_user = st.text_input("username")
        new_password = st.text_input("password",type='password')
        if st.button("Ajouter"):
            users.create_usertable()
            users.add_userdata(new_user,users.make_hashes(new_password))
            st.success("Le nouvel utilisateur a été ajouté avec succès")
                           
    elif task == "Voir la liste des utilisateurs":
        st.subheader(":eyes: Liste des utilisateurs")
        user_result = users.view_all_users()
        clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
        st.dataframe(clean_db)

def page_user():
    st.subheader("Bienvenue sur la page Utilisateurs")
    st.write('***')  
    
    #premier graphique
    st.subheader('Montant du panier moyen en fonction de la catégorie socioprofessionnelle')
    st.bar_chart(query.df())
    st.write('***')
   
    #deuxième graphique
    st.subheader('Dépense par catégorie en fonction de la catégorie socioprofessionnelle')
    cat = st.selectbox('Sélectionnez la CSP à afficher', ("Agriculteurs", "Artisans-Commerçants", "Cadres", "Employés", "Ouvriers", "Professions intermédiaires", "Retraités", "Sans activité"))
    df_csp= query.df2().query('csp == @cat' ).set_index(['csp'])
    df_t=df_csp.T
    st.bar_chart(df_t)
    st.write('***')

    #export de données 
    st.subheader('Export de la table de collecte')
    b=st.number_input('Combien de lignes de la table souhaitez vous exporter ?', 0, 1000, 10)
    export=query.df_export(b)
    export

    st.download_button(
        label="télécharger les données en csv",
        data=export.to_csv().encode('utf-8'),
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
		hashed_pswd = users.make_hashes(password)
		result = users.login_admin(username,users.check_hashes(password,hashed_pswd))
		if result:
			st.sidebar.success("Bonjour {}".format(username))
			page_admin()

		else:
			st.sidebar.warning("l'identifiant ou le mot de passe est incorrect")

elif choice == "Utilisateurs":
	username = st.sidebar.text_input("Identifiant")
	password = st.sidebar.text_input("Mot de passe",type='password')
	if st.sidebar.checkbox("Login"):
		users.create_usertable()
		hashed_pswd = users.make_hashes(password)
		result = users.login_user(username,users.check_hashes(password,hashed_pswd))
		if result:
			st.sidebar.success("Bonjour {}".format(username))
			page_user()
			
		else:
			st.sidebar.warning("l'identifiant ou le mot de passe est incorrect")








