import customtkinter as ctk
from models.bakugan import BAKUGAN_SPECIES, FACTIONS


class BakuganTab(ctk.CTkFrame):
    """Vista de la pestaña Bakugan estilo PKHeX (Lista/Cajas e Inspector de Stats)"""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        # Layout Principal
        main_layout = ctk.CTkFrame(self, fg_color="transparent")
        main_layout.pack(fill="both", expand=True, padx=5, pady=5)

        # Columna Izquierda: Cajas y Lista
        col_left = ctk.CTkFrame(main_layout, width=320, corner_radius=10)
        col_left.pack(side="left", fill="both", padx=(5, 10), pady=5)

        ctk.CTkLabel(
            col_left,
            text="📦 Almacenamiento & Cajas",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#38bdf8"
        ).pack(padx=10, pady=(12, 6))

        self.combo_boxes = ctk.CTkOptionMenu(
            col_left,
            values=[f"Caja {i+1}" for i in range(18)]
        )
        self.combo_boxes.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(col_left, text="Bakugans Registrados:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=12, pady=(10, 4))

        self.scroll_baku_list = ctk.CTkScrollableFrame(col_left, corner_radius=8)
        self.scroll_baku_list.pack(fill="both", expand=True, padx=10, pady=5)

        btn_box_actions = ctk.CTkFrame(col_left, fg_color="transparent")
        btn_box_actions.pack(fill="x", padx=10, pady=10)

        self.btn_add_baku = ctk.CTkButton(
            btn_box_actions,
            text="➕ Agregar",
            width=135,
            fg_color="#059669",
            hover_color="#047857"
        )
        self.btn_add_baku.pack(side="left", padx=2)

        self.btn_del_baku = ctk.CTkButton(
            btn_box_actions,
            text="❌ Eliminar",
            width=135,
            fg_color="#dc2626",
            hover_color="#b91c1c"
        )
        self.btn_del_baku.pack(side="right", padx=2)

        # Columna Derecha: Inspector estilo PKHeX
        col_right = ctk.CTkScrollableFrame(main_layout, corner_radius=10)
        col_right.pack(side="right", fill="both", expand=True, padx=(0, 5), pady=5)

        ctk.CTkLabel(
            col_right,
            text="🔍 Inspector de Stats Bakugan (Estilo PKHeX)",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#f59e0b"
        ).pack(anchor="w", padx=15, pady=(12, 10))

        inspector_grid = ctk.CTkFrame(col_right, fg_color="transparent")
        inspector_grid.pack(fill="x", padx=15, pady=5)

        # Mote / Nickname
        ctk.CTkLabel(inspector_grid, text="Mote / Nickname:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky="w", pady=8, padx=5)
        self.entry_baku_nick = ctk.CTkEntry(inspector_grid, width=240, placeholder_text="Mote del Bakugan")
        self.entry_baku_nick.grid(row=0, column=1, sticky="w", pady=8, padx=5)

        # Especie
        ctk.CTkLabel(inspector_grid, text="Especie Bakugan:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=1, column=0, sticky="w", pady=8, padx=5)
        self.combo_baku_species = ctk.CTkOptionMenu(inspector_grid, width=240, values=BAKUGAN_SPECIES)
        self.combo_baku_species.grid(row=1, column=1, sticky="w", pady=8, padx=5)

        # Facción / Atributo
        ctk.CTkLabel(inspector_grid, text="Facción / Atributo:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=2, column=0, sticky="w", pady=8, padx=5)
        self.combo_baku_faction = ctk.CTkOptionMenu(inspector_grid, width=240, values=list(FACTIONS.values()))
        self.combo_baku_faction.grid(row=2, column=1, sticky="w", pady=8, padx=5)

        # Nivel
        ctk.CTkLabel(inspector_grid, text="Nivel (1 - 100):", font=ctk.CTkFont(size=14, weight="bold")).grid(row=3, column=0, sticky="w", pady=8, padx=5)
        self.entry_baku_level = ctk.CTkEntry(inspector_grid, width=240, placeholder_text="Ej: 100")
        self.entry_baku_level.grid(row=3, column=1, sticky="w", pady=8, padx=5)

        # B-Power
        ctk.CTkLabel(inspector_grid, text="Poder B-Power:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=4, column=0, sticky="w", pady=8, padx=5)
        self.entry_baku_bp = ctk.CTkEntry(inspector_grid, width=240, placeholder_text="Ej: 9999")
        self.entry_baku_bp.grid(row=4, column=1, sticky="w", pady=8, padx=5)

        # BakuGear Equipado
        ctk.CTkLabel(inspector_grid, text="BakuGear Equipado:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=5, column=0, sticky="w", pady=8, padx=5)
        self.combo_bakugear = ctk.CTkOptionMenu(
            inspector_grid,
            width=240,
            values=["Ninguno", "Cañones Ultima Pyrus", "Alas Ventus Alpha", "Escudo Aquos Delta", "Lanza Haos Sun", "Garras Darkus Void", "Armadura Aurelus Gold"]
        )
        self.combo_bakugear.grid(row=5, column=1, sticky="w", pady=8, padx=5)

        # Separador
        ctk.CTkFrame(col_right, height=2, fg_color="#334155").pack(fill="x", padx=15, pady=15)

        baku_btns = ctk.CTkFrame(col_right, fg_color="transparent")
        baku_btns.pack(fill="x", padx=15, pady=10)

        self.btn_save_this_baku = ctk.CTkButton(
            baku_btns,
            text="✏️ Modificar este Bakugan",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#0284c7",
            hover_color="#0369a1",
            height=38
        )
        self.btn_save_this_baku.pack(side="left", padx=5)

        self.btn_max_this_baku = ctk.CTkButton(
            baku_btns,
            text="🌟 ¡Dejar este Bakugan Filete (Lvl 100 / BP 9999)!",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#8b5cf6",
            hover_color="#7c3aed",
            height=38
        )
        self.btn_max_this_baku.pack(side="left", padx=5)

    def display_bakugan_details(self, bakugan):
        """Muestra los detalles de un objeto Bakugan en los controles"""
        if not bakugan:
            return

        self.entry_baku_nick.delete(0, "end")
        self.entry_baku_nick.insert(0, bakugan.nickname)

        self.combo_baku_species.set(bakugan.species_name)
        self.combo_baku_faction.set(bakugan.faction_name)

        self.entry_baku_level.delete(0, "end")
        self.entry_baku_level.insert(0, str(bakugan.level))

        self.entry_baku_bp.delete(0, "end")
        self.entry_baku_bp.insert(0, str(bakugan.b_power))
