# Who has more? – Pipeline

TikTok-Account **@who.has.more1** (Englisch). Ranking-Videos mit Promi-Vergleichen, Comic-Avatare statt Fotos.
Gepostet wird über Metricool, Marke **"Who has more?"**, blogId `7714006`, Zeitzone Europe/Madrid.

## Wöchentlicher Ablauf (geplante Aufgabe, sonntags)
1. Repo klonen (Schreibzugriff), `TOPICS.md` lesen: Bereits gepostete Themen nicht wiederholen.
2. 7 neue Themen wählen (Mix: Geld, Sport, Musik, Film, Social Media, Rekorde, Kurioses). Bevorzugt aktuelle Anlässe (Award gerade vergeben, neue Forbes-Liste …).
3. Jede Zahl per Websuche aus einer aktuellen, seriösen Quelle prüfen (Forbes, Guinness, offizielle Award-Datenbanken, Wikipedia-Listen mit Datum). Keine Themen mit unsicheren/umstrittenen Zahlen. Jede `note`/`foot`/Caption-Aussage nachrechnen.
4. Episoden in `renderer/episodes.py` anlegen (Struktur wie bestehende: 5–6 Personen, `look` mit Erkennungsmerkmalen, `fmt`, `unit`, `source`, `title`, `caption` mit Quelle + Hashtags inkl. #whohasmore). Fortlaufende Nummern im `slug`.
5. Rendern: `python3 renderer/episodes.py <slugs…>`, einige Frames als Bild prüfen (Überlappungen, Textlänge).
6. Commit + Push auf `main`. Video-URL: `https://raw.githubusercontent.com/GiahnStudio/Promi-Vergleich/main/videos/<slug>.mp4`
7. In Metricool je ein TikTok-Post Mo–So 20:00 Europe/Madrid einplanen (privacyOption PUBLIC_TO_EVERYONE, title = `title`, text = `caption`, kein videoThumbnailUrl – privates Konto).
8. Vorher prüfen, ob frühere Posts mit Status ERROR existieren (getScheduledPosts); dann Fehler melden statt weiter einzuplanen.
9. Themen in `TOPICS.md` eintragen, pushen, kurze Zusammenfassung an GIAHN senden.

## Regeln
- Keine Fotos oder realistischen KI-Bilder echter Personen – nur `cartoon.py`-Avatare.
- Keine erfundenen Zitate, keine Gerüchte, keine sensiblen Themen (Gesundheit, Verbrechen, Politik).
