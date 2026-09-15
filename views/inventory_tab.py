import customtkinter as ctk


class InventoryTab(ctk.CTkScrollableFrame):
    """Vista correspondiente a la pestaña de Mochila, Cartas y Cores"""

    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)

        lbl_inv = ctk.CTkLabel(
            self,
            text="Mochila, Cartas de Habilidad y BakuCores",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#f59e0b"
        )
        lbl_inv.pack(anchor="w", padx=15, pady=(15, 10))

        inv_grid = ctk.CTkFrame(self, fg_color="transparent")
        inv_grid.pack(fill="x", padx=15, pady=10)

        # Cartas
        card_box = ctk.CTkFrame(inv_grid, corner_radius=8, fg_color="#1e293b")
        card_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(card_box, text="🃏 Colección de Cartas", font=ctk.CTkFont(size=16, weight="bold"), text_color="#38bdf8").pack(padx=15, pady=(12, 6))
        ctk.CTkLabel(card_box, text="Cartas de Ataque, Defensa y Evolución").pack(padx=15, pady=2)
        self.btn_max_cards = ctk.CTkButton(
            card_box,
            text="🔓 Desbloquear Todas las Cartas",
            fg_color="#059669",
            hover_color="#047857"
        )
        self.btn_max_cards.pack(padx=15, pady=(10, 15))

        # Cores
        core_box = ctk.CTkFrame(inv_grid, corner_radius=8, fg_color="#1e293b")
        core_box.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(core_box, text="💎 Colección BakuCore", font=ctk.CTkFont(size=16, weight="bold"), text_color="#f59e0b").pack(padx=15, pady=(12, 6))
        ctk.CTkLabel(core_box, text="Cores de Oro, Plata, Escudo y Fuego").pack(padx=15, pady=2)
        self.btn_max_cores = ctk.CTkButton(
            core_box,
            text="✨ Máximos BakuCores (x99)",
            fg_color="#7c3aed",
            hover_color="#6d28d9"
        )
        self.btn_max_cores.pack(padx=15, pady=(10, 15))

        # Ítems
        item_box = ctk.CTkFrame(inv_grid, corner_radius=8, fg_color="#1e293b")
        item_box.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(item_box, text="🧪 Objetos y Consumibles", font=ctk.CTkFont(size=16, weight="bold"), text_color="#10b981").pack(padx=15, pady=(12, 6))
        ctk.CTkLabel(item_box, text="Pociones de Energía y Boosts").pack(padx=15, pady=2)
        self.btn_max_items = ctk.CTkButton(
            item_box,
            text="🎒 Maximizar Objetos (x999)",
            fg_color="#2563eb",
            hover_color="#1d4ed8"
        )
        self.btn_max_items.pack(padx=15, pady=(10, 15))
