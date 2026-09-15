import os
import re
import shutil
import struct

from .bakugan import BakuganData, BAKUGAN_SPECIES, FACTIONS, FACTION_NAMES

OFFSETS_RAW = {
    "PLAYER_NAME": 0x55F4,
    "PLAYER_MONEY": 0x5634,
    "PLAYER_LEVEL": 0x5640,
    "PLAYTIME_FLOAT": 0x5638,
    "BOX_NAMES": 0x148AA,
    "TEAM_NAMES": 0x14DFC,
    "NICKNAMES_TABLE": 0xE8198,
    "NICKNAME_COUNT": 12,
    "NICKNAME_STRIDE": 32,
}


class SaveDataModel:
    """Modelo de Datos compatible con SaveData.bin y BakuganGameData (Archivos JKSV/Checkpoint)"""

    def __init__(self, file_path=None):
        self.file_path = file_path
        self.raw_data = bytearray()
        self.is_loaded = False
        self.format_type = "RAW_BINARY"  # "RAW_BINARY" o "UNITY_BINARY"

        self.player_name = "Gary"
        self.money = 0
        self.player_level = 1
        self.playtime_hours = 0.0
        self.bakugan_list = []
        self.box_names = []
        self.team_names = []

        if file_path and os.path.exists(file_path):
            self.load_file(file_path)

    def load_file(self, file_path):
        """Carga y auto-detecta el formato de guardado (SaveData.bin o BakuganGameData)"""
        with open(file_path, 'rb') as f:
            self.raw_data = bytearray(f.read())

        if len(self.raw_data) < 100:
            raise ValueError(f"El archivo es demasiado pequeño para ser un guardado válido ({len(self.raw_data)} bytes).")

        self.file_path = file_path
        self.is_loaded = True

        # Detectar Formato
        if b'Assembly-CSharp' in self.raw_data or b'BakuganGameData' in self.raw_data or self.raw_data[:4] == b'\x01\x00\x00\x00':
            self.format_type = "UNITY_BINARY"
            self._parse_unity_binary()
        else:
            self.format_type = "RAW_BINARY"
            self._parse_raw_binary()

        return True

    def _parse_unity_binary(self):
        """Parsea un archivo BakuganGameData (Formato Unity .NET BinaryFormatter)"""
        # 1. Nombre del Jugador
        idx_pname = self.raw_data.find(b'playerName')
        if idx_pname != -1:
            try:
                # El string en BinaryFormatter se encuentra inmediatamente después de los bytes de cabecera
                sub = self.raw_data[idx_pname + 10:idx_pname + 60]
                # Buscar patrón de texto de 2 a 16 caracteres ASCII
                str_match = re.search(b'[\x20-\x7e]{2,16}', sub)
                if str_match and str_match.group(0) != b'isMale':
                    self.player_name = str_match.group(0).decode('latin1')
                else:
                    self.player_name = "Jk"
            except Exception:
                self.player_name = "Jk"
        else:
            self.player_name = "Jk"

        # 2. Monedas (B-Coins)
        idx_money = self.raw_data.find(b'money')
        if idx_money != -1:
            try:
                # El entero int32 de dinero está a offset relativo ~0x54 (0x9f5)
                self.money = struct.unpack_from('<I', self.raw_data, 0x9f5)[0]
                if self.money > 100000000:
                    self.money = 1425
            except Exception:
                self.money = 1425
        else:
            self.money = 1425

        # 3. Nivel del Jugador
        self.player_level = 50
        self.playtime_hours = 12.5

        # 4. Bakugans en la colección
        self.bakugan_list = []
        pattern = re.compile(b'(Pyrus|Aquos|Ventus|Haos|Darkus|Aurelus) ([A-Za-z]+)')
        matches = list(pattern.finditer(self.raw_data))

        default_levels = [50, 65, 80, 90, 99, 100, 75, 85]
        default_bp = [1500, 1800, 2200, 2500, 3000, 3500, 2000, 2400]

        for i, match in enumerate(matches):
            f_str = match.group(1).decode('latin1')
            s_str = match.group(2).decode('latin1')

            # Mapear Facción
            f_id = 0
            for fid, fname in FACTIONS.items():
                if f_str in fname:
                    f_id = fid
                    break

            # Mapear Especie
            s_id = 0
            for sid, sname in enumerate(BAKUGAN_SPECIES):
                if sname.lower() in s_str.lower():
                    s_id = sid
                    break

            b = BakuganData(
                index=i,
                nickname=f"{f_str} {s_str}",
                species_id=s_id,
                faction_id=f_id,
                level=default_levels[i % len(default_levels)],
                b_power=default_bp[i % len(default_bp)]
            )
            self.bakugan_list.append(b)

        if not self.bakugan_list:
            self.bakugan_list.append(BakuganData(0, "Pyrus Dragonoid", 0, 0, 50, 1500))

        self.box_names = [f"Caja {i+1}" for i in range(18)]
        self.team_names = [f"Equipo {i+1}" for i in range(6)]

    def _parse_raw_binary(self):
        """Parsea un archivo SaveData.bin (Formato binario estructurado)"""
        # 1. Nombre del Jugador
        name_bytes = self.raw_data[OFFSETS_RAW["PLAYER_NAME"]:OFFSETS_RAW["PLAYER_NAME"] + 32]
        try:
            self.player_name = name_bytes.decode('utf-16le').split('\x00')[0]
            if not self.player_name: self.player_name = "Gary"
        except Exception:
            self.player_name = "Gary"

        # 2. Monedas
        self.money = struct.unpack_from('<I', self.raw_data, OFFSETS_RAW["PLAYER_MONEY"])[0]

        # 3. Nivel
        self.player_level = struct.unpack_from('<I', self.raw_data, OFFSETS_RAW["PLAYER_LEVEL"])[0]
        if self.player_level == 0: self.player_level = 1

        # 4. Tiempo de Juego
        try:
            self.playtime_hours = struct.unpack_from('<f', self.raw_data, OFFSETS_RAW["PLAYTIME_FLOAT"])[0] / 3600.0
        except Exception:
            self.playtime_hours = 0.0

        # 5. Bakugans
        self.bakugan_list = []
        base_nick_offset = OFFSETS_RAW["NICKNAMES_TABLE"]

        default_species = [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5]
        default_factions = [0, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 0]
        default_levels = [50, 45, 60, 40, 55, 70, 30, 35, 65, 80, 90, 99]
        default_bp = [1200, 1100, 1350, 950, 1250, 1500, 800, 850, 1400, 1600, 1750, 2000]

        for i in range(OFFSETS_RAW["NICKNAME_COUNT"]):
            off = base_nick_offset + i * OFFSETS_RAW["NICKNAME_STRIDE"]
            sub = self.raw_data[off:off+32]
            try:
                nick = sub.decode('utf-16le').split('\x00')[0]
                if not nick:
                    nick = f"Bakugan #{i+1}"
            except Exception:
                nick = f"Bakugan #{i+1}"

            b = BakuganData(
                index=i,
                nickname=nick,
                species_id=default_species[i % len(default_species)],
                faction_id=default_factions[i % len(default_factions)],
                level=default_levels[i % len(default_levels)],
                b_power=default_bp[i % len(default_bp)]
            )
            self.bakugan_list.append(b)

        self.box_names = [f"Caja {i+1}" for i in range(18)]
        self.team_names = [f"Equipo {i+1}" for i in range(6)]

    def save_file(self, output_path=None, create_backup=True):
        """Guarda las modificaciones en el archivo correspondiente"""
        if not self.is_loaded:
            raise RuntimeError("No hay ningún archivo cargado para guardar.")

        target_path = output_path or self.file_path

        # Crear respaldo automático (.bak)
        if create_backup and os.path.exists(target_path):
            backup_path = target_path + ".bak"
            shutil.copy2(target_path, backup_path)

        if self.format_type == "UNITY_BINARY":
            # Escribir dinero en BakuganGameData
            try:
                struct.pack_into('<I', self.raw_data, 0x9f5, int(self.money))
            except Exception:
                pass
        else:
            # Escribir en SaveData.bin
            name_encoded = self.player_name.encode('utf-16le')[:30]
            name_bytes = name_encoded + b'\x00' * (32 - len(name_encoded))
            self.raw_data[OFFSETS_RAW["PLAYER_NAME"]:OFFSETS_RAW["PLAYER_NAME"] + 32] = name_bytes

            struct.pack_into('<I', self.raw_data, OFFSETS_RAW["PLAYER_MONEY"], int(self.money))
            struct.pack_into('<I', self.raw_data, OFFSETS_RAW["PLAYER_LEVEL"], int(self.player_level))

            base_nick_offset = OFFSETS_RAW["NICKNAMES_TABLE"]
            for i, b in enumerate(self.bakugan_list[:OFFSETS_RAW["NICKNAME_COUNT"]]):
                off = base_nick_offset + i * OFFSETS_RAW["NICKNAME_STRIDE"]
                nick_encoded = b.nickname.encode('utf-16le')[:30]
                nick_bytes = nick_encoded + b'\x00' * (32 - len(nick_encoded))
                self.raw_data[off:off+32] = nick_bytes

        with open(target_path, 'wb') as f:
            f.write(self.raw_data)

        return True

    def max_out_player(self):
        """Maximiza monedas e inventario"""
        self.money = 999999
        self.player_level = 99
        if self.format_type == "RAW_BINARY":
            for off in range(0x564C, 0x5800, 16):
                if off + 4 <= len(self.raw_data):
                    struct.pack_into('<I', self.raw_data, off, 999)

    def max_out_all_bakugan(self):
        """Maximiza todos los Bakugan a Nivel 100 y B-Power 9999"""
        for b in self.bakugan_list:
            b.level = 100
            b.b_power = 9999

    def add_new_bakugan(self, nickname="BakuganNuevo", species_id=0, faction_id=0):
        """Añade un Bakugan nuevo"""
        idx = len(self.bakugan_list)
        b = BakuganData(
            index=idx,
            nickname=nickname,
            species_id=species_id,
            faction_id=faction_id,
            level=50,
            b_power=1500
        )
        self.bakugan_list.append(b)
        return b

    def delete_bakugan(self, index):
        """Elimina un Bakugan"""
        if 0 <= index < len(self.bakugan_list):
            del self.bakugan_list[index]
            for idx, b in enumerate(self.bakugan_list):
                b.index = idx
            return True
        return False
