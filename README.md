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
├── data/                                      # Datasets nettoyés et prêts à l'emploi (sur GitHub)
│   ├── fed_funds_futures_history.csv          # Historique COMPLET Fed Funds (181 067 lignes, 228 contrats, 2010-2028)
│   ├── sofr_futures_history.csv               # Historique COMPLET SOFR 3 mois (50 509 lignes, 43 contrats, 2018-2028)
│   ├── eurodollar_futures_history.csv         # Historique COMPLET Eurodollar (138 064 lignes, 54 contrats, 2010-2023)
│   ├── wirp_historical_snapshots.csv          # Snapshots WIRP historiques sur 6 cycles Fed (2015 à 2026)
│   ├── wirp_snapshots_2026.csv                # Snapshots WIRP actuels des 18 prochaines réunions FOMC
│   ├── macro_surprises_clean.csv              # Historique COMPLET des surprises macro (3 241 dates, 1990-2026)
│   ├── treasury_2y_yield.csv                  # Historique COMPLET Taux 2 ans US (9 602 jours, 1990-2026)
│   ├── reference_rates_bloomberg.csv          # Taux de référence quotidiens Bloomberg (EFFR & SOFR, 1990-2026)
│   ├── fed_rates.csv                          # Historique corridor Fed & EFFR (FRED 2015-2026)
│   ├── fomc_calendar.csv                      # Calendrier officiel des réunions FOMC (2024-2026)
│   └── fomc_events_history_1990_2026.csv      # Historique des annonces FOMC depuis 1990
├── notebooks/
│   ├── 01_fedwatch_model_erian.ipynb          # Notebook Erian (CME FedWatch)
│   ├── 02_wirp_comparison_ouiam.ipynb         # Notebook Ouiam (WIRP vs FedWatch)
│   ├── 03_historical_reconstruction_justine.ipynb # Notebook Justine (Historique)
│   ├── 04_sofr_fomc_analysis_assunta.ipynb             # Notebook Assunta (SOFR)
│   └── 05_macro_repricing_yasmine.ipynb       # Notebook Yasmine (Surprises Macro)
├── src/
│   ├── __init__.py
│   ├── fed_data.py                            # Téléchargement FRED (EFFR, corridor)
│   ├── futures_math.py                        # Décomposition futures avant/après FOMC
│   └── probabilities.py                       # Calcul des probabilités de décision
├── requirements.txt                           # Dépendances Python du projet
└── README.md
```

---

## 📊 Dictionnaire des Données Historiques Complètes

Afin de répondre rigoureusement aux exigences de M. Grasselli (reproduction des anticipations de marché sur les cycles passés, reconstruction à $t-30, t-7, t-1$, et analyses d'event study), **l'intégralité des séries temporelles historiques extraites du terminal Bloomberg a été compilée en fichiers CSV complets et légers** :

### 1. `fed_funds_futures_history.csv` (181 067 lignes — 228 contrats)
* **Période :** **2010 à 2028**.
* **Contenu :** L'ensemble des 228 contrats mensuels 30-Day Federal Funds futures (`FFF10` à `FFZ28`).
* **Colonnes :** `date`, `px_last`, `px_settle`, `px_volume`, `open_interest`, `contract`.
* **Usage :** Indispensable pour Justine (Mission 3) pour reconstruire les anticipations de marché à $t-30, t-7, t-1$ jours de n'importe quelle réunion FOMC passée (2015, 2018, 2020, 2022, 2024).

### 2. `sofr_futures_history.csv` (50 509 lignes — 43 contrats)
* **Période :** **2018 à 2028** (Depuis le lancement de SOFR sur le CME).
* **Contenu :** Tous les contrats trimestriels SOFR 3 mois (`SFRM18` à `SFRZ28`).
* **Colonnes :** `date`, `px_last`, `px_settle`, `px_volume`, `open_interest`, `contract`.
* **Usage :** Indispensable pour Assunta (Mission 4) pour analyser la dynamique de terme et le saut de politique monétaire selon Acosta, Brennan & Jacobson (2024).

### 3. `eurodollar_futures_history.csv` (138 064 lignes — 54 contrats)
* **Période :** **2010 à 2023** (Jusqu'à la fin du LIBOR).
* **Contenu :** Tous les contrats trimestriels Eurodollar futures de 2010 à 2023 (`EDH10` à `EDM23`).
* **Colonnes :** `date`, `px_last`, `px_settle`, `px_volume`, `open_interest`, `contract`.
* **Usage :** Permet la continuité historique pré-2022 avant la bascule vers SOFR (Acosta et al.).

### 4. `wirp_historical_snapshots.csv` (78 réunions sur 6 cycles Fed)
* **Période :** **2015 à 2026**.
* **Contenu :** Snapshots historiques réels de Bloomberg `WIRP <GO>` capturés aux dates charnières :
  - `2015-01-02` : Premier cycle de normalisation post-crise.
  - `2018-01-02` : Cycle de resserrement (taux à 1.50%).
  - `2020-01-02` : Anticipations pré-COVID.
  - `2021-12-31` : Veille du grand choc inflationniste (taux à 0.25%).
  - `2024-12-31` : Cycle de baisse des taux (taux à 4.50%).
  - `2026-11-17` : Cycle actuel sous Kevin Warsh (taux à 4.00%).
* **Colonnes :** `asof_pricing_date`, `fomc_meeting_date`, `target_rate_pct`, `effective_rate_pct`, `implied_rate_pct`, `expected_change_bp`, `priced_moves`, `prob_move_pct`.
* **Usage :** Ouiam (Mission 2) & Erian (Mission 1) pour comparer l'évolution des probabilités WIRP vs FedWatch dans le passé.

### 5. `macro_surprises_clean.csv` (3 241 dates — 1990 à 2026)
* **Période :** **1990 à 2026** (36 ans d'historique macro).
* **Contenu :** Toutes les publications officielles pour CPI, Core CPI, Non-Farm Payrolls, et Taux de chômage, avec les valeurs réelles (`actual`), le consensus médian Bloomberg (`survey_median`) et la surprise brute calculée (`surprise`).
* **Usage :** Yasmine (Mission 5) pour les régressions Healy & Jia (2024).

### 6. `treasury_2y_yield.csv` (9 602 jours — 1990 à 2026)
* **Période :** **1990 à 2026**.
* **Contenu :** Taux actuariel quotidien du bon du Trésor US à 2 ans (`yield_2y_pct`).
* **Usage :** Yasmine (Mission 5) comme variable dépendante de réaction de la politique monétaire.

---

## 🚀 Prise en main rapide

```python
import pandas as pd

# 1. Historique complet des Fed Funds (2010-2028) :
df_ff = pd.read_csv('data/fed_funds_futures_history.csv')

# 2. Snapshots WIRP historiques sur tous les cycles :
df_wirp_hist = pd.read_csv('data/wirp_historical_snapshots.csv')

# 3. Surprises macroéconomiques (1990-2026) :
df_macro = pd.read_csv('data/macro_surprises_clean.csv')
```
