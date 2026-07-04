# Application de dimensionnement NG-RAN 5G

Application Python (interface Tkinter) realisant le dimensionnement de la partie
radio (NG-RAN) d'un reseau 5G en bande sub-6 GHz (n78, 3.5 GHz), selon les deux
approches classiques : **couverture** (link budget) et **capacite**.

## 1. Structure du projet

```
ngran_dimensioning/
|-- main.py          # Interface graphique Tkinter (point d'entree)
|-- propagation.py   # Modeles de propagation 3GPP TR 38.901 (UMa / UMi NLOS)
|-- link_budget.py   # Bilan de liaison + dimensionnement couverture
|-- capacity.py       # Dimensionnement capacite
|-- README.md
```

## 2. Lancer l'application

Prerequis : Python 3.8+ avec Tkinter (inclus par defaut sur la plupart des
distributions ; sous Linux Debian/Ubuntu, si absent : `sudo apt install python3-tk`).

```bash
cd ngran_dimensioning
python3 main.py
```

## 3. Methodologie

### 3.1 Dimensionnement couverture (Link Budget)

1. **EIRP** = Puissance d'emission (dBm) + Gain antenne (dBi) - Pertes cables (dB)
2. **Sensibilite recepteur** = Bruit thermique total + Facteur de bruit + SINR requis
   - Bruit thermique total (dBm) = -174 + 10*log10(Bande passante en Hz)
3. **MAPL** (Maximum Allowable Path Loss) = EIRP - Sensibilite - Marges (shadowing,
   penetration, corps humain)
4. **Rayon de cellule** : inversion du modele de propagation **3GPP TR 38.901**
   (UMa ou UMi, NLOS) a partir du MAPL
5. **Surface par site** (configuration tri-sectorielle) = (3*sqrt(3)/2) * R^2
6. **Nombre de sites (couverture)** = Surface de la zone cible / Surface par site

### 3.2 Dimensionnement capacite

1. Population active 5G = Densite de population x Surface x Taux de penetration x
   Ratio d'utilisateurs actifs en heure de pointe
2. Demande totale en debit (DL) = Utilisateurs actifs x Debit moyen demande par
   utilisateur
3. Capacite par secteur = Bande passante (Hz) x Efficacite spectrale (bps/Hz)
4. Capacite par site = Capacite par secteur x Nombre de secteurs
5. **Nombre de sites (capacite)** = Demande totale / Capacite par site

### 3.3 Resultat final

Nombre de sites retenu = **max**(Nombre de sites couverture, Nombre de sites capacite)

Le critere dimensionnant (couverture ou capacite) est indique dans les resultats :
en zone tres dense, c'est generalement la capacite qui domine ; en zone peu dense,
c'est la couverture.

## 4. Justification des parametres d'entree par defaut

| Parametre | Valeur par defaut | Justification |
|---|---|---|
| Frequence porteuse | 3.5 GHz (bande n78) | Bande pionniere 5G sub-6 GHz la plus deployee au monde, bon compromis couverture/capacite |
| Environnement | UMa (Urban Macro) | Modele 3GPP recommande pour sites macro en zone urbaine, coherent avec les pylones de 45 m existants |
| Bande passante | 100 MHz | Largeur de canal type pour un operateur disposant d'un bloc n78 standard |
| Puissance gNB | 49 dBm (~80 W) | Puissance totale rayonnee typique d'un equipement macro 5G multi-antennes |
| Gain antenne | 17 dBi | Valeur usuelle d'une antenne active AAS (Active Antenna System) sub-6 GHz |
| Pertes cables | 2 dB | Pertes feeder/connecteurs reduites grace aux radios distantes (RRH/AAU) montees au sommet du pylone |
| Facteur de bruit UE | 7 dB | Valeur typique d'un recepteur smartphone 5G |
| SINR requis | -2 dB | SINR cible en bord de cellule pour un service garanti (debit minimal, modulation robuste QPSK) |
| Marge de shadowing | 6 dB | Marge standard pour un environnement urbain avec obstacles (batiments) |
| Pertes de penetration | 15 dB | Penetration legere (fenetre, vehicule) ; mettre 20 dB si on cible une couverture indoor profonde |
| Pertes corporelles | 3 dB | Perte standard due a la proximite du corps humain (UE tenu en main) |
| Hauteur antenne gNB | 25 m | Coherente avec un pylone urbain (inferieure aux 45 m du pylone car hauteur effective rayonnante) |
| Hauteur UE | 1.5 m | Hauteur standard d'un terminal utilise a hauteur d'homme |
| Densite de population | 8000 hab/km2 | Ordre de grandeur d'un quartier urbain dense (similaire a un centre-ville africain) |
| Taux de penetration 5G | 30 % | Hypothese d'adoption progressive en phase de deploiement |
| Ratio actifs heure de pointe | 5 % | Valeur usuelle en dimensionnement (Busy Hour) |
| Debit moyen par utilisateur | 20 Mbps DL | Cible eMBB moderee (video HD, navigation) |
| Efficacite spectrale | 5 bps/Hz | Valeur moyenne realiste cellule (MIMO 4x4, mix de conditions radio) |
| Nombre de secteurs | 3 | Configuration tri-sectorielle standard d'un site macro |

**Tous ces parametres sont modifiables directement dans l'interface** avant de
lancer le calcul, afin de tester plusieurs scenarios (sensibilite aux parametres).

## 5. Limites et ameliorations possibles

- Le modele 3GPP 38.901 utilise est le cas NLOS (le plus defavorable et le plus
  realiste en environnement urbain dense avec obstruction).
- L'efficacite spectrale est ici un parametre moyen fixe ; une version avancee
  pourrait la deriver dynamiquement de la formule de Shannon a partir du SINR
  moyen et d'un facteur d'efficacite d'implementation.
- Le modele ne distingue pas encore les terminaux indoor/outdoor (un mix pourrait
  etre ajoute en ponderant deux jeux de pertes de penetration).
