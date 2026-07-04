"""
Module de dimensionnement capacite pour le NG-RAN 5G.

Methode :
1. Estimation du nombre d'utilisateurs actifs en heure de pointe dans la zone
2. Estimation de la demande totale en debit (DL)
3. Calcul de la capacite offerte par cellule (bande passante x efficacite spectrale)
4. Calcul de la capacite offerte par site (x nombre de secteurs)
5. Nombre de sites necessaires pour la capacite = demande totale / capacite par site
"""

import math


def compute_active_users(zone_area_km2, population_density_km2, penetration_rate_pct, active_ratio_pct):
    """
    Nombre d'utilisateurs actifs simultanes en heure de pointe.

    Population totale = densite x surface
    Utilisateurs 5G = Population totale x taux de penetration
    Utilisateurs actifs (heure de pointe) = Utilisateurs 5G x ratio d'activite
    """
    total_population = zone_area_km2 * population_density_km2
    users_5g = total_population * (penetration_rate_pct / 100.0)
    active_users = users_5g * (active_ratio_pct / 100.0)
    return total_population, users_5g, active_users


def compute_total_demand_mbps(active_users, avg_throughput_per_user_mbps):
    """Demande totale en debit (Mbps) en heure de pointe, sur la liaison descendante (DL)."""
    return active_users * avg_throughput_per_user_mbps


def compute_cell_capacity_mbps(bandwidth_mhz, spectral_efficiency_bps_hz):
    """
    Capacite offerte par cellule/secteur (Mbps) = Bande passante (Hz) x Efficacite spectrale (bps/Hz)
    Resultat converti en Mbps.
    """
    bandwidth_hz = bandwidth_mhz * 1e6
    capacity_bps = bandwidth_hz * spectral_efficiency_bps_hz
    return capacity_bps / 1e6


def dimension_capacity(params):
    """
    Effectue le dimensionnement capacite complet a partir d'un dictionnaire de parametres.
    """
    total_pop, users_5g, active_users = compute_active_users(
        params["zone_area_km2"], params["population_density_km2"],
        params["penetration_rate_pct"], params["active_ratio_pct"]
    )

    total_demand_mbps = compute_total_demand_mbps(active_users, params["avg_throughput_per_user_mbps"])

    cell_capacity_mbps = compute_cell_capacity_mbps(
        params["bandwidth_mhz"], params["spectral_efficiency_bps_hz"]
    )

    site_capacity_mbps = cell_capacity_mbps * params["nb_sectors"]

    if site_capacity_mbps > 0:
        nb_sites_capacity = math.ceil(total_demand_mbps / site_capacity_mbps)
    else:
        nb_sites_capacity = float("inf")

    return {
        "total_population": total_pop,
        "users_5g": users_5g,
        "active_users": active_users,
        "total_demand_mbps": total_demand_mbps,
        "cell_capacity_mbps": cell_capacity_mbps,
        "site_capacity_mbps": site_capacity_mbps,
        "nb_sites_capacity": nb_sites_capacity,
    }
