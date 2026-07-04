"""
Module de bilan de liaison (Link Budget) pour le dimensionnement couverture NG-RAN 5G.

Etapes :
1. Calcul de l'EIRP de la station de base (gNB)
2. Calcul de la sensibilite du recepteur (UE)
3. Calcul du MAPL (Maximum Allowable Path Loss)
4. Inversion du modele de propagation -> rayon de cellule
5. Calcul de la surface couverte par site (configuration tri-sectorielle)
6. Nombre de sites necessaires pour la couverture
"""

import math
from propagation import get_cell_radius

THERMAL_NOISE_DENSITY_DBM_HZ = -174.0  # kT0, bruit thermique a temperature ambiante


def compute_eirp(ptx_dbm, antenna_gain_dbi, cable_loss_db):
    """EIRP (dBm) = Puissance TX + Gain antenne - Pertes cables/connecteurs"""
    return ptx_dbm + antenna_gain_dbi - cable_loss_db


def compute_receiver_sensitivity(bandwidth_mhz, noise_figure_db, required_sinr_db):
    """
    Sensibilite du recepteur (dBm) = Bruit thermique total + Facteur de bruit + SINR requis

    Bruit thermique total (dBm) = -174 + 10*log10(BW en Hz)
    """
    bandwidth_hz = bandwidth_mhz * 1e6
    thermal_noise_total = THERMAL_NOISE_DENSITY_DBM_HZ + 10 * math.log10(bandwidth_hz)
    sensitivity = thermal_noise_total + noise_figure_db + required_sinr_db
    return sensitivity


def compute_mapl(eirp_dbm, sensitivity_dbm, shadow_margin_db, penetration_loss_db, body_loss_db):
    """
    MAPL (Maximum Allowable Path Loss) en dB
    = EIRP - Sensibilite - Marge de shadowing - Pertes de penetration - Pertes corporelles
    """
    return eirp_dbm - sensitivity_dbm - shadow_margin_db - penetration_loss_db - body_loss_db


def compute_cell_area_trisector(radius_m):
    """
    Surface couverte par un site tri-sectoriel (hexagone regulier approxime).
    Formule standard : Area = (3*sqrt(3)/2) * R^2  approx 2.598 * R^2
    Convertit en km^2 (R en metres -> surface en m^2 / 1e6)
    """
    area_m2 = (3 * math.sqrt(3) / 2) * (radius_m ** 2)
    return area_m2 / 1e6  # km^2


def dimension_coverage(params):
    """
    Effectue le dimensionnement couverture complet a partir d'un dictionnaire de parametres.
    Retourne un dictionnaire de resultats intermediaires et finaux.
    """
    eirp = compute_eirp(params["ptx_dbm"], params["antenna_gain_dbi"], params["cable_loss_db"])

    sensitivity = compute_receiver_sensitivity(
        params["bandwidth_mhz"], params["noise_figure_db"], params["required_sinr_db"]
    )

    mapl = compute_mapl(
        eirp, sensitivity, params["shadow_margin_db"],
        params["penetration_loss_db"], params["body_loss_db"]
    )

    radius_m = get_cell_radius(
        params["environment"], mapl, params["frequency_ghz"],
        params["h_ut_m"], params["h_bs_m"]
    )

    cell_area_km2 = compute_cell_area_trisector(radius_m)

    if cell_area_km2 > 0:
        nb_sites_coverage = math.ceil(params["zone_area_km2"] / cell_area_km2)
    else:
        nb_sites_coverage = float("inf")

    return {
        "eirp_dbm": eirp,
        "sensitivity_dbm": sensitivity,
        "mapl_db": mapl,
        "cell_radius_m": radius_m,
        "cell_area_km2": cell_area_km2,
        "nb_sites_coverage": nb_sites_coverage,
    }
