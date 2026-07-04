# Application de Dimensionnement NG-RAN 5G

> Projet réalisé dans le cadre du cours de **Dimensionnement et Planification des Réseaux Mobiles**  
> **DIEME – LITA / Département Génie Informatique – UCAD**  
> Année universitaire : 2025 – 2026  
> Auteur : **Mame Bousso Diene**

---

##  Description du projet

Cette application Python permet de réaliser automatiquement le **dimensionnement de la partie radio NG-RAN (Next Generation Radio Access Network) de la 5G** en bande **sub-6 GHz (n78 – 3,5 GHz)**.

Elle couvre les deux approches classiques du dimensionnement radio :

- **Dimensionnement couverture** : calcul du bilan de liaison (Link Budget) → MAPL → inversion du modèle de propagation 3GPP TR 38.901 (UMa NLOS) → rayon de cellule → surface couverte par site → nombre de sites nécessaires.
- **Dimensionnement capacité** : calcul de la demande totale en débit (DL) des utilisateurs actifs en heure de pointe → capacité offerte par site → nombre de sites nécessaires.

Le **nombre de sites retenu** est le maximum entre les deux approches (couverture et capacité).

---

##  Structure du projet

    ngran_dimensioning/
    │
    ├── main.py            # Interface graphique Tkinter (point d'entrée de l'application)
    ├── propagation.py     # Modèles de propagation 3GPP TR 38.901 (UMa / UMi NLOS) + inversion
    ├── link_budget.py     # Calcul du bilan de liaison et dimensionnement couverture
    ├── capacity.py        # Calcul de la demande en débit et dimensionnement capacité
    └── README.md          # Documentation du projet

---

##  Prérequis

- **Python 3.8 ou supérieur** — téléchargeable sur [python.org](https://www.python.org/downloads/)
- **Tkinter** — inclus automatiquement avec l'installeur officiel Python sur Windows

>  Lors de l'installation de Python sur Windows, cochez bien la case **"Add python.exe to PATH"** en bas de la première fenêtre d'installation.

Aucune bibliothèque externe n'est requise — l'application utilise uniquement des modules Python standards (`math`, `tkinter`).

---

##  Installation et lancement

### 1. Cloner le dépôt

    git clone https://github.com/Mame-Bousso-Diene/Projet-R-seaux-Mobile.git

Ou téléchargez directement le ZIP depuis GitHub en cliquant sur **Code → Download ZIP**.

### 2. Accéder au dossier du projet

    cd Projet-R-seaux-Mobile

### 3. Lancer l'application

    python main.py

>  Une fenêtre graphique s'ouvre avec le formulaire de dimensionnement.

---

##  Utilisation de l'application

### Étape 1 – Paramètres de couverture (Section 1)

| Paramètre | Valeur par défaut | Description |
|---|---|---|
| Fréquence porteuse (GHz) | 3,5 | Bande n78 sub-6 GHz |
| Environnement | UMa | Urban Macro – zone urbaine dense |
| Surface de la zone cible (km²) | 10 | Surface à couvrir |
| Bande passante (MHz) | 100 | Largeur de canal n78 |
| Puissance d'émission gNB (dBm) | 49 | Puissance TX du gNodeB |
| Gain antenne (dBi) | 17 | Antenne active AAS |
| Pertes câbles/connecteurs (dB) | 2 | Pertes feeder |
| Facteur de bruit UE (dB) | 7 | Récepteur smartphone 5G |
| SINR requis en bord de cellule (dB) | -2 | Modulation QPSK robuste |
| Marge de shadowing (dB) | 6 | Variations lentes du signal |
| Pertes de pénétration (dB) | 15 | Pénétration bâtiment légère |
| Pertes corporelles (dB) | 3 | Absorption corps humain |
| Hauteur antenne gNB (m) | 25 | Hauteur effective rayonnante |
| Hauteur UE (m) | 1,5 | Terminal à hauteur d'homme |

### Étape 2 – Paramètres de capacité (Section 2)

| Paramètre | Valeur par défaut | Description |
|---|---|---|
| Densité de population (hab/km²) | 8000 | Zone urbaine dense |
| Taux de pénétration 5G (%) | 30 | Adoption progressive |
| Ratio d'utilisateurs actifs (%) | 5 | Heure de pointe (Busy Hour) |
| Débit moyen DL par utilisateur (Mbps) | 20 | Cible eMBB (vidéo HD, 4K) |
| Efficacité spectrale (bps/Hz) | 5 | MIMO 4×4 en conditions moyennes |
| Nombre de secteurs par site | 3 | Configuration tri-sectorielle |

### Étape 3 – Calculer
Cliquez sur le bouton **« Calculer le dimensionnement »**.

### Étape 4 – Lire les résultats
Les résultats s'affichent en trois blocs :
1. **Dimensionnement couverture** : EIRP, sensibilité, MAPL, rayon de cellule, surface par site, nombre de sites
2. **Dimensionnement capacité** : population, utilisateurs actifs, demande totale, capacité par site, nombre de sites
3. **Synthèse finale** : nombre de sites retenu et critère dimensionnant (couverture ou capacité)

---

##  Méthodologie et formules

### Modèle de propagation : 3GPP TR 38.901 (UMa NLOS)

    PL (dB) = 13,54 + 39,08 × log10(d3D) + 20 × log10(fc) − 0,6 × (hUE − 1,5)

Ce modèle est valide de **0,5 à 100 GHz** et recommandé par le 3GPP pour les déploiements 5G NR.

### Bilan de liaison

    MAPL = EIRP − Sensibilité − Marge shadowing − Pertes pénétration − Pertes corporelles
    EIRP (dBm)        = Puissance TX + Gain antenne − Pertes câbles
    Sensibilité (dBm) = −174 + 10×log10(BW en Hz) + Facteur de bruit + SINR requis

### Surface couverte par site (tri-sectoriel)

    Aire (km²) = (3 × √3 / 2) × R²  /  1 000 000

### Nombre de sites

    Nombre de sites = max(sites couverture, sites capacité)

---

##  Exemple de résultats (valeurs par défaut)

| Indicateur | Valeur |
|---|---|
| EIRP | 64,00 dBm |
| Sensibilité récepteur | −89,00 dBm |
| MAPL | 129,00 dB |
| Rayon de cellule | 473,7 m |
| Surface par site | 0,583 km² |
| Nombre de sites (couverture) | **18 sites** |
| Demande totale DL | 24 000 Mbps |
| Capacité par site | 1 500 Mbps |
| Nombre de sites (capacité) | **16 sites** |
| **Nombre de sites retenu** | **18 sites (critère : Couverture)** |

---

