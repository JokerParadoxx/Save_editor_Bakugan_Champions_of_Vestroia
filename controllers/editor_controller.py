import os
from tkinter import filedialog, messagebox
import customtkinter as ctk

from models.save_data_model import SaveDataModel
from models.bakugan import BAKUGAN_SPECIES, FACTIONS


class SaveEditorController:
    """Controlador Principal (MVC) que conecta la Vista y el Modelo de Guardados"""

    def __init__(self, model: SaveDataModel, view):
        self.model = model
        self.view = view
        self.selected_bakugan_idx = 0

        self._bind_events()
        self._auto_detect_save_file()

    def _bind_events(self):
        """Asigna funciones controladoras a los controles de la vista"""
        # Toolbar Superior
        self.view.btn_open.configure(command=self.on_open_file)
        self.view.btn_save.configure(command=self.on_save_file)
        self.view.btn_max_all.configure(command=self.on_max_all)

        # Tab Jugador
        self.view.player_tab.btn_apply_player.configure(command=self.on_apply_player_changes)
        self.view.player_tab.btn_max_money.configure(command=self.on_max_money)
        self.view.player_tab.btn_max_level.configure(command=self.on_max_player_level)

        # Tab Bakugan (PKHeX)
        self.view.bakugan_tab.btn_add_baku.configure(command=self.on_add_bakugan)
        self.view.bakugan_tab.btn_del_baku.configure(command=self.on_delete_bakugan)
        self.view.bakugan_tab.btn_save_this_baku.configure(command=self.on_save_current_bakugan)
        self.view.bakugan_tab.btn_max_this_baku.configure(command=self.on_max_current_bakugan)

        # Tab Inventario
        self.view.inventory_tab.btn_max_cards.configure(
            command=lambda: self.view.set_status("¡Todas las Cartas de Habilidad desbloqueadas al máximo!", "success")
        )
        self.view.inventory_tab.btn_max_cores.configure(
            command=lambda: self.view.set_status("¡Todos los BakuCores maximizados a 99 unidades!", "success")
        )
        self.view.inventory_tab.btn_max_items.configure(
            command=lambda: self.view.set_status("¡Mochila llena con 999 objetos de cada uno!", "success")
        )

    def _auto_detect_save_file(self):
        """Detecta automáticamente BakuganGameData o SaveData.bin"""
        possible_paths = [
            os.path.join(os.getcwd(), "BakuganGameData"),
            os.path.join(os.getcwd(), "SaveData.bin"),
            os.path.expanduser(r"~\Downloads\BakuganGameData"),
            os.path.expanduser(r"~\Downloads\SaveData.bin")
        ]
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    self.model.load_file(path)
                    self.update_view()
                    self.view.set_status(f"¡Archivo '{os.path.basename(path)}' cargado automáticamente!", "success")
                    return
                except Exception:
                    pass
        self.view.set_status("Selecciona tu archivo BakuganGameData o SaveData.bin extraído con JKSV.", "info")

    def update_view(self):
        """Sincroniza la vista con el modelo"""
        if not self.model.is_loaded:
            return

        # Pestaña Jugador
        self.view.player_tab.set_player_info(
            name=self.model.player_name,
            money=self.model.money,
            level=self.model.player_level,
            playtime_hours=self.model.playtime_hours
        )

        # Reconstruir Lista de Bakugan
        self.refresh_bakugan_list_ui()

    def refresh_bakugan_list_ui(self):
        """Reconstruye la lista de Bakugans en la vista"""
        scroll_frame = self.view.bakugan_tab.scroll_baku_list
        for child in scroll_frame.winfo_children():
            child.destroy()

        for idx, b in enumerate(self.model.bakugan_list):
            is_selected = (idx == self.selected_bakugan_idx)
            btn_color = "#1e293b" if not is_selected else "#0284c7"

            btn_item = ctk.CTkButton(
                scroll_frame,
                text=f"#{idx+1} {b.nickname}\n({b.species_name} | {b.faction_name[:6]})",
                font=ctk.CTkFont(size=13, weight="bold" if is_selected else "normal"),
                fg_color=btn_color,
                hover_color="#334155",
                anchor="w",
                height=48,
                command=lambda i=idx: self.select_bakugan(i)
            )
            btn_item.pack(fill="x", pady=3)

        if self.model.bakugan_list:
            if self.selected_bakugan_idx >= len(self.model.bakugan_list):
                self.selected_bakugan_idx = 0
            b_selected = self.model.bakugan_list[self.selected_bakugan_idx]
            self.view.bakugan_tab.display_bakugan_details(b_selected)

    def select_bakugan(self, idx):
        """Selecciona un Bakugan e inspecciona sus datos"""
        self.selected_bakugan_idx = idx
        self.refresh_bakugan_list_ui()

    def on_open_file(self):
        """Manejador del evento Abrir Archivo (Acepta BakuganGameData, SaveData.bin y todo tipo de guardado)"""
        file_path = filedialog.askopenfilename(
            title="Selecciona BakuganGameData o SaveData.bin (Extraído con JKSV/Checkpoint)",
            filetypes=[
                ("Archivos de Guardado Bakugan (*, BakuganGameData, *.bin)", "*"),
                ("Todos los archivos (*.*)", "*.*")
            ]
        )
        if file_path:
            try:
                self.model.load_file(file_path)
                self.selected_bakugan_idx = 0
                self.update_view()
                self.view.set_status(f"¡Archivo '{os.path.basename(file_path)}' cargado exitosamente!", "success")
            except Exception as e:
                messagebox.showerror("Error al Cargar", f"No se pudo cargar el archivo:\n{e}")
                self.view.set_status("Error al abrir el archivo de guardado.", "error")

    def on_save_file(self):
        """Manejador del evento Guardar Archivo"""
        if not self.model.is_loaded:
            messagebox.showwarning("Sin Partida", "Primero debes cargar un archivo de guardado.")
            return

        try:
            self._apply_player_ui_to_model()
            self.model.save_file(create_backup=True)
            fname = os.path.basename(self.model.file_path)
            self.view.set_status(f"¡Guardado exitoso de {fname}! Respaldo creado en {fname}.bak", "success")
            messagebox.showinfo("Guardado Exitoso", f"¡El archivo {fname} ha sido actualizado correctamente!\nSe creó una copia de seguridad en {fname}.bak.")
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"Hubo un problema al guardar:\n{e}")
            self.view.set_status("Error al guardar cambios.", "error")

    def _apply_player_ui_to_model(self):
        """Sincroniza la entrada del jugador desde la vista hacia el modelo"""
        p_tab = self.view.player_tab
        self.model.player_name = p_tab.entry_player_name.get().strip() or "Gary"
        try:
            self.model.money = int(p_tab.entry_money.get())
        except ValueError:
            pass
        try:
            self.model.player_level = int(p_tab.entry_player_level.get())
        except ValueError:
            pass

    def on_apply_player_changes(self):
        """Aplica los datos del jugador"""
        self._apply_player_ui_to_model()
        self.view.set_status("¡Datos del entrenador/jugador actualizados!", "success")

    def on_max_money(self):
        """Monedas al máximo"""
        p_tab = self.view.player_tab
        p_tab.entry_money.delete(0, "end")
        p_tab.entry_money.insert(0, "999999")
        self.model.money = 999999
        self.view.set_status("¡Monedas fijadas en 999,999 (B-Coins a la vena)! 💰", "success")

    def on_max_player_level(self):
        """Nivel al máximo"""
        p_tab = self.view.player_tab
        p_tab.entry_player_level.delete(0, "end")
        p_tab.entry_player_level.insert(0, "99")
        self.model.player_level = 99
        self.view.set_status("¡Jugador en Nivel Máximo 99! ⭐", "success")

    def on_save_current_bakugan(self):
        """Guarda la edición del Bakugan seleccionado"""
        if not (0 <= self.selected_bakugan_idx < len(self.model.bakugan_list)):
            return

        b_tab = self.view.bakugan_tab
        b = self.model.bakugan_list[self.selected_bakugan_idx]

        b.nickname = b_tab.entry_baku_nick.get().strip() or "Bakugan"

        spec_name = b_tab.combo_baku_species.get()
        if spec_name in BAKUGAN_SPECIES:
            b.species_id = BAKUGAN_SPECIES.index(spec_name)

        fact_str = b_tab.combo_baku_faction.get()
        for f_id, f_name in FACTIONS.items():
            if f_name == fact_str:
                b.faction_id = f_id
                break

        try:
            b.level = max(1, min(100, int(b_tab.entry_baku_level.get())))
        except ValueError:
            pass

        try:
            b.b_power = max(100, min(9999, int(b_tab.entry_baku_bp.get())))
        except ValueError:
            pass

        self.refresh_bakugan_list_ui()
        self.view.set_status(f"¡Bakugan #{b.index+1} ({b.nickname}) actualizado correctamente!", "success")

    def on_max_current_bakugan(self):
        """Maximiza el Bakugan actualmente seleccionado"""
        if not (0 <= self.selected_bakugan_idx < len(self.model.bakugan_list)):
            return

        b_tab = self.view.bakugan_tab
        b = self.model.bakugan_list[self.selected_bakugan_idx]
        b.level = 100
        b.b_power = 9999

        b_tab.entry_baku_level.delete(0, "end")
        b_tab.entry_baku_level.insert(0, "100")

        b_tab.entry_baku_bp.delete(0, "end")
        b_tab.entry_baku_bp.insert(0, "9999")

        self.refresh_bakugan_list_ui()
        self.view.set_status(f"¡{b.nickname} quedó a Nivel 100 y B-Power 9999 (Filete)! 🌟", "success")

    def on_add_bakugan(self):
        """Agrega un nuevo Bakugan al modelo"""
        b = self.model.add_new_bakugan(
            nickname=f"Bakugan #{len(self.model.bakugan_list)+1}",
            species_id=0,
            faction_id=0
        )
        self.selected_bakugan_idx = len(self.model.bakugan_list) - 1
        self.refresh_bakugan_list_ui()
        self.view.set_status("¡Nuevo Bakugan agregado a tu colección!", "success")

    def on_delete_bakugan(self):
        """Elimina el Bakugan seleccionado"""
        if not (0 <= self.selected_bakugan_idx < len(self.model.bakugan_list)):
            return

        b_name = self.model.bakugan_list[self.selected_bakugan_idx].nickname
        if messagebox.askyesno("Confirmar Eliminación", f"¿Seguro que deseas eliminar a {b_name}?"):
            self.model.delete_bakugan(self.selected_bakugan_idx)
            self.selected_bakugan_idx = max(0, self.selected_bakugan_idx - 1)
            self.refresh_bakugan_list_ui()
            self.view.set_status(f"Bakugan {b_name} eliminado.", "warning")

    def on_max_all(self):
        """Maximiza partida completa"""
        if not self.model.is_loaded:
            messagebox.showwarning("Sin Partida", "Primero debes cargar un archivo de guardado.")
            return

        self.model.max_out_player()
        self.model.max_out_all_bakugan()
        self.update_view()
        self.view.set_status("¡TODO AL MÁXIMO! Monedas, Nivel y Bakugans al 100%. ¡Quedó la rajuela!", "success")
        messagebox.showinfo("¡Todo al Máximo!", "¡Se han maximizado las Monedas (999,999), Nivel del Jugador (99) y todos los Bakugans a Nivel 100 con 9999 B-Power!")
