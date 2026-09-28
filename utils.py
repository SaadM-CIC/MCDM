import pandas as pd
import streamlit as st

ALTERNATIVES = ["Actions", "Obligations", "Mixte", "Immobilier", "Tech"]
CRITERES = ["Rendement (%)", "Volatilité (%)", "Sharpe", "Drawdown max (%)", "Frais (%)"]
TYPES = ["max", "min", "max", "min", "min"]

DATA = [
    [12.5, 18.0, 0.58, 35, 0.8],
    [ 4.2,  5.5, 0.40, 12, 0.3],
    [ 8.1, 10.2, 0.60, 20, 0.6],
    [ 6.8,  8.5, 0.56, 18, 1.2],
    [16.0, 25.0, 0.56, 45, 1.0],
]


def init_state():
    """Initialise la matrice et les types au premier chargement.
    À appeler au début de chaque page."""
    if "matrice" not in st.session_state:
        m = pd.DataFrame(DATA, index=ALTERNATIVES, columns=CRITERES)
        m.index.name = "Alternative"
        st.session_state.matrice = m
        st.session_state.types = pd.Series(TYPES, index=CRITERES, name="Type")
def afficher_steps(res):
    for i, (titre, obj) in enumerate(res["steps"], 1):
        st.markdown(f"**Étape {i} : {titre}**")
        if isinstance(obj, (pd.DataFrame, pd.Series)):
            df = pd.DataFrame(obj)
            st.dataframe(df.style.format("{:.4f}", subset=df.select_dtypes("number").columns),
                         use_container_width=True)
        else:
            st.write(obj)