import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu
import bcrypt
import yaml
from yaml.loader import SafeLoader
def load_users():
    try:
        users = pd.read_csv('partie_3_codes.csv')
        return users
    except FileNotFoundError:
        st.error("Le fichier partie_3_codes.csv est introuvable.")  # Diagnostic si le fichier n'existe pas
        return pd.DataFrame(columns=["name", "password", "email", "failed_login_attempts", "role"])
users_df = load_users()

credentials = {
    "usernames": {
        row["name"]: {
            "name": row["name"],
            "password": row["password"],  # Déjà haché
            "email" : row["email"],
            "failed_login_attempts" : row["failed_login_attempts"],
            "role": row["role"]
        }
        for _, row in users_df.iterrows()}}

config = {"credentials": credentials, "cookie": {"expiry_days": 1}}


authenticator = stauth.Authenticate(
    config["credentials"], # Les données des comptes
    "cookie name", # Le nom du cookie, un str quelconque
    "cookie key", # La clé du cookie, un str quelconque
    30, # Le nombre de jours avant que le cookie expire 
)


authenticator.login()
if st.session_state["authentication_status"]:
 
  with st.sidebar:
    authenticator.logout("Déconnexion")
    st.write(f"Bienvenue, {st.session_state['name']}")
    selection = option_menu(
            menu_title=None,
            options = ["Accueil", "Mon équipe"]
        )
    
  if selection == 'Accueil':
    st.title("Bienvenue sur ma page")
    st.write("Ca c'est moi :point_down: Professeur Hubert Farnsworth")
    st.image("prof.png")
  elif selection == 'Mon équipe':

        st.title("Bienvenue sur la page des personnages de futurama")
        col1, col2, col3 = st.columns(3)
        with col1 :
            st.header("Leela")
            st.image("leela-1.png")
        with col2 :
            st.header("Bender")
            st.image("bender.png")
        with col3 :  
            st.header("Fry") 
            st.image("fry.png")


# Si l'utilisateur n'est pas authentifié
elif st.session_state.get("authentication_status") is False:
    st.error("L'username ou le mot de passe est incorrect")
elif st.session_state.get("authentication_status") is None:
    st.warning('Les champs username et mot de passe doivent être remplis')
    st.write("Pour te connecter en username entre ton prénom avec majuscule et accent exemple : Antoine et en mot de passe ton prénom en minuscule sans accent exemple : antoine")