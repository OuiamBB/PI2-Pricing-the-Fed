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
├── data/                                 # Datasets nettoyés et prêts à l'emploi (sur GitHub)
│   ├── fomc_calendar.csv                 # Calendrier officiel des réunions FOMC (2024-2026)
│   ├── fed_rates.csv                     # Historique corridor Fed & EFFR (FRED 2015-2026)
│   ├── reference_rates_bloomberg.csv     # Taux de référence EFFR & SOFR (Bloomberg)
│   ├── wirp_snapshots_2026.csv           # Snapshots des 18 prochaines réunions FOMC (Bloomberg WIRP)
│   ├── fed_funds_recent_contracts.csv    # Cours journaliers des contrats Fed Funds (FFV26 à FFZ27)
│   ├── sofr_futures_recent.csv           # Cours journaliers des contrats SOFR 3 mois (SFRU26 à SFRZ27)
│   ├── macro_surprises_clean.csv         # Surprises macro (CPI, Core CPI, NFP, Chômage: Actual vs Survey)
│   ├── treasury_2y_yield.csv             # Rendement journalier du bon du Trésor US à 2 ans (1990-2026)
│   └── README.md                         # Dictionnaire des données et méthodologie de nettoyage
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

## 📊 Dictionnaire des Données : Sources et Nettoyage (Data Pipeline)

Afin d'éviter tout bug dans les notebooks et d'assurer une exécution ultra-rapide (< 0.1s), les extractions brutes volumineuses issues du terminal Bloomberg (fichiers `.xlsx` de plus de 400 onglets conservés en archive locale) ont été converties en **fichiers CSV propres, normalisés et légers**, directement utilisables par toute l'équipe :

### 1. `wirp_snapshots_2026.csv`
* **Source :** Bloomberg Terminal — fonction `WIRP <GO>` (World Interest Rate Probability).
* **Contenu :** Snapshots des 18 prochaines réunions de la Fed (décembre 2026 à janvier 2028). Comprend le taux de référence actuel (4.00% target / 3.88% EFFR), le taux implicite (*implied rate*), le nombre de hausses/baisses anticipées (*priced moves*), et les probabilités calculées sous les deux modèles : **Futures Fed Funds** (`US_FUT`) et **OIS** (`US_OIS`).
* **Nettoyage appliqué :** Extraction de la table clean Bloomberg, standardisation des en-têtes en minuscules snake_case, formatage des dates en ISO `YYYY-MM-DD`, et conversion des variations de taux en points de base (`implied_rate_change_bp`).
* **Utilisateurs :** Ouiam (Mission 2) & Erian (Mission 1).

### 2. `fed_funds_recent_contracts.csv`
* **Source :** Bloomberg Terminal — extraction des contrats 30-Day Federal Funds futures (`FFV26`, `FFX26`, `FFZ26`, `FFF27`, `FFG27`, `FFH27`, `FFM27`, `FFU27`, `FFZ27`).
* **Contenu :** Historique journalier complet des cours pour chaque contrat mensuel : dernier prix (`px_last`), cours de règlement (`px_settle`), volume (`px_volume`) et positions ouvertes (`open_interest`).
* **Nettoyage appliqué :** Élimination des 5 premières lignes de métadonnées Bloomberg (*Header & spill area*), suppression des lignes sans cotation, typage strict des dates et prix, et empilement vertical (*concat*) avec colonne d'identification `contract`.
* **Utilisateurs :** Erian (Mission 1) & Justine (Mission 3).

### 3. `reference_rates_bloomberg.csv` & `fed_rates.csv`
* **Sources :** Bloomberg Terminal (`Reference_Rates_COMPLETE_1990_2026.xlsx`) et Federal Reserve Bank of St. Louis (FRED).
* **Contenu :** Séries quotidiennes officielles des taux de référence :
  - `effr` : Effective Federal Funds Rate (taux interbancaire non garanti).
  - `sofr` : Secured Overnight Financing Rate (taux repo collatéralisé en bons du Trésor).
  - `target_upper`, `target_lower`, `target_midpoint` : Fourchette cible fixée par le FOMC.
* **Nettoyage appliqué :** Alignement temporel des séries sur le calendrier ouvré US, suppression des métadonnées, suppression des doublons, et calcul de l'écart historique `effr_midpoint_spread_bp = (effr - target_midpoint) * 100`.
* **Utilisateurs :** TOUT LE GROUPE (Fondation commune).

### 4. `sofr_futures_recent.csv`
* **Source :** Bloomberg Terminal — contrats trimestriels 3-Month SOFR futures (`SFRU26`, `SFRZ26`, `SFRH27`, `SFRM27`, `SFRU27`, `SFRZ27`).
* **Contenu :** Prix journaliers des 3e, 4e et 5e contrats de référence, au cœur de la méthodologie d'Acosta, Brennan et Jacobson (2024).
* **Nettoyage appliqué :** Suppression des en-têtes terminaux, typage des cours de règlement et volumes, indexation par contrat et date.
* **Utilisateurs :** Assunta (Mission 4).

### 5. `macro_surprises_clean.csv`
* **Source :** Bloomberg Terminal — calendrier économique `ECO <GO>` et consensus d'analystes.
* **Contenu :** Données des annonces macroéconomiques clés :
  - `CPI_MOM` & `CORE_CPI_MOM` (Inflation globale et sous-jacente mensuelle).
  - `NFP` (Non-Farm Payrolls - créations d'emplois non agricoles).
  - `UNEMPLOYMENT` (Taux de chômage US).
  - Colonnes : `actual` (valeur officielle publiée), `survey_median` (consensus médian Bloomberg pré-publication), `surprise` ($A - E$).
* **Nettoyage appliqué :** Concaténation des indicateurs, conversion numérique des surprises, harmonisation des dates de publication à 8h30 (heure de New York).
* **Utilisateurs :** Yasmine (Mission 5).

### 6. `treasury_2y_yield.csv`
* **Source :** Bloomberg Terminal — ticker `USGG2YR Index`.
* **Contenu :** Rendement quotidien du bon du Trésor américain à 2 ans (1990–2026).
* **Nettoyage appliqué :** Nettoyage de l'en-tête Bloomberg, suppression des jours fériés sans cotation, renommage explicite de la colonne de rendement `yield_2y_pct`.
* **Utilisateurs :** Yasmine (Mission 5) — variable dépendante pour les régressions de politique monétaire (Healy & Jia 2024).

### 7. `fomc_calendar.csv`
* **Source :** Federal Reserve Board.
* **Contenu :** Calendrier officiel des réunions du FOMC (2024-2026) avec dates d'annonce de décision et indicateur `sep_dot_plot` (True pour les réunions de mars, juin, septembre et décembre incluant les projections macroéconomiques).
* **Utilisateurs :** TOUT LE GROUPE (Indispensable pour découper les mois $n_{\text{before}} / n_{\text{after}}$ et caler les fenêtres d'Event Study).

---

## 🚀 Prise en main rapide

### 1. Cloner ou mettre à jour le projet
```bash
git clone https://github.com/OuiamBB/PI2-Pricing-the-Fed.git
cd PI2-Pricing-the-Fed
# Ou si vous l'avez déjà :
git pull origin main
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Exemple de chargement immédiat en Python
```python
import pandas as pd

# 1. Snapshots WIRP de Bloomberg :
df_wirp = pd.read_csv('data/wirp_snapshots_2026.csv')

# 2. Contrats Fed Funds récents :
df_ff = pd.read_csv('data/fed_funds_recent_contracts.csv')

# 3. Surprises macroéconomiques :
df_macro = pd.read_csv('data/macro_surprises_clean.csv')
```

---

## 📏 Règles communes pour les données et le code
- **Dates** : Format ISO `YYYY-MM-DD`.
- **Niveaux de taux** : Pourcentages (ex. `4.25` pour `4.25%`).
- **Variations de taux** : Points de base (ex. `25` pour `25 bp`).
- **Probabilités** : Décimales entre `0` et `1` (ex. `0.60` pour `60%`).
- **Chemins** : Utilisez toujours des chemins relatifs (`../data/...` ou `src/...`) afin que le code fonctionne sur la machine de n'importe quel membre de l'équipe.
