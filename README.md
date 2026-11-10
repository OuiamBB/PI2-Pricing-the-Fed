# Pricing the Fed: Extracting Monetary Policy Expectations from Market Data

**ESILV — Majeure Ingénierie Financière (IF-A5) — Projet d'Innovation Industrielle (PI²)**  
**Projet :** P153_T2  
**Tuteur Référent :** M. Martino Grasselli (DVHE)  

---

## 👥 Équipe Projet

| Membre | Rôle | Mission Technique Principale |
| :--- | :--- | :--- |
| **Ouiam BOUSSAID BENCHAARA** | **Team Referent** | **Mission 2 :** Analyse Bloomberg WIRP, corridor Fed et comparaison méthodologique |
| **Erian STANLEY YOGARAJ** | Membre | **Mission 1 :** Reproduction de CME FedWatch (formules, probabilités 2 états et arbre) |
| **Justine RENAUD** | Membre | **Mission 3 :** Reconstruction historique des anticipations à $t-30, t-7, t-1$ jours |
| **Assunta DAMIANO** | Membre | **Mission 4 :** SOFR / Eurodollar et révision de la courbe lors des annonces FOMC |
| **Yasmine PERALDI** | Membre | **Mission 5 :** Surprises macroéconomiques (CPI, NFP) et régressions d'event study |

---

## 📂 Architecture du Projet

```text
PI2-Pricing-the-Fed/
├── data/
│   ├── fomc_calendar.csv                 # Calendrier des réunions FOMC (2024-2026)
│   └── README.md                         # Conventions de nommage et unités
├── notebooks/
│   ├── 01_fedwatch_model_erian.ipynb     # Notebook Erian (CME FedWatch)
│   ├── 02_wirp_comparison_ouiam.ipynb    # Notebook Ouiam (WIRP vs FedWatch)
│   ├── 03_historical_reconstruction_justine.ipynb # Notebook Justine (Historique)
│   ├── 04_sofr_fomc_analysis_assunta.ipynb        # Notebook Assunta (SOFR)
│   └── 05_macro_repricing_yasmine.ipynb  # Notebook Yasmine (Surprises Macro)
├── src/
│   ├── __init__.py
│   ├── fed_data.py                       # Téléchargement FRED (EFFR, corridor)
│   ├── futures_math.py                   # Décomposition futures avant/après FOMC
│   └── probabilities.py                  # Calcul des probabilités de décision
├── requirements.txt                      # Dépendances Python du projet
└── README.md
```

---

## 🚀 Prise en main rapide

### 1. Cloner le projet
```bash
git clone https://github.com/OuiamBB/PI2-Pricing-the-Fed.git
cd PI2-Pricing-the-Fed
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Lancer Jupyter
```bash
jupyter notebook
```
Chaque membre travaille directement dans son notebook assigné dans le dossier `notebooks/`.

---

## 📏 Règles communes pour les données et le code
- **Dates** : Format ISO `YYYY-MM-DD`.
- **Niveaux de taux** : Pourcentages (ex. `4.25` pour `4.25%`).
- **Variations de taux** : Points de base (ex. `25` pour `25 bp`).
- **Probabilités** : Décimales entre `0` et `1` (ex. `0.60` pour `60%`).
- **Chemins** : Utilisez toujours des chemins relatifs (`../data/...` ou `src/...`) afin que le code fonctionne chez tous les membres de l'équipe.
