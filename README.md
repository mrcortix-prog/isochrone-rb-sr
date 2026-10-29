# isochrone-rb-sr

Ce projet repose sur le principe de la décroissance radioactive. Un isotope radioactif (appelé élément père, instable par définition) se désintègre au cours du temps en un isotope radiogénique (appelé élément fils, stable par définition). Ce sont les rapports isotopiques père/fils que l’on mesure pour déterminer l’âge. Il est donc important de savoir si l’on peut négliger la quantité initiale de fils : si c’est le cas, on parle de système riche, dans le cas inverse, de système pauvre.

Il existe plusieurs couples père-fils, et celui utilisé ici est le couple rubidium (père) - strontium (fils).

On part de la loi de décroissance $P(t) = P_0 \, e^{-\lambda t}$, obtenue par intégration de $-\frac{dN}{dt} = \lambda N(t)$. On en déduit la quantité de fils : $F = F_0 + P\,(e^{\lambda t}-1)$.

Le couple Rb-Sr est un système pauvre : la quantité initiale de fils $F_0$ n’est pas négligeable, d’où l’expression ci-dessus, qui la conserve.

En remplaçant le père et le fils, on obtient :

$$^{87}Sr = {}^{87}Sr_0 + {}^{87}Rb\,(e^{\lambda t}-1)$$

Cette équation présente deux inconnues : $^{87}Sr_0$ et $t$.

Pour les déterminer, on divise chaque terme par $^{86}Sr$, isotope stable et non radiogénique, dont la quantité est restée constante depuis la formation de la roche. On obtient une fonction affine :

$$\frac{^{87}Sr}{^{86}Sr} = \left(\frac{^{87}Sr}{^{86}Sr}\right)_0 + \frac{^{87}Rb}{^{86}Sr}\,(e^{\lambda t}-1)$$

C’est une équation de type $y = ax + b$, avec $a = e^{\lambda t}-1$ (la pente) et $b = \left(\frac{^{87}Sr}{^{86}Sr}\right)_0$ (l’ordonnée à l’origine). On cherche à isoler $t$ :

$$t = \frac{\ln(a+1)}{\lambda}$$

où $a$ est le coefficient directeur de l’isochrone et $\lambda$ la constante de désintégration du $^{87}Rb$ en $^{87}Sr$ ($1{,}42 \times 10^{-11}\ \text{an}^{-1}$).



[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://isochrone-rb-sr.streamlit.app/)
