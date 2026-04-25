import customtkinter as ctk
import threading
import os
import sys
from pathlib import Path
import subprocess

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG      = "#0e0e12"
CARD    = "#16161e"
ACCENT  = "#ff2d55"
ACCENT2 = "#ff9f0a"
TEXT    = "#f0f0f5"
MUTED   = "#6e6e80"
SUCCESS = "#30d158"
ERROR   = "#ff453a"

def ensure_deps():
    try:
        import yt_dlp
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp", "-q"])

class DownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MediaGrab")
        self.geometry("620x580")
        self.resizable(False, False)
        self.configure(fg_color=BG)

        self._output_dir = str(Path.home() / "Downloads")
        self._mode = ctk.StringVar(value="video")
        self._quality = ctk.StringVar(value="best")
        self._busy = False

        self._build_ui()

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0, height=64)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="⬇  MediaGrab",
                     font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"),
                     text_color=ACCENT).pack(side="left", padx=24)
        ctk.CTkLabel(header, text="YouTube · TikTok · und mehr",
                     font=ctk.CTkFont(size=12), text_color=MUTED).pack(side="left")

        # Card
        card = ctk.CTkFrame(self, fg_color=CARD, corner_radius=16)
        card.pack(padx=24, pady=20, fill="both", expand=True)

        # URL
        ctk.CTkLabel(card, text="URL", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=MUTED).pack(anchor="w", padx=20, pady=(20, 4))
        self.url_entry = ctk.CTkEntry(
            card, height=44, placeholder_text="https://youtube.com/watch?v=... oder TikTok-Link",
            font=ctk.CTkFont(size=13), fg_color="#1e1e2a", border_color="#2a2a3a",
            text_color=TEXT, corner_radius=10)
        self.url_entry.pack(fill="x", padx=20)

        # Mode buttons
        ctk.CTkLabel(card, text="FORMAT", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=MUTED).pack(anchor="w", padx=20, pady=(18, 6))
        mode_row = ctk.CTkFrame(card, fg_color="transparent")
        mode_row.pack(fill="x", padx=20)
        self._btn_video = self._make_mode_btn(mode_row, "🎬  Video (MP4)", "video")
        self._btn_audio = self._make_mode_btn(mode_row, "🎵  Nur Audio (MP3)", "audio")
        self._btn_video.pack(side="left", padx=(0, 8))
        self._btn_audio.pack(side="left")

        # Quality — must be created BEFORE _update_mode_buttons is called
        ctk.CTkLabel(card, text="QUALITÄT", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=MUTED).pack(anchor="w", padx=20, pady=(18, 6))
        self.quality_menu = ctk.CTkOptionMenu(
            card,
            values=["best", "1080p", "720p", "480p", "360p"],
            variable=self._quality,
            fg_color="#1e1e2a", button_color=ACCENT, button_hover_color="#cc2244",
            dropdown_fg_color="#1e1e2a", text_color=TEXT,
            font=ctk.CTkFont(size=13), corner_radius=10, width=160)
        self.quality_menu.pack(anchor="w", padx=20)

        # Now safe to call
        self._update_mode_buttons()

        # Folder
        ctk.CTkLabel(card, text="SPEICHERORT", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=MUTED).pack(anchor="w", padx=20, pady=(18, 6))
        folder_row = ctk.CTkFrame(card, fg_color="transparent")
        folder_row.pack(fill="x", padx=20)
        self.folder_label = ctk.CTkLabel(
            folder_row, text=self._output_dir, text_color=MUTED,
            font=ctk.CTkFont(size=12), anchor="w")
        self.folder_label.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(
            folder_row, text="Ändern", width=80, height=28,
            fg_color="#2a2a3a", hover_color="#3a3a4a", text_color=TEXT,
            font=ctk.CTkFont(size=12), corner_radius=8,
            command=self._pick_folder).pack(side="right")

        # Download button
        self.dl_btn = ctk.CTkButton(
            card, text="Download starten", height=48,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=ACCENT, hover_color="#cc2244",
            corner_radius=12, command=self._start_download)
        self.dl_btn.pack(fill="x", padx=20, pady=(24, 12))

        # Progress bar
        self.progress = ctk.CTkProgressBar(card, height=6, corner_radius=3,
                                            fg_color="#1e1e2a", progress_color=ACCENT)
        self.progress.pack(fill="x", padx=20, pady=(0, 8))
        self.progress.set(0)

        # Status row: links Status, rechts ETA
        status_row = ctk.CTkFrame(card, fg_color="transparent")
        status_row.pack(fill="x", padx=20, pady=(0, 16))

        self.status = ctk.CTkLabel(status_row, text="Bereit.", font=ctk.CTkFont(size=12),
                                   text_color=MUTED, anchor="w")
        self.status.pack(side="left", fill="x", expand=True)

        self.eta_label = ctk.CTkLabel(status_row, text="", font=ctk.CTkFont(size=12, weight="bold"),
                                      text_color=ACCENT2, anchor="e")
        self.eta_label.pack(side="right")

    def _make_mode_btn(self, parent, text, value):
        def on_click():
            self._mode.set(value)
            self._update_mode_buttons()
        return ctk.CTkButton(parent, text=text, width=180, height=40,
                             font=ctk.CTkFont(size=13), corner_radius=10, command=on_click)

    def _update_mode_buttons(self):
        is_video = self._mode.get() == "video"
        self._btn_video.configure(
            fg_color=ACCENT if is_video else "#1e1e2a",
            hover_color="#cc2244" if is_video else "#2a2a3a", text_color=TEXT)
        self._btn_audio.configure(
            fg_color=ACCENT2 if not is_video else "#1e1e2a",
            hover_color="#cc8800" if not is_video else "#2a2a3a", text_color=TEXT)
        self.quality_menu.configure(state="normal" if is_video else "disabled")

    def _pick_folder(self):
        from tkinter import filedialog
        folder = filedialog.askdirectory(initialdir=self._output_dir)
        if folder:
            self._output_dir = folder
            self.folder_label.configure(text=folder)

    def _start_download(self):
        if self._busy:
            return
        url = self.url_entry.get().strip()
        if not url:
            self._set_status("Bitte eine URL eingeben.", ERROR)
            return
        self._busy = True
        self.dl_btn.configure(state="disabled", text="Lädt...")
        self.progress.set(0)
        self.eta_label.configure(text="")
        self._set_status("Download wird vorbereitet...", MUTED)
        threading.Thread(target=self._download_thread, args=(url,), daemon=True).start()

    def _download_thread(self, url):
        try:
            import yt_dlp

            mode    = self._mode.get()
            quality = self._quality.get()
            out_dir = self._output_dir

            def progress_hook(d):
                if d["status"] == "downloading":
                    total   = d.get("total_bytes") or d.get("total_bytes_estimate") or 1
                    current = d.get("downloaded_bytes", 0)
                    pct     = current / total
                    speed   = d.get("_speed_str", "").strip()
                    eta_sec = d.get("eta")
                    if eta_sec is not None:
                        m, s = divmod(int(eta_sec), 60)
                        eta_str = f"⏱ noch ~{m}:{s:02d} min" if m else f"⏱ noch ~{s}s"
                    else:
                        eta_str = ""
                    self.after(0, lambda p=pct, sp=speed, e=eta_str: (
                        self.progress.set(p),
                        self._set_status(f"Lädt...  {int(p*100)}%  –  {sp}", MUTED),
                        self.eta_label.configure(text=e)
                    ))
                elif d["status"] == "finished":
                    self.after(0, lambda: (
                        self.progress.set(1),
                        self._set_status("Wird verarbeitet...", MUTED),
                        self.eta_label.configure(text="")
                    ))

            if mode == "audio":
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": os.path.join(out_dir, "%(title)s.%(ext)s"),
                    "postprocessors": [{"key": "FFmpegExtractAudio",
                                        "preferredcodec": "mp3", "preferredquality": "192"}],
                    "progress_hooks": [progress_hook],
                    "quiet": True,
                }
            else:
                fmt_map = {
                    "best":  "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                    "1080p": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
                    "720p":  "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]",
                    "480p":  "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]",
                    "360p":  "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360]",
                }
                ydl_opts = {
                    "format": fmt_map.get(quality, fmt_map["best"]),
                    "outtmpl": os.path.join(out_dir, "%(title)s.%(ext)s"),
                    "merge_output_format": "mp4",
                    "progress_hooks": [progress_hook],
                    "quiet": True,
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.after(0, self._on_success)

        except Exception as e:
            err_msg = str(e)
            # Erkennung ob Video nicht gefunden / nicht verfügbar
            not_found_keywords = [
                "Video unavailable", "not available", "404", "does not exist",
                "This video is unavailable", "keine", "not found", "Unable to extract"
            ]
            if any(k.lower() in err_msg.lower() for k in not_found_keywords):
                self.after(0, lambda: self._on_error("❌ Video konnte nicht gefunden werden."))
            else:
                self.after(0, lambda: self._on_error(f"Fehler: {err_msg[:100]}"))

    def _on_success(self):
        self._set_status(f"✓ Fertig! Gespeichert in: {self._output_dir}", SUCCESS)
        self.eta_label.configure(text="")
        self._reset()

    def _on_error(self, msg):
        self._set_status(msg, ERROR)
        self.progress.set(0)
        self.eta_label.configure(text="")
        self._reset()

    def _reset(self):
        self._busy = False
        self.dl_btn.configure(state="normal", text="Download starten")

    def _set_status(self, msg, color=None):
        self.status.configure(text=msg, text_color=color or MUTED)


if __name__ == "__main__":
    ensure_deps()
    app = DownloaderApp()
    app.mainloop()
