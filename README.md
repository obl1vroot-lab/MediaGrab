# ⬇️ MediaGrab

> Tired of sketchy online downloaders full of ads? MediaGrab lädt dir YouTube & TikTok Videos direkt auf deinen PC – als MP4 oder MP3, in der Qualität die du willst. Keine Werbung, kein Browser, kein Bullshit.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📋 Voraussetzungen

- **Python 3.8+** → [python.org/downloads](https://www.python.org/downloads/)  
  ⚠️ Bei der Installation unbedingt **„Add Python to PATH"** anhaken!
- **ffmpeg** (nur für MP3-Downloads) → Anleitung weiter unten

---

## 🚀 Installation & Start – Schritt für Schritt

### Schritt 1 – CMD öffnen

Drücke `Windows-Taste`, tippe `cmd` und drücke **Enter**.

Ein schwarzes Fenster öffnet sich – das ist die Eingabeaufforderung.

---

### Schritt 2 – In den richtigen Ordner navigieren

Navigiere mit `cd` zu dem Ordner, in dem du `Mediagrab.py` gespeichert hast.

**Beispiel:** Du hast die Datei in `C:\Users\DeinName\Downloads` gespeichert:
```
cd C:\Users\DeinName\Downloads
```

> 💡 **Tipp:** Im Explorer den Ordner öffnen, oben in die Adressleiste klicken, `cmd` eintippen und Enter drücken – CMD öffnet sich direkt im richtigen Ordner.

---

### Schritt 3 – Abhängigkeiten installieren

Tippe folgenden Befehl und drücke **Enter**:
```
pip install customtkinter yt-dlp
```

Falls das nicht funktioniert, probiere der Reihe nach diese Alternativen:
```
pip3 install customtkinter yt-dlp
```
```
python -m pip install customtkinter yt-dlp
```
```
py -m pip install customtkinter yt-dlp
```

Warte bis alles durchgelaufen ist. Du siehst am Ende `Successfully installed ...`.

---

### Schritt 4 – ffmpeg installieren (für MP3)

Nur nötig wenn du Audio herunterladen willst. Tippe in CMD:
```
winget install ffmpeg
```

Danach CMD **neu starten**.

---

### Schritt 5 – MediaGrab starten

```
python Mediagrab.py
```

Das Fenster öffnet sich und du kannst loslegen. 🎉

---

## 🎮 Benutzung

**1. URL kopieren**  
Geh auf YouTube oder TikTok, such dir ein Video raus und kopiere die URL aus der Adressleiste.

**2. URL einfügen**  
Füge die URL in das Textfeld oben in MediaGrab ein.

**3. Format wählen**  
- 🎬 **Video (MP4)** – komplettes Video  
- 🎵 **Nur Audio (MP3)** – nur der Ton, z.B. für Musik oder Podcasts

**4. Qualität einstellen**  
Wähle zwischen `best`, `1080p`, `720p`, `480p` und `360p`.  
`best` nimmt automatisch die höchste verfügbare Qualität.

**5. Speicherort festlegen**  
Standard ist dein **Downloads**-Ordner. Mit **Ändern** kannst du einen anderen Ordner wählen.

**6. Download starten**  
Klick auf **Download starten**. Du siehst live Fortschritt, Geschwindigkeit und verbleibende Zeit.

**7. Fertig**  
Unten erscheint grün: **✓ Fertig! Gespeichert in: ...** – die Datei liegt im gewählten Ordner.

---

## 🌐 Unterstützte Seiten

YouTube, TikTok, Instagram, Twitter/X, Reddit und über **1000 weitere Seiten** – alles was [yt-dlp](https://github.com/yt-dlp/yt-dlp) unterstützt.

---

## ❓ Häufige Probleme

| Problem | Lösung |
|---|---|
| `pip` wird nicht erkannt | Python neu installieren und „Add to PATH" anhaken |
| MP3 funktioniert nicht | ffmpeg installieren: `winget install ffmpeg` |
| Video nicht gefunden | URL nochmal kopieren, manchmal läuft die Session ab |
| Schwarzes Fenster öffnet sich kurz und schließt | CMD benutzen statt Doppelklick |
