"""
Application de dimensionnement NG-RAN 5G
Interface graphique Tkinter

Auteur : (a completer)
Cadre : Projet Dimensionnement et Planification - 5G NG-RAN
"""

import tkinter as tk
from tkinter import ttk, messagebox

from link_budget import dimension_coverage
from capacity import dimension_capacity


class NGRANDimensioningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dimensionnement NG-RAN 5G")
        self.root.geometry("980x720")

        # --- Conteneur scrollable ---
        container = ttk.Frame(root)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, borderwidth=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scroll_frame = ttk.Frame(canvas)

        self.scroll_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.entries = {}
        self._build_ui()

    # ------------------------------------------------------------------
    def _add_section(self, parent, title):
        label = ttk.Label(parent, text=title, font=("Helvetica", 12, "bold"))
        label.pack(anchor="w", pady=(15, 5), padx=10)
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=10)
        return frame

    def _add_field(self, frame, row, key, label_text, default_value, widget="entry", values=None):
        ttk.Label(frame, text=label_text).grid(row=row, column=0, sticky="w", pady=3, padx=5)
        if widget == "entry":
            var = tk.StringVar(value=str(default_value))
            entry = ttk.Entry(frame, textvariable=var, width=15)
            entry.grid(row=row, column=1, sticky="w", pady=3, padx=5)
            self.entries[key] = var
        elif widget == "combo":
            var = tk.StringVar(value=default_value)
            combo = ttk.Combobox(frame, textvariable=var, values=values, width=20, state="readonly")
            combo.grid(row=row, column=1, sticky="w", pady=3, padx=5)
            self.entries[key] = var

    # ------------------------------------------------------------------
    def _build_ui(self):
        title = ttk.Label(
            self.scroll_frame,
            text="Application de dimensionnement NG-RAN 5G (bande sub-6 GHz, n78 - 3.5 GHz)",
            font=("Helvetica", 14, "bold"), wraplength=900, justify="center"
        )
        title.pack(pady=10)

        # ===================== SECTION COUVERTURE =====================
        cov_frame = self._add_section(self.scroll_frame, "1. Parametres de couverture (Link Budget)")

        self._add_field(cov_frame, 0, "frequency_ghz", "Frequence porteuse (GHz)", 3.5)
        self._add_field(cov_frame, 1, "environment", "Environnement", "UMa",
                         widget="combo", values=["UMa", "UMi"])
        self._add_field(cov_frame, 2, "zone_area_km2", "Surface de la zone cible (km2)", 10)
        self._add_field(cov_frame, 3, "bandwidth_mhz", "Bande passante (MHz)", 100)
        self._add_field(cov_frame, 4, "ptx_dbm", "Puissance d'emission gNB (dBm)", 49)
        self._add_field(cov_frame, 5, "antenna_gain_dbi", "Gain antenne (dBi)", 17)
        self._add_field(cov_frame, 6, "cable_loss_db", "Pertes cables/connecteurs (dB)", 2)
        self._add_field(cov_frame, 7, "noise_figure_db", "Facteur de bruit UE (dB)", 7)
        self._add_field(cov_frame, 8, "required_sinr_db", "SINR requis en bord de cellule (dB)", -2)
        self._add_field(cov_frame, 9, "shadow_margin_db", "Marge de shadowing (dB)", 6)
        self._add_field(cov_frame, 10, "penetration_loss_db", "Pertes de penetration (dB)", 15)
        self._add_field(cov_frame, 11, "body_loss_db", "Pertes corporelles (dB)", 3)
        self._add_field(cov_frame, 12, "h_bs_m", "Hauteur antenne gNB (m)", 25)
        self._add_field(cov_frame, 13, "h_ut_m", "Hauteur UE (m)", 1.5)

        # ===================== SECTION CAPACITE =====================
        cap_frame = self._add_section(self.scroll_frame, "2. Parametres de capacite")

        self._add_field(cap_frame, 0, "population_density_km2", "Densite de population (hab/km2)", 8000)
        self._add_field(cap_frame, 1, "penetration_rate_pct", "Taux de penetration 5G (%)", 30)
        self._add_field(cap_frame, 2, "active_ratio_pct", "Ratio d'utilisateurs actifs heure de pointe (%)", 5)
        self._add_field(cap_frame, 3, "avg_throughput_per_user_mbps", "Debit moyen DL par utilisateur (Mbps)", 20)
        self._add_field(cap_frame, 4, "spectral_efficiency_bps_hz", "Efficacite spectrale moyenne (bps/Hz)", 5)
        self._add_field(cap_frame, 5, "nb_sectors", "Nombre de secteurs par site", 3)

        # ===================== BOUTON CALCUL =====================
        btn = ttk.Button(self.scroll_frame, text="Calculer le dimensionnement", command=self.on_calculate)
        btn.pack(pady=15)

        # ===================== ZONE RESULTATS =====================
        result_label = ttk.Label(self.scroll_frame, text="Resultats", font=("Helvetica", 12, "bold"))
        result_label.pack(anchor="w", padx=10)

        self.result_text = tk.Text(self.scroll_frame, height=20, width=110, wrap="word")
        self.result_text.pack(padx=10, pady=10)

    # ------------------------------------------------------------------
    def _get_float(self, key):
        return float(self.entries[key].get())

    def on_calculate(self):
        try:
            coverage_params = {
                "frequency_ghz": self._get_float("frequency_ghz"),
                "environment": self.entries["environment"].get(),
                "zone_area_km2": self._get_float("zone_area_km2"),
                "bandwidth_mhz": self._get_float("bandwidth_mhz"),
                "ptx_dbm": self._get_float("ptx_dbm"),
                "antenna_gain_dbi": self._get_float("antenna_gain_dbi"),
                "cable_loss_db": self._get_float("cable_loss_db"),
                "noise_figure_db": self._get_float("noise_figure_db"),
                "required_sinr_db": self._get_float("required_sinr_db"),
                "shadow_margin_db": self._get_float("shadow_margin_db"),
                "penetration_loss_db": self._get_float("penetration_loss_db"),
                "body_loss_db": self._get_float("body_loss_db"),
                "h_bs_m": self._get_float("h_bs_m"),
                "h_ut_m": self._get_float("h_ut_m"),
            }

            capacity_params = {
                "zone_area_km2": coverage_params["zone_area_km2"],
                "population_density_km2": self._get_float("population_density_km2"),
                "penetration_rate_pct": self._get_float("penetration_rate_pct"),
                "active_ratio_pct": self._get_float("active_ratio_pct"),
                "avg_throughput_per_user_mbps": self._get_float("avg_throughput_per_user_mbps"),
                "bandwidth_mhz": coverage_params["bandwidth_mhz"],
                "spectral_efficiency_bps_hz": self._get_float("spectral_efficiency_bps_hz"),
                "nb_sectors": self._get_float("nb_sectors"),
            }

        except ValueError:
            messagebox.showerror("Erreur de saisie", "Veuillez verifier que tous les champs sont des nombres valides.")
            return

        cov_result = dimension_coverage(coverage_params)
        cap_result = dimension_capacity(capacity_params)

        nb_sites_final = max(cov_result["nb_sites_coverage"], cap_result["nb_sites_capacity"])
        critere = "Couverture" if cov_result["nb_sites_coverage"] >= cap_result["nb_sites_capacity"] else "Capacite"

        self.result_text.delete("1.0", tk.END)
        output = []
        output.append("=" * 90)
        output.append("RESULTATS - DIMENSIONNEMENT COUVERTURE (Link Budget)")
        output.append("=" * 90)
        output.append(f"EIRP                         : {cov_result['eirp_dbm']:.2f} dBm")
        output.append(f"Sensibilite recepteur         : {cov_result['sensitivity_dbm']:.2f} dBm")
        output.append(f"MAPL (perte de parcours max)  : {cov_result['mapl_db']:.2f} dB")
        output.append(f"Rayon de cellule              : {cov_result['cell_radius_m']:.1f} m")
        output.append(f"Surface couverte par site     : {cov_result['cell_area_km2']:.3f} km2 (tri-secteur)")
        output.append(f"Nombre de sites (couverture)  : {cov_result['nb_sites_coverage']}")
        output.append("")
        output.append("=" * 90)
        output.append("RESULTATS - DIMENSIONNEMENT CAPACITE")
        output.append("=" * 90)
        output.append(f"Population totale dans la zone        : {cap_result['total_population']:.0f} habitants")
        output.append(f"Utilisateurs 5G                       : {cap_result['users_5g']:.0f}")
        output.append(f"Utilisateurs actifs (heure de pointe)  : {cap_result['active_users']:.0f}")
        output.append(f"Demande totale en debit (DL)           : {cap_result['total_demand_mbps']:.1f} Mbps")
        output.append(f"Capacite par cellule/secteur            : {cap_result['cell_capacity_mbps']:.1f} Mbps")
        output.append(f"Capacite par site (tri-secteur)         : {cap_result['site_capacity_mbps']:.1f} Mbps")
        output.append(f"Nombre de sites (capacite)              : {cap_result['nb_sites_capacity']}")
        output.append("")
        output.append("=" * 90)
        output.append("SYNTHESE FINALE")
        output.append("=" * 90)
        output.append(f"Nombre de sites retenu  : {nb_sites_final}  (critere dimensionnant : {critere})")

        self.result_text.insert(tk.END, "\n".join(output))


def main():
    root = tk.Tk()
    app = NGRANDimensioningApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
