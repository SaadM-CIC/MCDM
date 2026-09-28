import streamlit as st
from methods import valider_matrice
from utils import init_state

st.set_page_config(page_title="Outils d'aide à la décision", layout="wide")
init_state()

st.title("Outils d'aide à la décision multicritère")
st.write(
    "Saisissez la matrice de décision ci-dessous, puis utilisez la barre latérale "
    "pour calculer les **poids des critères** ou **classer les alternatives**."
)

# --- Matrice de décision -------------------------------------------------
st.subheader("1. Matrice de décision")
st.caption("Vous pouvez modifier les valeurs, renommer les alternatives, "
           "en ajouter (ligne vide en bas du tableau) ou en supprimer.")

df = st.session_state.matrice.reset_index()
edite = st.data_editor(df, num_rows="dynamic", hide_index=True,
                       use_container_width=True)

# --- Types de critères ---------------------------------------------------
st.subheader("2. Type de chaque critère")
st.caption("**max** : plus grand = mieux (bénéfice)   |   **min** : plus petit = mieux (coût)")

types_df = st.session_state.types.to_frame().T
types_edite = st.data_editor(
    types_df, hide_index=True, use_container_width=True,
    column_config={
        c: st.column_config.SelectboxColumn(options=["max", "min"], required=True)
        for c in types_df.columns
    },
)

# --- Validation et enregistrement ---------------------------------------
try:
    edite = edite.dropna(subset=["Alternative"])
    if edite["Alternative"].duplicated().any():
        raise AssertionError("Les noms d'alternatives doivent être uniques.")
    if edite.isna().any().any():
        raise AssertionError("Certaines cases sont vides.")
    nouvelle = edite.set_index("Alternative")
    nouveaux_types = types_edite.iloc[0].rename("Type")

    valider_matrice(nouvelle, nouveaux_types)

    st.session_state.matrice = nouvelle
    st.session_state.types = nouveaux_types
    st.success(f"Matrice valide : {nouvelle.shape[0]} alternatives × "
               f"{nouvelle.shape[1]} critères. Elle est prête pour les autres pages.")
except AssertionError as e:
    st.error(f"Matrice non valide : {e}")