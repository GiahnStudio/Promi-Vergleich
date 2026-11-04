# Who has more? – Pipeline

TikTok-Account **@who.has.more1** (Englisch). Promi-Vergleiche, Comic-Avatare statt Fotos.

## Formate (Stand 4.11.2026: Ranglisten liefen schwach – 250–900 Views, kaum Likes)
- **Race (Hauptformat, 5 von 7 Videos/Woche):** `renderer/races.py` + `renderer/race.py`. Duell von 2–3 Promis über die Zeit (Linien mit Comic-Köpfen, Überholmanöver, Callouts). Vorbild: `14_big3_grand_slam_race`.
- **Ranking (Nebenformat, 2 von 7):** `renderer/episodes.py` (Countdown-Rangliste).

### Gute Race-Themen
- Bekannte Rivalitäten mit Führungswechseln: Ronaldo vs Messi (Tore, Titel), Swift vs Drake (Hot-100-Hits), Hamilton vs Verstappen (Siege), LeBron vs Jordan (Punkte), Promi-Follower über die Jahre …
- Überraschende Gegenüberstellungen, die Kommentare auslösen.
- Nur mit **jahrgenauen, belegbaren Daten** (offizielle Siegerlisten, Award-Datenbanken, Wikipedia-Tabellen pro Jahr). Keine geschätzten Verlaufsdaten erfinden oder interpolieren, wenn nur Endwerte bekannt sind. Event-Listen vor dem Rendern auf Endsummen prüfen.

### Race-Regeln
- `headline` = Neugier-Hook, sichtbar ab Sekunde 0 (z. B. "X led for 17 years. Then this happened…"). Muss stimmen.
- 3–6 `callouts` an echten Wendepunkten (Gleichstand, Überholen, Rekord); `slow` für die spannende Phase; `race_dur` 14–17 s, `end_dur` ~3,4 s.
- `end_q` = Diskussionsfrage ("Who is the real GOAT?").
- Frames bei Callouts und am Ende prüfen: Köpfe/Labels dürfen nicht überlappen oder rechts aus dem Bild laufen.
Gepostet wird über Metricool, Marke **"Who has more?"**, blogId `7714006`, Zeitzone Europe/Madrid.

## Wöchentlicher Ablauf (geplante Aufgabe, sonntags)
1. Repo klonen (Schreibzugriff), `TOPICS.md` lesen: Bereits gepostete Themen nicht wiederholen.
2. 7 neue Themen wählen (Mix: Geld, Sport, Musik, Film, Social Media, Rekorde, Kurioses). Bevorzugt aktuelle Anlässe (Award gerade vergeben, neue Forbes-Liste …).
3. Jede Zahl per Websuche aus einer aktuellen, seriösen Quelle prüfen (Forbes, Guinness, offizielle Award-Datenbanken, Wikipedia-Listen mit Datum). Keine Themen mit unsicheren/umstrittenen Zahlen. Jede `note`/`foot`/Caption-Aussage nachrechnen.
4. 5 Race-Episoden in `renderer/races.py` und 2 Ranking-Episoden in `renderer/episodes.py` anlegen (Struktur wie bestehende: 5–6 Personen, `look` mit Erkennungsmerkmalen, `fmt`, `unit`, `source`, `title`, `caption` mit Quelle + Hashtags inkl. #whohasmore). Fortlaufende Nummern im `slug`.
5. Rendern: `python3 renderer/races.py <slugs…>` bzw. `python3 renderer/episodes.py <slugs…>`, einige Frames als Bild prüfen (Überlappungen, Textlänge).
6. Commit + Push auf `main`. Video-URL: `https://raw.githubusercontent.com/GiahnStudio/Promi-Vergleich/main/videos/<slug>.mp4`
7. Reihenfolge abwechseln (nie 2 Rankings hintereinander). In Metricool je ein TikTok-Post pro Tag um 20:00 Europe/Madrid einplanen – ab dem ersten Tag ohne bereits geplanten Post, 7 Tage am Stück (Tage mit vorhandenem Post überspringen, nie zwei Posts am selben Tag) (privacyOption PUBLIC_TO_EVERYONE, title = `title`, text = `caption`, kein videoThumbnailUrl – privates Konto).
8. Vorher prüfen, ob frühere **Who-has-more-Posts** (Text enthält `#whohasmore`, erstellt ab 2026-10-29 21:30) mit Status ERROR existieren (getScheduledPosts); dann Fehler melden statt weiter einzuplanen. Alte Facts-Germany-Posts (deutsch, ohne #whohasmore, Entwürfe oder ERROR vom 29.10.) ignorieren und nie anfassen.
9. Themen in `TOPICS.md` eintragen, pushen, kurze Zusammenfassung an GIAHN senden – inkl. Views/Likes der Vorwoche pro Format (getAnalyticsDataByMetrics, TikTok posts: TKPO05, TKPO07, TKPO08, TKPO09), damit sichtbar wird, welches Format besser läuft.

## Regeln
- Keine Fotos oder realistischen KI-Bilder echter Personen – nur `cartoon.py`-Avatare.
- Keine erfundenen Zitate, keine Gerüchte, keine sensiblen Themen (Gesundheit, Verbrechen, Politik).
