import pandas as pd
import sqlite3
from pathlib import Path

# Define the paths
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
database_path = current_dir / "goldenline.db"


# connection à la database
conn = sqlite3.connect(database_path,check_same_thread=False)


# première requete

def df():
    query = '''
    SELECT csp, avg(montant) as panier_moyen
    FROM client
    GROUP BY csp
    '''
    return pd.read_sql_query(query, conn).set_index(['csp'])

#deuxième requete

def df2():
    query = '''
    SELECT csp, avg(alimentaire) as alimentaire, avg(textile) as textile, avg(multimedia) as multimedia, avg(bazar) as bazar, avg(jardin) as jardin
    FROM client INNER JOIN collecte ON client.id_collecte=collecte.id_collecte
    GROUP BY csp 
    '''
    return pd.read_sql_query(query, conn)

def df_export(b):
    query_donnees = f"SELECT * FROM collecte LIMIT {b}"
    return pd.read_sql_query(query_donnees, conn).set_index(['id_collecte'])


