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


def appliquer_style():
    """Applique le thème visuel commun à toutes les pages Streamlit."""
    st.markdown(
        """
        <style>
        :root {
            --mcdm-ink: #172b3a;
            --mcdm-muted: #637787;
            --mcdm-accent: #147d78;
            --mcdm-accent-dark: #0e625e;
            --mcdm-surface: #ffffff;
            --mcdm-canvas: #f3f7f8;
            --mcdm-border: #dce6e9;
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(ellipse at 85% 0%, rgba(20, 125, 120, 0.08), transparent 34rem),
                var(--mcdm-canvas);
            color: var(--mcdm-ink);
        }

        [data-testid="stHeader"] {
            background: rgba(243, 247, 248, 0.82);
        }

        [data-testid="stSidebar"] {
            background: #eaf1f2;
            border-right: 1px solid var(--mcdm-border);
        }

        [data-testid="stMain"] .block-container {
            max-width: 1440px;
            padding-top: 2.4rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3 {
            color: var(--mcdm-ink);
            letter-spacing: -0.035em;
        }

        h1 {
            font-weight: 750;
            padding-bottom: 0.65rem;
            border-bottom: 3px solid var(--mcdm-accent);
        }

        h2, h3 {
            font-weight: 650;
        }

        [data-testid="stCaptionContainer"],
        [data-testid="stMarkdownContainer"] p {
            color: var(--mcdm-muted);
        }

        [data-testid="stVerticalBlockBorderWrapper"],
        [data-testid="stDataFrame"],
        [data-testid="stTable"] {
            border: 1px solid var(--mcdm-border);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 5px 18px rgba(23, 43, 58, 0.045);
        }

        [data-testid="stDataEditor"] {
            border: 1px solid var(--mcdm-border);
            border-radius: 12px;
            overflow: hidden;
        }

        [data-testid="stButton"] > button,
        [data-testid="stFormSubmitButton"] > button {
            border-radius: 9px;
            font-weight: 650;
            transition: transform 120ms ease, box-shadow 120ms ease, background 120ms ease;
        }

        [data-testid="stButton"] > button[kind="primary"],
        [data-testid="stFormSubmitButton"] > button[kind="primary"] {
            background: var(--mcdm-accent);
            border-color: var(--mcdm-accent);
            color: white;
        }

        [data-testid="stButton"] > button[kind="primary"]:hover,
        [data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
            background: var(--mcdm-accent-dark);
            border-color: var(--mcdm-accent-dark);
            box-shadow: 0 5px 14px rgba(20, 125, 120, 0.2);
            transform: translateY(-1px);
        }

        [data-testid="stAlert"] {
            border-radius: 10px;
        }

        [data-testid="stSlider"] [role="slider"],
        [data-testid="stCheckbox"] [role="checkbox"] {
            accent-color: var(--mcdm-accent);
        }

        hr {
            border-color: var(--mcdm-border);
        }

        @media (max-width: 700px) {
            [data-testid="stMain"] .block-container {
                padding: 1.4rem 1rem 2rem;
            }

            h1 {
                font-size: 1.8rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state():
    """Initialise la matrice et les types au premier chargement.
    À appeler au début de chaque page."""
    appliquer_style()
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