# Bakugan: Champions of Vestroia - Save Editor (Arquitectura MVC 🇨🇱)

Editor gráfico de partidas guardadas (`BakuganGameData` / `SaveData.bin`) para **Bakugan Champions of Vestroia** en **Nintendo Switch** (extraídas con JKSV, Checkpoint, EdiZon o similares).

Desarrollado en **Python 3** usando **CustomTkinter** con arquitectura **MVC (Modelo - Vista - Controlador)** y localizado completamente en **Español Chileno**.

---

## 🌟 Características Principales

1. **🎮 Datos del Entrenador / Jugador**:
   - Nombre del Jugador (Editable).
   - Monedas **B-Coins** (Botón para fijar 999,999 B-Coins de inmediato).
   - **Nivel del Jugador** (Nivel 1 a 99).
   - Tiempo de juego registrado.
   - Apariencia y cosméticos.

2. **🐲 Editor de Bakugan (Estilo PKHeX)**:
   - Visualizador e inspector lateral de Bakugans de tu colección.
   - Navegación entre **Cajas (Caja 1 a 18)** y **Equipos (Equipo 1 a 6)**.
   - Modificación de **Mote / Nickname**.
   - Cambio de **Especie** (*Dragonoid, Nillious, Hydorous, Trox, Pegatrix, Howlkor, Cyndeous, Pharol, Gillator, etc.*).
   - Cambio de **Facción / Atributo** (*Pyrus 🔥, Aquos 💧, Ventus 🍃, Haos ⚡, Darkus 🌑, Aurelus ✨*).
   - Modificación de **Nivel (1-100)** y **Poder B-Power (100-9999)**.
   - Equipamiento de **BakuGear** (Ultima Pyrus, Wings Alpha, Shield Delta, Void Claws, Armor Gold).
   - Botón **"¡Dejar este Bakugan Filete (Lvl 100 / BP 9999)!"**.
   - Funcionalidad para **Agregar** y **Eliminar** Bakugans.

3. **🎒 Mochila, Cartas & BakuCores**:
   - Desbloqueador de todas las **Cartas de Habilidad** (Ataque, Defensa, Evolución).
   - Maximizador de **BakuCores** (x99).
   - Maximizador de **Ítems y Consumibles** (x999).

4. **⚡ Botón "¡Dejar Todo Filete!"**:
   - Maximiza en un solo clic las Monedas (999,999), Nivel del Jugador (99) y todos los Bakugans a Nivel 100 con B-Power 9999.

5. **🛡️ Respaldo Automático de Seguridad**:
   - Cada vez que guardas cambios, la aplicación crea automáticamente una copia de seguridad (`.bak`).

---

## 🚀 Cómo Ejecutar la Aplicación

Para iniciar la aplicación ejecuta únicamente **`main.py`**:

```powershell
python main.py
```

O especificando el ejecutable de Python en PowerShell:

```powershell
& "C:\Users\hehum\AppData\Local\Python\bin\python.exe" main.py
```

---

## 📂 Guía de Uso con JKSV (Nintendo Switch)

1. En tu consola **Nintendo Switch** con CFW (Atmosphère), abre **JKSV**.
2. Selecciona **Bakugan: Champions of Vestroia** y elige **New Backup** (por ejemplo: `Save_Backup_01`).
3. Copia la carpeta del respaldo desde tu tarjeta SD (`/JKSV/Bakugan Champions of Vestroia/...`) a tu PC.
4. Abre esta aplicación ejecutando `python main.py` y haz clic en **"📂 Cargar SaveData.bin"** (o selecciona `BakuganGameData`).
5. Realiza todas las modificaciones que quieras a tu jugador y tus Bakugans.
6. Haz clic en **"💾 Guardar Cambios"**.
7. Copia el archivo modificado de vuelta a tu tarjeta SD en la carpeta de JKSV.
8. En tu Nintendo Switch, abre **JKSV** y selecciona **Restore**.
9. ¡Inicia el juego y a disfrutar con todo al máximo! 🎮🔥
