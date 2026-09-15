import customtkinter as ctk


class PlayerTab(ctk.CTkScrollableFrame):
    """Vista correspondiente a la pestaña de Datos del Jugador"""

    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)

        # Sección 1: Datos del Jugador
        self.lbl_title = ctk.CTkLabel(
            self,
            text="Perfil del Entrenador / Jugador",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#f59e0b"
        )
        self.lbl_title.pack(anchor="w", padx=15, pady=(15, 10))

        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(fill="x", padx=15, pady=5)

        # Nombre del Jugador
        ctk.CTkLabel(grid_frame, text="Nombre del Jugador:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky="w", pady=8, padx=10)
        self.entry_player_name = ctk.CTkEntry(grid_frame, width=220, placeholder_text="Ej: Gary")
        self.entry_player_name.grid(row=0, column=1, sticky="w", pady=8, padx=10)

        # Monedas B-Coins
        ctk.CTkLabel(grid_frame, text="Monedas (B-Coins):", font=ctk.CTkFont(size=14, weight="bold")).grid(row=1, column=0, sticky="w", pady=8, padx=10)
        self.entry_money = ctk.CTkEntry(grid_frame, width=220, placeholder_text="Ej: 999999")
        self.entry_money.grid(row=1, column=1, sticky="w", pady=8, padx=10)

        self.btn_max_money = ctk.CTkButton(
            grid_frame,
            text="💰 Monedas Máximas (999,999)",
            width=200,
            fg_color="#059669",
            hover_color="#047857"
        )
        self.btn_max_money.grid(row=1, column=2, sticky="w", pady=8, padx=10)

        # Nivel del Jugador
        ctk.CTkLabel(grid_frame, text="Nivel del Jugador:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=2, column=0, sticky="w", pady=8, padx=10)
        self.entry_player_level = ctk.CTkEntry(grid_frame, width=220, placeholder_text="Ej: 99")
        self.entry_player_level.grid(row=2, column=1, sticky="w", pady=8, padx=10)

        self.btn_max_level = ctk.CTkButton(
            grid_frame,
            text="⭐ Nivel Máximo (99)",
            width=200,
            fg_color="#7c3aed",
            hover_color="#6d28d9"
        )
        self.btn_max_level.grid(row=2, column=2, sticky="w", pady=8, padx=10)

        # Horas de Juego
        ctk.CTkLabel(grid_frame, text="Tiempo de Juego:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=3, column=0, sticky="w", pady=8, padx=10)
        self.lbl_playtime = ctk.CTkLabel(grid_frame, text="0.0 horas", font=ctk.CTkFont(size=14), text_color="#94a3b8")
        self.lbl_playtime.grid(row=3, column=1, sticky="w", pady=8, padx=10)

        # Separador
        ctk.CTkFrame(self, height=2, fg_color="#334155").pack(fill="x", padx=15, pady=20)

        # Sección 2: Cosméticos
        lbl_cosm = ctk.CTkLabel(
            self,
            text="Cosméticos y Estilo de Personaje",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#f59e0b"
        )
        lbl_cosm.pack(anchor="w", padx=15, pady=(5, 10))

        grid_cosm = ctk.CTkFrame(self, fg_color="transparent")
        grid_cosm.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(grid_cosm, text="Estilo de Ropa:", font=ctk.CTkFont(size=14)).grid(row=0, column=0, sticky="w", pady=6, padx=10)
        self.combo_outfit = ctk.CTkOptionMenu(grid_cosm, values=["Estándar Vestroia", "Campeón Vestroia", "Set Urbano", "Especial Torneo"])
        self.combo_outfit.grid(row=0, column=1, sticky="w", pady=6, padx=10)

        ctk.CTkLabel(grid_cosm, text="Color de Cabello:", font=ctk.CTkFont(size=14)).grid(row=1, column=0, sticky="w", pady=6, padx=10)
        self.combo_hair = ctk.CTkOptionMenu(grid_cosm, values=["Negro", "Castaño", "Rubio", "Rojo Pyrus", "Azul Aquos"])
        self.combo_hair.grid(row=1, column=1, sticky="w", pady=6, padx=10)

        # Botón Aplicar
        self.btn_apply_player = ctk.CTkButton(
            self,
            text="✔️ Aplicar Cambios al Jugador",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=40,
            fg_color="#2563eb",
            hover_color="#1d4ed8"
        )
        self.btn_apply_player.pack(anchor="w", padx=15, pady=20)

    def set_player_info(self, name, money, level, playtime_hours):
        """Actualiza los campos del jugador en la interfaz"""
        self.entry_player_name.delete(0, "end")
        self.entry_player_name.insert(0, str(name))

        self.entry_money.delete(0, "end")
        self.entry_money.insert(0, str(money))

        self.entry_player_level.delete(0, "end")
        self.entry_player_level.insert(0, str(level))

        self.lbl_playtime.configure(text=f"{playtime_hours:.1f} horas jugadas")
