#----------------------------------------PARTIE PYTHON----------------------------------------

#import matplotlib.pyplot as plt 
#import numpy as np

#rapport_Rb_Sr = [2.24, 3.642, 6.59, 0.2313, 3.628] #axe horizontal                                                              <- j'ai repris les données du dm de géochimie de L2, pour vérifier la véracité de mes résultats 
#rapport_Sr_Sr = [0.738, 0.7612, 0.7992, 0.7074, 0.7573] #axe vertical

#Lambda = 1.42e-11                                                                                                               <- constante de désintégration du Rb87 en Sr87

#A, B = np.polyfit(rapport_Rb_Sr, rapport_Sr_Sr, 1)                                                                              <- calcul de la pente et de l'ordonnée à l'origine de la droite de régression
#t = (np.log(1 + A) / Lambda)                                                                                                    <- calcul du temps grâce à la pente et au lambda
#y_reg = A * np.array(rapport_Rb_Sr) + B                                                                                         <- calcul des valeurs de y pour la droite de régression

#plt.scatter(rapport_Rb_Sr, rapport_Sr_Sr, marker='o', label='Données expérimentales')                                           <- affichage des points expérimentaux
#plt.plot(rapport_Rb_Sr, y_reg, '-', label='Droite de régression')                                                               <- affichage de la droite de régression
#plt.text(0.05, 0.95, f"y = {A:.5f}x + {B:.4f}\n Âge = {t/1e9:.2f} Ga", transform=plt.gca().transAxes, verticalalignment="top")  <- affichage de la formule de la droite de régression
#plt.xlabel("Rapport 87Rb/86Sr")                                                                                                 <- légende de l'axe horizontal
#plt.ylabel("Rapport 87Sr/86Sr")                                                                                                 <- légende de l'axe vertical
#plt.title("Datation absolue par droite isochrone Rb-Sr")                                                                        <- titre du graphique
#plt.grid(False) 
#plt.show()



#----------------------------------------PARTIE PYTHON + STREAMLIT----------------------------------------
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.set_page_config(page_title="Isochrone Rb-Sr", page_icon="🪨", layout="wide")
st.title("Datation absolue par isochrone Rb-Sr")

Lambda = 1.42e-11  # constante de désintégration du Rb87 en Sr87 (an^-1)

st.caption("Pour supprimer une ligne : coche la case à gauche, puis clique sur la corbeille (ou touche Suppr). Pour ajouter : clique sur + sous le tableau.")
with st.expander("Comment ça marche ?"):
    st.markdown("""
    **Le principe :** Certains minéraux contiennent du rubidium-87 (⁸⁷Rb), un atome
    radioactif qui se transforme lentement en strontium-87 (⁸⁷Sr). Cette transformation
    est très lente (demi-vie d'environ 49 milliards d'années) mais régulière : plus une
    roche est ancienne, plus elle contient de ⁸⁷Sr issu de cette désintégration.

    Des minéraux formés au même moment peuvent contenir des quantités différentes de ⁸⁷Rb.
    Avec le temps, ils produisent donc des quantités différentes de ⁸⁷Sr.

    Pour pouvoir les comparer, on prend le ⁸⁶Sr comme référence : cet isotope est stable,
    sa quantité ne change pas avec le temps. On mesure ainsi, pour chaque échantillon, les
    rapports ⁸⁷Rb/⁸⁶Sr et ⁸⁷Sr/⁸⁶Sr.

    En reportant ces rapports sur un graphique, les points forment une droite appelée **isochrone**.

    - la **pente** de la droite dépend de l'âge.
    - l'**ordonnée à l'origine** donne le rapport ⁸⁷Sr/⁸⁶Sr initial.
    """)
    st.latex(r"t = \frac{1}{\lambda}\ln(1+a)")
    st.markdown("""
    où *t* est l'âge, *a* la pente de la droite et *λ* la constante de désintégration
    du ⁸⁷Rb : 1,42 × 10⁻¹¹ an⁻¹ (valeur recommandée par Steiger et Jäger, 1977).

    **Limites.** La méthode suppose que les échantillons ont le même âge et le même
    ⁸⁷Sr/⁸⁶Sr initial, et que le système est resté fermé (ni gain ni perte de Rb ou de Sr).
    Si les points ne s'alignent pas bien, la roche a peut-être été perturbée
    (métamorphisme, altération).
    """)
    
# Tableau de départ (exemple), modifiable par l'utilisateur
def exemple():
    return pd.DataFrame({
        "Suppr.": [False] * 5,
        "Nom de l'échantillon" : ["Roche 1", "Roche 2", "Roche 3", "Roche 4", "Roche 5"],
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

col_tableau, col_graphique = st.columns([1, 1.6], gap="large")
with col_tableau:
    edited = st.data_editor(
        st.session_state.data,
        num_rows="fixed",
        hide_index=True,
        key=f"editeur_{st.session_state.version}",
    )
# Permet d'ajouter, supprimer et tout vider dans le tableau des valeurs
    c1, c2, c3 = st.columns(3)
    if c1.button("❌ Supprimer  \ncochées"):
        st.session_state.data = edited[~edited["Suppr."]].reset_index(drop=True)
        st.session_state.version += 1
        st.rerun()
    if c2.button("➕ Ajouter"):
        nouvelle = pd.DataFrame({"Suppr.": [False], "87Rb/86Sr": [np.nan], "87Sr/86Sr": [np.nan]})
        st.session_state.data = pd.concat([edited, nouvelle], ignore_index=True)
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

df = edited[["Nom de l'échantillon", "87Rb/86Sr", "87Sr/86Sr"]]
df = df.dropna(subset=["87Rb/86Sr", "87Sr/86Sr"])

rapport_Rb_Sr = df["87Rb/86Sr"].to_numpy()
rapport_Sr_Sr = df["87Sr/86Sr"].to_numpy()

# Calcul de la pente, de l’ordonnée à l’origine et de l’âge (repris du script Python initial)
A, B = np.polyfit(rapport_Rb_Sr, rapport_Sr_Sr, 1)  # pente et ordonnée à l'origine
if A <= 0:
    st.warning("La pente est négative ou nulle : vérifie tes données, l'âge n'a pas de sens.")
    st.stop()
t = np.log(1 + A) / Lambda  # âge en années

# Graphique
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(rapport_Rb_Sr, rapport_Sr_Sr, marker="o", label="Données expérimentales")
for x, y, nom in zip(
    df["87Rb/86Sr"],
    df["87Sr/86Sr"],
    df["Nom de l'échantillon"],
):
    if pd.notna(nom) and str(nom).strip():
        ax.annotate(
            str(nom),
            (x, y),
            xytext=(7, 0),
            textcoords="offset points",
            fontsize=12,
        )
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
# Partie qui affiche les infos sur le graphique (nom des axes (en x et en y), titre, coefficient directeur, rapport 87Sr/86Sr initial et l'âge)
ax.set_xlabel("Rapport 87Rb/86Sr")
ax.set_ylabel("Rapport 87Sr/86Sr")
ax.set_title("Datation absolue par droite isochrone Rb-Sr")
ax.legend(loc="lower right")
with col_graphique:
    st.pyplot(fig, use_container_width=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Pente", f"{A:.5f}")
    col2.metric("⁸⁷Sr/⁸⁶Sr initial", f"{B:.4f}")
    col3.metric("Âge", formater_age(t))
