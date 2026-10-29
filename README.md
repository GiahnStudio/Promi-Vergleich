# Promi Vergleich

Ranking-Shorts mit Promi-Vergleichen („Wer hat mehr?“ / „Who has more?“) für den TikTok-Account „Who has more?“ (Englisch).

- `videos/`: fertige Videos (9:16, MP4). Metricool holt sie über die öffentliche Raw-URL ab.
- `covers/`: Titelbilder
- `renderer/`: Python-Renderer (Pillow + ffmpeg)
  - `promi_specs.py`: Daten und Szenen pro Video, Personen mit Comic-Merkmalen (`look`)
  - `cartoon.py`: Avatar-Baukasten (stilisierte Comic-Figuren, keine Fotos)
  - `promi_videos.py`: Szenen (Hook, Gleichstand, Rang, Reveal, Rangliste, CTA)
  - `data_videos.py`: gemeinsame Basis (Fonts, Audio)

Neue Videos: Personen und Szenen in `promi_specs.py` anlegen, dann `python3 renderer/promi_specs.py`.
