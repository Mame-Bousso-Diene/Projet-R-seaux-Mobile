"""
Module de modeles de propagation - 3GPP TR 38.901
Modeles NLOS Urban Macro (UMa) et Urban Micro / Street Canyon (UMi)
Utilises pour le dimensionnement radio 5G NG-RAN en bande sub-6 GHz.

Reference: 3GPP TR 38.901 v16.1.0, Table 7.4.1-1
"""

import math


def path_loss_uma_nlos(d3d_m, fc_ghz, h_ut_m):
    """
    Path loss UMa NLOS (3GPP 38.901).
    Valide pour d3D dans [10m, 5000m], fc dans [0.5, 100] GHz, h_UT dans [1.5, 22.5] m.

    PL = 13.54 + 39.08*log10(d3D) + 20*log10(fc) - 0.6*(h_UT - 1.5)
    """
    return 13.54 + 39.08 * math.log10(d3d_m) + 20 * math.log10(fc_ghz) - 0.6 * (h_ut_m - 1.5)


def path_loss_umi_nlos(d3d_m, fc_ghz, h_ut_m):
    """
    Path loss UMi Street Canyon NLOS (3GPP 38.901).

    PL = 35.3*log10(d3D) + 22.4 + 21.3*log10(fc) - 0.3*(h_UT - 1.5)
    """
    return 35.3 * math.log10(d3d_m) + 22.4 + 21.3 * math.log10(fc_ghz) - 0.3 * (h_ut_m - 1.5)


def inverse_path_loss_uma(mapl_db, fc_ghz, h_ut_m, h_bs_m):
    """
    Inverse le modele UMa NLOS pour retrouver la distance 2D (rayon de cellule)
    a partir du MAPL (Maximum Allowable Path Loss).

    log10(d3D) = (MAPL - 13.54 - 20*log10(fc) + 0.6*(h_UT-1.5)) / 39.08
    """
    log_d3d = (mapl_db - 13.54 - 20 * math.log10(fc_ghz) + 0.6 * (h_ut_m - 1.5)) / 39.08
    d3d = 10 ** log_d3d
    delta_h = h_bs_m - h_ut_m
    if d3d <= abs(delta_h):
        # Cas degenere : MAPL trop faible pour la difference de hauteur
        return 0.0
    d2d = math.sqrt(d3d ** 2 - delta_h ** 2)
    return d2d


def inverse_path_loss_umi(mapl_db, fc_ghz, h_ut_m, h_bs_m):
    """
    Inverse le modele UMi Street Canyon NLOS pour retrouver la distance 2D.

    log10(d3D) = (MAPL - 22.4 - 21.3*log10(fc) + 0.3*(h_UT-1.5)) / 35.3
    """
    log_d3d = (mapl_db - 22.4 - 21.3 * math.log10(fc_ghz) + 0.3 * (h_ut_m - 1.5)) / 35.3
    d3d = 10 ** log_d3d
    delta_h = h_bs_m - h_ut_m
    if d3d <= abs(delta_h):
        return 0.0
    d2d = math.sqrt(d3d ** 2 - delta_h ** 2)
    return d2d


def get_cell_radius(environment, mapl_db, fc_ghz, h_ut_m, h_bs_m):
    """
    Retourne le rayon de cellule (en metres) selon l'environnement choisi.
    environment: 'UMa' (urbain/suburbain macro) ou 'UMi' (urbain dense, street canyon)
    """
    if environment == "UMa":
        return inverse_path_loss_uma(mapl_db, fc_ghz, h_ut_m, h_bs_m)
    elif environment == "UMi":
        return inverse_path_loss_umi(mapl_db, fc_ghz, h_ut_m, h_bs_m)
    else:
        raise ValueError("Environnement inconnu : choisir 'UMa' ou 'UMi'")
