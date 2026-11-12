import streamlit as st
import pandas as pd
import numpy as np
from methods import waspas, topsis, fuzzy_topsis
from utils import init_state, afficher_steps

st.set_page_config(page_title="Classement", layout="wide")
init_state()

matrice = st.session_state.matrice
types = st.session_state.types
criteres = list(matrice.columns)

st.title("Classement des alternatives")

methode = st.sidebar.radio("Méthode", ["WASPAS", "TOPSIS", "Fuzzy TOPSIS"])
st.subheader(f"Méthode : {methode}")

# --- 1. Choix des poids --------------------------------------------------
st.markdown("#### 1. Poids des critères")

# Les poids mémorisés ne sont utilisables que s'ils correspondent aux critères actuels
poids_memo = st.session_state.get("poids")
memo_ok = poids_memo is not None and list(poids_memo.index) == criteres

options = ["Saisie manuelle"]
if memo_ok:
    options.insert(0, f"Derniers poids calculés ({st.session_state.poids_source})")
origine = st.radio("Origine des poids", options, horizontal=True)

if origine == "Saisie manuelle":
    st.caption("Saisissez des valeurs positives : elles seront automatiquement normalisées "
               "pour que leur somme vaille 1.")
    brut = st.data_editor(
        pd.DataFrame({"Poids": [1.0] * len(criteres)}, index=criteres),
        use_container_width=True,
        key="poids_manuels",
    )["Poids"]
    if (brut <= 0).any() or brut.isna().any():
        st.error("Tous les poids doivent être strictement positifs.")
        st.stop()
    poids = (brut / brut.sum()).rename("Poids")
else:
    poids = poids_memo.rename("Poids")
    if not memo_ok:
        st.warning("Aucun poids calculé : utilisez la page Pondération ou la saisie manuelle.")

st.dataframe(poids.to_frame().T.style.format("{:.4f}"), use_container_width=True)

# --- 2. Paramètres -------------------------------------------------------
lam = 0.5
delta_x = 0.10
delta_w = 0.10
if methode == "WASPAS":
    st.markdown("#### 2. Paramètre λ")
    lam = st.slider("λ (0 = produit pondéré pur, 1 = somme pondérée pure)",
                    0.0, 1.0, 0.5, 0.05)
elif methode == "Fuzzy TOPSIS":
    st.markdown("#### 2. Incertitude des données et des poids")
    delta_x = st.slider("δₓ — incertitude sur les données", 0.0, 0.5, 0.10, 0.05)
    delta_w = st.slider("δᵥ — incertitude sur les poids", 0.0, 0.5, 0.10, 0.05)

# --- 3. Run --------------------------------------------------------------
if st.button("▶ Run", type="primary"):
    try:
        if methode == "WASPAS":
            res = waspas(matrice, types, poids, lam)
        elif methode == "Fuzzy TOPSIS":
            res = fuzzy_topsis(matrice, types, poids, delta_x=delta_x, delta_w=delta_w)
        else:
            res = topsis(matrice, types, poids)
        st.session_state.res_class = {
            "methode": methode, "res": res,
            "delta_x": delta_x, "delta_w": delta_w,
        }
    except AssertionError as e:
        st.error(f"Erreur : {e}")

# --- Affichage du dernier résultat --------------------------------------
stocke = st.session_state.get("res_class")
resultat_a_jour = (
    stocke
    and stocke["methode"] == methode
    and (
        methode != "Fuzzy TOPSIS"
        or (stocke["delta_x"] == delta_x and stocke["delta_w"] == delta_w)
    )
)
if resultat_a_jour:
    st.divider()
    afficher_steps(stocke["res"])

    st.markdown("### Résultat final : classement")
    classement = stocke["res"]["result"]
    score = {"WASPAS": "Q", "TOPSIS": "C", "Fuzzy TOPSIS": "CC"}[methode]

    meilleur = classement.index[0]
    st.success(f"Meilleure alternative : **{meilleur}** ({score} = {classement[score].iloc[0]:.4f})")

    g, t = st.columns([2, 1])
    g.bar_chart(classement[score])
    t.dataframe(classement.style.format({c: "{:.4f}" for c in classement.columns if c != "Rang"}),
                use_container_width=True)

    if methode == "Fuzzy TOPSIS":
        st.caption(f"Comparaison calculée avec les poids sélectionnés : {origine}.")
        comparaison = pd.DataFrame({
            "TOPSIS": topsis(matrice, types, poids)["result"]["Rang"],
            "Fuzzy TOPSIS": classement["Rang"],
        }).loc[matrice.index]
        st.markdown("### TOPSIS vs Fuzzy TOPSIS (poids sélectionnés)")
        st.dataframe(comparaison, use_container_width=True)

        sensibilite = pd.DataFrame({
            f"δ = {d:.1f}": fuzzy_topsis(
                matrice, types, poids, delta_x=d, delta_w=d
            )["result"]["CC"]
            for d in [0.0, 0.1, 0.2, 0.3]
        }).loc[matrice.index]
        st.markdown("### Sensibilité du coefficient CC à l'incertitude δ")
        st.dataframe(sensibilite.style.format("{:.4f}"), use_container_width=True)