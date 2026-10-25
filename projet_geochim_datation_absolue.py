"""import matplotlib.pyplot as plt
import numpy as np

rapport_Rb_Sr = [2.24, 3.642, 6.59, 0.2313, 3.628] #axe horizontal
rapport_Sr_Sr = [0.738, 0.7612, 0.7992, 0.7074, 0.7573] #axe vertical

Lambda = 1.42e-11 #constante de désintégration du Rb87 en Sr87

A, B = np.polyfit(rapport_Rb_Sr, rapport_Sr_Sr, 1) #calcul de la pente et de l'ordonnée à l'origine de la droite de régression
t = (np.log(1 + A) / Lambda) #calcul du temps grace a la pente et au lambda
y_reg = A * np.array(rapport_Rb_Sr) + B #calcul des valeurs de y pour la droite de régression

plt.scatter(rapport_Rb_Sr, rapport_Sr_Sr, marker='o', label='Données expérimentales') #affichage des points expérimentaux
plt.plot(rapport_Rb_Sr, y_reg, '-', label='Droite de régression') #affichage de la droite de régression
plt.text(0.05, 0.95, f"y = {A:.5f}x + {B:.4f}\n Âge = {t/1e9:.2f} Ga", transform=plt.gca().transAxes, verticalalignment="top")
plt.xlabel("Rapport 87Rb/86Sr")
plt.ylabel("Rapport 87Sr/86Sr")
plt.title("Datation absolue par droite de isochrone Rb-Sr")
plt.grid(False)
plt.show()"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Datation absolue par isochrone Rb-Sr")

Lambda = 1.42e-11  # constante de désintégration du Rb87 en Sr87 (an^-1)

st.caption("Pour supprimer une ligne : coche la case à gauche, puis clique sur la corbeille (ou touche Suppr). Pour ajouter : clique sur + sous le tableau.")
st.write(
    "Modifie les valeurs du tableau, ajoute ou supprime des lignes \n(un échantillon par ligne) : le graphique et l'âge se mettent à jour."
)

# Tableau de départ (exemple), modifiable par l'utilisateur
def exemple():
    return pd.DataFrame({
        "Suppr.": [False] * 5,
        "Nom de l'écgantillon" : [] * 5,
        "87Rb/86Sr": [2.24, 3.642, 6.59, 0.2313, 3.628],
        "87Sr/86Sr": [0.738, 0.7612, 0.7992, 0.7074, 0.7573],
    })

# Fonction pour formater l'âge dans l'unité la plus adaptée
def formater_age(t):
    """Affiche l'âge dans l'unité la plus adaptée."""
    if t >= 1e9:
        return f"{t / 1e9:.2f} Ga"
    elif t >= 1e6:
        return f"{t / 1e6:.1f} Ma"
    else:
        return f"{t / 1e3:.1f} ka"
    
if "data" not in st.session_state:
    st.session_state.data = exemple()
    st.session_state.version = 0

st.caption("Coche « Suppr. » sur les lignes à retirer, puis clique sur ❌. Clique sur ➕ pour ajouter une ligne.")

edited = st.data_editor(
    st.session_state.data,
    num_rows="fixed",
    hide_index=True,
    key=f"editeur_{st.session_state.version}",
)

c1, c2, c3 = st.columns(3)
if c1.button("➕ Ajouter"):
    nouvelle = pd.DataFrame({"Suppr.": [False], "87Rb/86Sr": [np.nan], "87Sr/86Sr": [np.nan]})
    st.session_state.data = pd.concat([edited, nouvelle], ignore_index=True)
    st.session_state.version += 1
    st.rerun()
if c2.button("❌ Supprimer cochées"):
    st.session_state.data = edited[~edited["Suppr."]].reset_index(drop=True)
    st.session_state.version += 1
    st.rerun()
if c3.button("🗑️ Tout vider"):
    st.session_state.data = edited.iloc[0:0]
    st.session_state.version += 1
    st.rerun()

# On ne garde que les deux colonnes de rapports pour le calcul
df = edited[["87Rb/86Sr", "87Sr/86Sr"]].dropna()

# Garde-fous : on ignore les lignes incomplètes et on exige au moins 2 points
df = df.dropna()
if len(df) < 2:
    st.info("Ajoute au moins 2 points pour tracer l'isochrone.")
    st.stop()

rapport_Rb_Sr = df["87Rb/86Sr"].to_numpy()
rapport_Sr_Sr = df["87Sr/86Sr"].to_numpy()

# Calculs (identiques à ton script)
A, B = np.polyfit(rapport_Rb_Sr, rapport_Sr_Sr, 1)  # pente et ordonnée à l'origine
if A <= 0:
    st.warning("La pente est négative ou nulle : vérifie tes données, l'âge n'a pas de sens.")
    st.stop()
t = np.log(1 + A) / Lambda  # âge en années

# Résultats
col1, col2, col3 = st.columns(3)
col1.metric("Pente", f"{A:.5f}")
col2.metric("⁸⁷Sr/⁸⁶Sr initial", f"{B:.4f}")
col3.metric("Âge", formater_age(t))

# Graphique
fig, ax = plt.subplots()
ax.scatter(rapport_Rb_Sr, rapport_Sr_Sr, marker="o", label="Données expérimentales")
x_min = min(rapport_Rb_Sr)
x_max = max(rapport_Rb_Sr)
marge = (x_max - x_min) * 0.05

ax.set_xlim(x_min - marge, x_max + marge)
xs = np.linspace(*ax.get_xlim(), 100)
ax.plot(xs, A * xs + B, "-", label="Droite de régression")
ax.text(
    0.05, 0.95,
    f"y = {A:.3e}x + {B:.4f}\nÂge = {formater_age(t)}",
    transform=ax.transAxes,
    verticalalignment="top",
)
ax.set_xlabel("Rapport 87Rb/86Sr")
ax.set_ylabel("Rapport 87Sr/86Sr")
ax.set_title("Datation absolue par droite isochrone Rb-Sr")
ax.legend(loc="lower right")
st.pyplot(fig)
