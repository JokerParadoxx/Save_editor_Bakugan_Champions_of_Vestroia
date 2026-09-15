import customtkinter as ctk
from .player_tab import PlayerTab
from .bakugan_tab import BakuganTab
from .inventory_tab import InventoryTab

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MainView(ctk.CTk):
    """Vista Principal de la Aplicación en Arquitectura MVC"""

    def __init__(self):
        super().__init__()

        self.title("Bakugan: Champions of Vestroia - Save Editor v1.0 by JokerParadox 🇨🇱")
        self.geometry("1100x720")
        self.minsize(980, 650)

        # 1. Barra de Herramientas Superior
        self._build_toolbar()

        # 2. Tabview Contenedor
        self.tabview = ctk.CTkTabview(self, corner_radius=12)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=5)

        self.tab_player_frame = self.tabview.add("🎮 Datos del Jugador")
        self.tab_bakugan_frame = self.tabview.add("🐲 Editor Bakugan (PKHeX)")
        self.tab_inventory_frame = self.tabview.add("🎒 Mochila, Cartas & Cores")

        # Subvistas
        self.player_tab = PlayerTab(self.tab_player_frame)
        self.player_tab.pack(fill="both", expand=True, padx=5, pady=5)

        self.bakugan_tab = BakuganTab(self.tab_bakugan_frame)
        self.bakugan_tab.pack(fill="both", expand=True, padx=5, pady=5)

        self.inventory_tab = InventoryTab(self.tab_inventory_frame)
        self.inventory_tab.pack(fill="both", expand=True, padx=5, pady=5)

        # 3. Barra de Estado Inferior
        self._build_statusbar()

    def _build_toolbar(self):
        """Barra de herramientas superior con botones principales"""
        self.toolbar_frame = ctk.CTkFrame(self, corner_radius=10)
        self.toolbar_frame.pack(fill="x", padx=15, pady=(15, 10))

        self.title_label = ctk.CTkLabel(
            self.toolbar_frame,
            text="🔥 BAKUGAN VESTROIA SAVE EDITOR",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(side="left", padx=15, pady=12)

        self.subtitle_label = ctk.CTkLabel(
            self.toolbar_frame,
            text="v1.0 by JokerParadox 🇨🇱",
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color="#38bdf8"
        )
        self.subtitle_label.pack(side="left", padx=5, pady=12)

        self.btn_max_all = ctk.CTkButton(
            self.toolbar_frame,
            text="⚡ ¡Dejar Todo Filete! (Max All)",
            fg_color="#8b5cf6",
            hover_color="#7c3aed",
            font=ctk.CTkFont(weight="bold")
        )
        self.btn_max_all.pack(side="right", padx=10, pady=10)

        self.btn_save = ctk.CTkButton(
            self.toolbar_frame,
            text="💾 Guardar Cambios",
            fg_color="#10b981",
            hover_color="#059669",
            font=ctk.CTkFont(weight="bold")
        )
        self.btn_save.pack(side="right", padx=5, pady=10)

        self.btn_open = ctk.CTkButton(
            self.toolbar_frame,
            text="📂 Cargar SaveData.bin",
            fg_color="#0284c7",
            hover_color="#0369a1",
            font=ctk.CTkFont(weight="bold")
        )
        self.btn_open.pack(side="right", padx=5, pady=10)

    def _build_statusbar(self):
        """Barra de estado inferior para notificaciones"""
        self.statusbar_frame = ctk.CTkFrame(self, height=36, corner_radius=0, fg_color="#0f172a")
        self.statusbar_frame.pack(fill="x", side="bottom")

        self.lbl_status = ctk.CTkLabel(
            self.statusbar_frame,
            text="Listo.",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        )
        self.lbl_status.pack(side="left", padx=15, pady=5)

    def set_status(self, text, message_type="info"):
        """Actualiza el texto y color de la barra de estado"""
        colors = {
            "info": "#94a3b8",
            "success": "#34d399",
            "warning": "#fbbf24",
            "error": "#f87171"
        }
        color = colors.get(message_type, "#94a3b8")
        self.lbl_status.configure(text=f"🇨🇱 {text}", text_color=color)
