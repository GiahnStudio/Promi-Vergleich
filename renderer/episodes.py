"""Episoden für "Who has more?" (Englisch). Neues Video = neuer Eintrag in EPISODES.
Rendern: python3 renderer/episodes.py [slug ...]   (ohne Argument: alle)"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import promi_videos as pv

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

def P(name, v, flag, cat, look, col, note=None):
    ini = "".join(w[0] for w in name.replace("-", " ").split()[:2]).upper()
    return {"name": name, "v": v, "flag": flag, "cat": cat, "look": look, "col": col, "ini": ini, **({"note": note} if note else {})}

def build(e):
    ppl = sorted(e["people"], key=lambda p: -p["v"])
    for i, p in enumerate(ppl):
        p["rank"] = 1 + sum(1 for q in ppl if q["v"] > p["v"])
        p["pos"] = i + 1
    groups = []
    for p in ppl:
        if groups and groups[-1][0]["v"] == p["v"]: groups[-1].append(p)
        else: groups.append([p])
    sc = [{"type": "hook", "dur": 2.9, "n": len(ppl), "kicker": e["kicker"], "setup": e["setup"], "question": e["question"], "tip": "Guess in the comments"}]
    for g in reversed(groups):
        a, b = g[0]["pos"], g[-1]["pos"]; top = a == 1
        if len(g) == 1 and top:
            sc.append({"type": "reveal", "dur": 4.3, "reveal_at": 1.1, "p": g[0], "teaser": e.get("teaser", "And number 1 is …")})
        elif len(g) == 1:
            sc.append({"type": "rank", "dur": 2.8 if g[0].get("note") else 2.5, "p": g[0]})
        else:
            for k in range(0, len(g), 3):
                ch = g[k:k + 3]
                sc.append({"type": "tie", "dur": 3.0 + 0.3 * len(ch), "v": g[0]["v"], "ps": ch, "top": top,
                           "head": "#1" if top else f"#{a} – #{b}", "sub": e.get("tie_sub", {}).get(a, "Shared first place!" if top else "It's a tie!"),
                           "each": "Each"})
    sc.append({"type": "board", "dur": 4.2, "head": e["board_head"], "foot": e["foot"]})
    sc.append({"type": "cta", "dur": 3.2, "q": e["cta"], "c": "Drop it in the comments", "btn": "Follow for more rankings"})
    return {"slug": e["slug"], "lang": "en", "brand": "WHO HAS MORE?", "vmax": ppl[0]["v"], "people": ppl[:6],
            "source": e["source"], "fmt": e["fmt"], "unit": e.get("unit"), "scenes": sc}

# ---------------- Looks ----------------
RONALDO = {"skin": "tan", "hair": "short", "hair_col": (40, 30, 25), "shirt": (235, 200, 40), "acc": ["studs"]}
MESSI = {"skin": "fair", "hair": "short", "hair_col": (90, 60, 40), "beard": "full", "beard_col": (90, 60, 40), "shirt": (120, 180, 230)}
cnt = lambda x: f"{round(x)}"

EPISODES = [
 {"slug": "02_highest_paid_athletes", "kicker": "HIGHEST-PAID ATHLETES 2026",
  "setup": "One athlete earned $300 million in a single year", "question": "Who is it?",
  "fmt": lambda x: f"${x:.0f}M", "unit": "earned in 12 months",
  "source": "Forbes, The World's Highest-Paid Athletes 2026 (May 2026), pre-tax", "board_head": "TOP 6 EARNERS 2026",
  "foot": "Ronaldo made more than Messi and LeBron combined.", "cta": "Who should be on this list?",
  "title": "Who earned $300M in one year?",
  "caption": "The highest-paid athletes of 2026 💰 Number 1 earned more than #3 and #4 combined. Did you guess right? 👇\n\nSource: Forbes (May 2026)\n\n#ronaldo #messi #lebron #forbes #sports #money #athletes #football #whohasmore",
  "people": [
   P("Cristiano Ronaldo", 300, "PT", "Football · Al Nassr", RONALDO, (200, 160, 40), "More than double what Messi earned."),
   P("Canelo Álvarez", 170, "MX", "Boxing", {"skin": "fair", "hair": "short", "hair_col": (190, 95, 50), "beard": "short", "beard_col": (180, 90, 50), "shirt": (190, 40, 40)}, (220, 70, 60)),
   P("Lionel Messi", 140, "AR", "Football · Inter Miami", MESSI, (90, 150, 220)),
   P("LeBron James", 138, "US", "Basketball", {"skin": "dark", "hair": "bald", "beard": "full", "beard_col": (30, 25, 25), "shirt": (85, 37, 130)}, (150, 90, 220)),
   P("Shohei Ohtani", 128, "JP", "Baseball", {"skin": "light", "hair": "short", "hair_col": (25, 22, 25), "shirt": (0, 90, 160)}, (60, 120, 200)),
   P("Stephen Curry", 125, "US", "Basketball", {"skin": "medium", "hair": "short", "hair_col": (30, 22, 20), "beard": "stubble", "beard_col": (30, 22, 20), "shirt": (29, 66, 138)}, (230, 180, 50)),
  ]},
 {"slug": "03_most_ballon_dor", "kicker": "BALLON D'OR RECORD",
  "setup": "Harry Kane just won his first Ballon d'Or", "question": "Who has won the most ever?",
  "fmt": cnt, "unit": "Ballon d'Or wins",
  "source": "France Football / Ballon d'Or records (as of Oct 2026)", "board_head": "MOST BALLON D'OR WINS",
  "foot": "Messi has as many as Ronaldo and Cruyff combined.", "cta": "Will anyone ever catch Messi?",
  "title": "Most Ballon d'Ors of all time",
  "caption": "Harry Kane just won his first Ballon d'Or 🏆 But how far away is the record? 👇\n\nSource: Ballon d'Or records (Oct 2026)\n\n#ballondor #messi #ronaldo #harrykane #football #soccer #goat #whohasmore",
  "people": [
   P("Lionel Messi", 8, "AR", "Argentina", MESSI, (90, 150, 220), "The all-time record. Nobody else has more than 5."),
   P("Cristiano Ronaldo", 5, "PT", "Portugal", RONALDO, (200, 160, 40)),
   P("Johan Cruyff", 3, "NL", "Netherlands", {"skin": "fair", "hair": "long", "hair_col": (110, 75, 45), "shirt": (240, 120, 30)}, (230, 120, 40)),
   P("Michel Platini", 3, "FR", "France", {"skin": "fair", "hair": "curly", "hair_col": (95, 65, 40), "shirt": (30, 60, 150)}, (60, 90, 200)),
   P("Marco van Basten", 3, "NL", "Netherlands", {"skin": "fair", "hair": "short", "hair_col": (170, 130, 80), "shirt": (200, 40, 40)}, (200, 60, 60)),
  ]},
 {"slug": "04_most_instagram_followers", "kicker": "MOST FOLLOWED ON INSTAGRAM",
  "setup": "One person has almost 700 million followers", "question": "Who is it?",
  "fmt": lambda x: f"{x:.0f}M", "unit": "followers",
  "source": "Instagram follower counts (Sept 2026), via Wikipedia list", "board_head": "MOST FOLLOWED PEOPLE",
  "foot": "The Rock and Kylie Jenner are only 1 million apart.", "cta": "Who will pass Ronaldo first?",
  "title": "Who has the most Instagram followers?",
  "caption": "The most followed people on Instagram 📱 One of them has more followers than the USA has people. Who's #1? 👇\n\nSource: Instagram counts (Sept 2026)\n\n#instagram #ronaldo #selenagomez #therock #kyliejenner #followers #celebrities #whohasmore",
  "people": [
   P("Cristiano Ronaldo", 679, "PT", "Football", RONALDO, (200, 160, 40), "The first person ever to pass 600 million."),
   P("Lionel Messi", 517, "AR", "Football", MESSI, (90, 150, 220)),
   P("Selena Gomez", 403, "US", "Singer · Actress", {"skin": "tan", "hair": "long", "hair_col": (45, 30, 25), "lips": (190, 70, 90), "shirt": (230, 120, 170), "acc": ["studs"]}, (220, 100, 160), "The most followed woman on Instagram."),
   P("Dwayne Johnson", 381, "US", "Actor", {"skin": "brown", "hair": "bald", "beard": "goatee", "beard_col": (40, 30, 25), "shirt": (30, 30, 36)}, (120, 120, 140)),
   P("Kylie Jenner", 380, "US", "Kylie Cosmetics", {"skin": "tan", "hair": "long", "hair_col": (25, 20, 20), "lips": (180, 90, 100), "shirt": (240, 200, 210)}, (230, 140, 170)),
   P("Ariana Grande", 362, "US", "Singer · Actress", {"skin": "tan", "hair": "bun", "hair_col": (100, 70, 45), "lips": (200, 110, 120), "shirt": (190, 170, 230)}, (170, 140, 230)),
  ]},
 {"slug": "05_most_acting_oscars", "kicker": "OSCAR RECORD",
  "setup": "Sean Penn just won his 3rd Oscar", "question": "But who has the most acting Oscars?",
  "fmt": cnt, "unit": "acting Oscars",
  "source": "Academy Awards database (through the 98th Oscars, 2026), competitive acting wins", "board_head": "MOST ACTING OSCARS",
  "foot": "Only 8 actors in history have won 3 or more.", "cta": "Who will be next to win 3?",
  "title": "Most acting Oscars ever",
  "caption": "Sean Penn just joined one of Hollywood's most exclusive clubs 🏆 But one actress is still unbeaten. Who? 👇\n\nSource: Academy Awards (98th Oscars, 2026)\n\n#oscars #academyawards #merylstreep #seanpenn #hollywood #movies #actors #whohasmore",
  "tie_sub": {2: "3 Oscars each"},
  "people": [
   P("Katharine Hepburn", 4, "US", "Actress · 1907–2003", {"skin": "light", "hair": "bun", "hair_col": (150, 75, 45), "lips": (180, 60, 60), "shirt": (120, 120, 130)}, (200, 120, 80), "Unbeaten since 1982 – four wins, all for Best Actress."),
   P("Meryl Streep", 3, "US", "Actress", {"skin": "light", "hair": "long", "hair_col": (215, 200, 170), "glasses": "round", "shirt": (40, 50, 90)}, (100, 110, 180)),
   P("Jack Nicholson", 3, "US", "Actor", {"skin": "fair", "hair": "buzz", "hair_col": (120, 110, 100), "glasses": "sun", "shirt": (25, 25, 30)}, (90, 90, 110)),
   P("Daniel Day-Lewis", 3, "GB", "Actor", {"skin": "fair", "hair": "short", "hair_col": (130, 120, 110), "beard": "stubble", "beard_col": (110, 100, 95), "shirt": (40, 80, 60)}, (70, 140, 100)),
   P("Frances McDormand", 3, "US", "Actress", {"skin": "fair", "hair": "short", "hair_col": (185, 185, 180), "shirt": (70, 100, 150)}, (100, 140, 190)),
   P("Sean Penn", 3, "US", "Actor · new in 2026", {"skin": "fair", "hair": "short", "hair_col": (140, 125, 110), "beard": "stubble", "beard_col": (130, 120, 110), "shirt": (50, 50, 60)}, (150, 130, 110)),
  ]},
 {"slug": "06_most_marriages", "kicker": "MOST MARRIED STARS",
  "setup": "Two stars walked down the aisle 8 times", "question": "Can you name them?",
  "fmt": cnt, "unit": "marriages",
  "source": "Guinness World Records, public marriage records", "board_head": "MOST MARRIAGES",
  "foot": "Both #1s married one spouse twice.", "cta": "Who would you add to this list?",
  "title": "Who has been married the most?",
  "caption": "Hollywood's most married stars 💍 Two of them said 'I do' 8 times. Could you guess who? 👇\n\nSources: Guinness World Records, public records\n\n#marriage #hollywood #elizabethtaylor #pamelaanderson #jlo #celebrities #wedding #whohasmore",
  "tie_sub": {1: "8 marriages each!"},
  "people": [
   P("Elizabeth Taylor", 8, "GB", "Actress · 7 husbands", {"skin": "light", "hair": "curly", "hair_col": (25, 20, 25), "lips": (190, 40, 60), "shirt": (110, 60, 160)}, (140, 90, 200)),
   P("Larry King", 8, "US", "TV host · 7 wives", {"skin": "fair", "hair": "buzz", "hair_col": (180, 180, 180), "glasses": "round", "shirt": (130, 170, 220)}, (90, 130, 200)),
   P("Pamela Anderson", 6, "CA", "Actress", {"skin": "light", "hair": "wavy", "hair_col": (240, 215, 150), "lips": (210, 90, 110), "shirt": (210, 40, 50)}, (220, 80, 90)),
   P("Billy Bob Thornton", 6, "US", "Actor", {"skin": "fair", "hair": "short", "hair_col": (80, 60, 45), "beard": "goatee", "beard_col": (80, 65, 55), "shirt": (30, 30, 34)}, (110, 100, 90)),
   P("Nicolas Cage", 5, "US", "Actor", {"skin": "fair", "hair": "long", "hair_col": (60, 45, 35), "beard": "stubble", "beard_col": (60, 50, 40), "shirt": (90, 90, 100)}, (120, 120, 140)),
   P("Jennifer Lopez", 4, "US", "Singer · Actress", {"skin": "tan", "hair": "wavy", "hair_col": (170, 120, 70), "lips": (180, 90, 80), "shirt": (240, 235, 225), "acc": ["hoops"]}, (210, 160, 90)),
  ]},
 # ---------------- Woche 2026-11-02 ----------------
 {"slug": "07_most_grammys", "kicker": "GRAMMY RECORD",
  "setup": "Kendrick Lamar just became the most-awarded rapper ever", "question": "But who has the most Grammys of all?",
  "fmt": cnt, "unit": "Grammy wins",
  "source": "Recording Academy / GRAMMY.com, all-time wins (through the 68th Grammys, 2026)", "board_head": "MOST GRAMMY WINS",
  "foot": "Kendrick Lamar won 5 Grammys in 2026 alone.", "cta": "Will anyone ever catch Beyoncé?",
  "title": "Who has the most Grammys ever?",
  "caption": "Kendrick Lamar now has more Grammys than any rapper in history 🏆 But one artist is still way ahead. Who? 👇\n\nSource: Recording Academy / GRAMMY.com (through the 2026 Grammys)\n\n#grammys #beyonce #kendricklamar #quincyjones #music #awards #records #whohasmore",
  "tie_sub": {3: "28 Grammys each", 5: "27 Grammys each"},
  "people": [
   P("Beyoncé", 35, "US", "Singer", {"skin": "tan", "hair": "wavy", "hair_col": (200, 150, 70), "lips": (180, 80, 80), "shirt": (220, 180, 60), "acc": ["hoops"]}, (220, 170, 60), "The all-time record – 4 more than anyone else."),
   P("Georg Solti", 31, "HU", "Conductor · 1912–1997", {"skin": "fair", "hair": "bald", "shirt": (25, 25, 30)}, (120, 120, 150)),
   P("Quincy Jones", 28, "US", "Producer · 1933–2024", {"skin": "brown", "hair": "buzz", "hair_col": (200, 200, 200), "beard": "short", "beard_col": (210, 210, 210), "glasses": "round", "shirt": (60, 40, 30)}, (170, 120, 80)),
   P("Chick Corea", 28, "US", "Jazz pianist · 1941–2021", {"skin": "fair", "hair": "short", "hair_col": (150, 140, 130), "glasses": "round", "shirt": (40, 90, 140)}, (80, 130, 190)),
   P("Kendrick Lamar", 27, "US", "Rapper · +5 in 2026", {"skin": "brown", "hair": "curly", "hair_col": (25, 20, 20), "beard": "short", "beard_col": (25, 20, 20), "shirt": (30, 30, 34), "acc": ["chain"]}, (200, 60, 60)),
   P("Alison Krauss", 27, "US", "Bluegrass singer", {"skin": "light", "hair": "long", "hair_col": (225, 195, 130), "lips": (190, 100, 100), "shirt": (80, 120, 90)}, (100, 160, 110)),
  ]},
 {"slug": "08_most_f1_titles", "kicker": "FORMULA 1 RECORD",
  "setup": "Only 35 drivers have ever won the F1 world title", "question": "Who has won the most?",
  "fmt": cnt, "unit": "world titles",
  "source": "Formula 1 World Drivers' Champions (through the 2025 season; 2026 still running)", "board_head": "MOST F1 WORLD TITLES",
  "foot": "Nobody has ever won 8 F1 titles.", "cta": "Will anyone ever win 8?",
  "title": "Most F1 world titles ever",
  "caption": "Only two drivers have won 7 F1 world titles 🏎️ Can you name them? 👇\n\nSource: Formula 1 champions list (through 2025)\n\n#f1 #formula1 #hamilton #schumacher #verstappen #racing #motorsport #whohasmore",
  "tie_sub": {1: "7 titles each!", 4: "4 titles each"},
  "people": [
   P("Lewis Hamilton", 7, "GB", "2008 · 2014–15 · 2017–20", {"skin": "medium", "hair": "short", "hair_col": (25, 20, 20), "beard": "stubble", "beard_col": (25, 20, 20), "shirt": (220, 30, 40), "acc": ["studs"]}, (220, 60, 60)),
   P("Michael Schumacher", 7, "DE", "1994–95 · 2000–04", {"skin": "fair", "hair": "short", "hair_col": (95, 70, 50), "shirt": (220, 30, 30)}, (200, 50, 50)),
   P("Juan Manuel Fangio", 5, "AR", "1950s legend", {"skin": "tan", "hair": "short", "hair_col": (60, 45, 35), "shirt": (200, 30, 40)}, (90, 150, 220)),
   P("Alain Prost", 4, "FR", "1985–86 · 1989 · 1993", {"skin": "fair", "hair": "curly", "hair_col": (60, 45, 35), "shirt": (230, 230, 235)}, (60, 90, 200)),
   P("Sebastian Vettel", 4, "DE", "2010–2013", {"skin": "fair", "hair": "short", "hair_col": (170, 130, 80), "beard": "stubble", "beard_col": (150, 115, 75), "shirt": (20, 30, 90)}, (60, 80, 180)),
   P("Max Verstappen", 4, "NL", "2021–2024", {"skin": "fair", "hair": "short", "hair_col": (120, 90, 60), "shirt": (20, 30, 90)}, (240, 120, 30)),
  ]},
 {"slug": "09_billionaire_athletes", "kicker": "FORBES 2026",
  "setup": "Only 5 athletes made Forbes' 2026 celebrity billionaires list", "question": "Who is the richest?",
  "fmt": lambda x: f"${x:.1f}B", "unit": "net worth",
  "source": "Forbes, The World's Celebrity Billionaires 2026 (net worth as of March 1, 2026)", "board_head": "BILLIONAIRE ATHLETES",
  "foot": "Jordan is worth more than Magic and Tiger combined.", "cta": "Who will be the next billionaire athlete?",
  "title": "The richest athletes in the world",
  "caption": "Only 5 athletes are on Forbes' 2026 list of celebrity billionaires 💰 Number 1 is worth more than #2 and #3 combined. Who is it? 👇\n\nSource: Forbes (March 2026)\n\n#forbes #michaeljordan #lebron #tigerwoods #federer #billionaire #money #sports #whohasmore",
  "people": [
   P("Michael Jordan", 4.3, "US", "Basketball legend", {"skin": "dark", "hair": "bald", "beard": "goatee", "beard_col": (40, 35, 35), "shirt": (200, 30, 40)}, (200, 50, 60), "No. 3 among ALL celebrity billionaires."),
   P("Magic Johnson", 1.6, "US", "Basketball legend", {"skin": "dark", "hair": "buzz", "hair_col": (40, 35, 35), "shirt": (85, 37, 130)}, (150, 90, 220)),
   P("Tiger Woods", 1.5, "US", "Golf", {"skin": "brown", "hair": "buzz", "hair_col": (30, 25, 25), "shirt": (200, 30, 40)}, (220, 70, 70)),
   P("LeBron James", 1.4, "US", "Basketball", {"skin": "dark", "hair": "bald", "beard": "full", "beard_col": (30, 25, 25), "shirt": (85, 37, 130)}, (230, 180, 50)),
   P("Roger Federer", 1.1, "CH", "Tennis", {"skin": "fair", "hair": "short", "hair_col": (60, 45, 35), "shirt": (240, 240, 240)}, (220, 60, 60)),
  ]},
 {"slug": "10_most_tiktok_followers", "kicker": "MOST FOLLOWED ON TIKTOK",
  "setup": "Two creators have more than 160 million followers", "question": "Who is #1?",
  "fmt": lambda x: f"{x:.1f}M".replace(".0M", "M"), "unit": "followers",
  "source": "TikTok follower counts, Epidemic Sound ranking (Oct 27, 2026)", "board_head": "MOST FOLLOWED CREATORS",
  "foot": "Khaby Lame leads Charli D'Amelio by under 3 million.", "cta": "Who will pass Khaby Lame?",
  "title": "Who has the most TikTok followers?",
  "caption": "The most followed people on TikTok 📱 The top 2 are less than 3 million apart. Who's #1? 👇\n\nSource: TikTok counts via Epidemic Sound (Oct 2026)\n\n#tiktok #khabylame #charlidamelio #mrbeast #followers #creators #fyp #whohasmore",
  "people": [
   P("Khaby Lame", 163, "IT", "Comedy creator", {"skin": "dark", "hair": "buzz", "hair_col": (25, 20, 20), "shirt": (240, 240, 240)}, (90, 200, 200), "The most followed person on TikTok."),
   P("Charli D'Amelio", 160.3, "US", "Dancer", {"skin": "light", "hair": "long", "hair_col": (70, 50, 35), "lips": (200, 110, 120), "shirt": (240, 180, 200)}, (230, 130, 170)),
   P("MrBeast", 145, "US", "YouTuber", {"skin": "light", "hair": "short", "hair_col": (90, 65, 40), "beard": "short", "beard_col": (90, 65, 40), "shirt": (60, 140, 230)}, (60, 140, 230)),
   P("Bella Poarch", 91.5, "US", "Singer · Creator", {"skin": "tan", "hair": "long_bangs", "hair_col": (25, 20, 25), "lips": (190, 90, 110), "shirt": (230, 120, 170)}, (220, 100, 160)),
   P("Addison Rae", 87.6, "US", "Singer · Actress", {"skin": "tan", "hair": "long", "hair_col": (80, 55, 35), "lips": (200, 110, 110), "shirt": (30, 30, 34)}, (170, 140, 230)),
   P("Willie Salim", 87.2, "ID", "Creator", {"skin": "light", "hair": "short", "hair_col": (25, 20, 20), "shirt": (240, 200, 40)}, (220, 180, 50)),
  ]},
 {"slug": "11_most_grand_slams", "kicker": "TENNIS RECORD",
  "setup": "Alexander Zverev won 2 Grand Slams this year", "question": "But who has the most ever?",
  "fmt": cnt, "unit": "Grand Slam singles titles",
  "source": "ATP / Grand Slam men's singles records (as of Nov 2026)", "board_head": "MOST GRAND SLAM TITLES (MEN)",
  "foot": "Djokovic, Nadal and Federer: 66 Grand Slams combined.", "cta": "Can Alcaraz or Sinner catch Djokovic?",
  "title": "Most Grand Slam titles ever (men)",
  "caption": "Zverev won the French Open AND the US Open in 2026 🎾 But how far is he from the record? 👇\n\nSource: ATP Grand Slam records (Nov 2026)\n\n#tennis #djokovic #nadal #federer #grandslam #usopen #atp #whohasmore",
  "people": [
   P("Novak Djokovic", 24, "RS", "Serbia", {"skin": "fair", "hair": "short", "hair_col": (45, 35, 30), "beard": "stubble", "beard_col": (60, 50, 45), "shirt": (200, 40, 50)}, (200, 60, 70), "The men's record – and he's still playing."),
   P("Rafael Nadal", 22, "ES", "Spain · 14x French Open", {"skin": "tan", "hair": "long", "hair_col": (45, 35, 30), "shirt": (240, 200, 40)}, (230, 170, 40)),
   P("Roger Federer", 20, "CH", "Switzerland · 8x Wimbledon", {"skin": "fair", "hair": "short", "hair_col": (60, 45, 35), "shirt": (240, 240, 240)}, (220, 60, 60)),
   P("Pete Sampras", 14, "US", "USA", {"skin": "tan", "hair": "short", "hair_col": (40, 30, 25), "shirt": (240, 240, 240)}, (90, 130, 200)),
   P("Roy Emerson", 12, "AU", "Australia · 1960s", {"skin": "fair", "hair": "short", "hair_col": (60, 45, 35), "shirt": (240, 240, 240)}, (60, 160, 90)),
  ]},
 {"slug": "12_most_hot100_number_ones", "kicker": "BILLBOARD RECORD",
  "setup": "Taylor Swift scored her 15th No. 1 hit this year", "question": "Which solo artist has the most?",
  "fmt": cnt, "unit": "Hot 100 No. 1 hits",
  "source": "Billboard Hot 100, most No. 1s by solo artists (as of Sept 2026)", "board_head": "MOST NO. 1 HITS (SOLO)",
  "foot": "Only The Beatles (20) have more No. 1s than Mariah.", "cta": "Will Taylor Swift catch Mariah?",
  "title": "Most No. 1 hits by a solo artist",
  "caption": "Taylor Swift got her 15th Billboard No. 1 this year 🎶 But one solo artist still has way more. Who? 👇\n\nSource: Billboard Hot 100 (Sept 2026)\n\n#billboard #taylorswift #mariahcarey #rihanna #drake #michaeljackson #music #whohasmore",
  "tie_sub": {3: "14 No. 1s each"},
  "people": [
   P("Mariah Carey", 19, "US", "Singer", {"skin": "tan", "hair": "wavy", "hair_col": (215, 170, 100), "lips": (200, 90, 110), "shirt": (230, 200, 230)}, (220, 140, 200), "The solo record – only The Beatles have more."),
   P("Taylor Swift", 15, "US", "Singer · 2 new No. 1s in 2026", {"skin": "light", "hair": "long_bangs", "hair_col": (215, 185, 120), "lips": (200, 40, 50), "shirt": (150, 110, 200)}, (170, 120, 220)),
   P("Rihanna", 14, "BB", "Singer", {"skin": "brown", "hair": "long", "hair_col": (40, 25, 25), "lips": (170, 40, 60), "shirt": (30, 30, 34), "acc": ["hoops"]}, (200, 80, 100)),
   P("Drake", 14, "CA", "Rapper · solo male record", {"skin": "medium", "hair": "buzz", "hair_col": (25, 20, 20), "beard": "full", "beard_col": (25, 20, 20), "shirt": (30, 30, 34), "acc": ["chain"]}, (230, 180, 50)),
   P("Michael Jackson", 13, "US", "King of Pop · 1958–2009", {"skin": "light", "hair": "curly", "hair_col": (20, 15, 15), "shirt": (200, 30, 40)}, (200, 50, 60)),
   P("Madonna", 12, "US", "Queen of Pop", {"skin": "light", "hair": "wavy", "hair_col": (235, 215, 160), "lips": (200, 30, 50), "shirt": (30, 30, 34)}, (230, 120, 170)),
  ]},
 {"slug": "13_box_office_stars", "kicker": "BOX OFFICE RECORD",
  "setup": "The #1 star at the box office made $30 billion – mostly with cameos", "question": "Who is it?",
  "fmt": lambda x: f"${x:.1f}B", "unit": "worldwide box office",
  "source": "The Numbers, lifetime worldwide box office, all roles incl. voice & cameos, not inflation-adjusted (Nov 2026)", "board_head": "BIGGEST BOX OFFICE STARS",
  "foot": "All roles count – cameos and voice roles too.", "cta": "Who should be #1?",
  "title": "The biggest box office stars ever",
  "caption": "The #1 box office star of all time mostly made cameos 🎬 And some of the top 6 got there with voice roles. Who's #1? 👇\n\nSource: The Numbers (worldwide box office, all roles, Nov 2026)\n\n#boxoffice #marvel #stanlee #samuelljackson #pixar #movies #hollywood #whohasmore",
  "people": [
   P("Stan Lee", 30.5, "US", "Marvel creator · 1922–2018", {"skin": "fair", "hair": "short", "hair_col": (220, 220, 220), "beard": "short", "beard_col": (220, 220, 220), "glasses": "sun", "shirt": (40, 60, 120)}, (200, 50, 60), "Famous for his cameos in Marvel movies."),
   P("Samuel L. Jackson", 28.4, "US", "Actor", {"skin": "dark", "hair": "bald", "beard": "goatee", "beard_col": (200, 200, 200), "shirt": (30, 30, 34)}, (120, 120, 150)),
   P("John Ratzenberger", 18.5, "US", "Pixar voice actor", {"skin": "fair", "hair": "short", "hair_col": (120, 100, 80), "beard": "short", "beard_col": (130, 110, 90), "shirt": (70, 110, 160)}, (80, 160, 220)),
   P("Frank Welker", 17.5, "US", "Voice actor", {"skin": "fair", "hair": "short", "hair_col": (180, 180, 180), "shirt": (110, 70, 160)}, (150, 100, 200)),
   P("Alan Tudyk", 16.4, "US", "Actor · Disney voices", {"skin": "fair", "hair": "short", "hair_col": (110, 85, 60), "beard": "stubble", "beard_col": (110, 85, 60), "shirt": (60, 120, 90)}, (90, 170, 120)),
   P("Robert Downey Jr.", 16.2, "US", "Actor", {"skin": "fair", "hair": "short", "hair_col": (40, 30, 25), "beard": "goatee", "beard_col": (40, 30, 25), "glasses": "sun", "shirt": (180, 30, 40)}, (200, 160, 50)),
  ]},
]
BY_SLUG = {e["slug"]: e for e in EPISODES}

if __name__ == "__main__":
    from multiprocessing import Pool
    slugs = sys.argv[1:] or list(BY_SLUG)
    def go(s): return pv.render(build(BY_SLUG[s]), os.path.join(ROOT, "videos"))
    with Pool(3) as p:
        for r in p.map(go, slugs): print(r)
    for s in slugs:
        v = build(BY_SLUG[s]); pv.frame(v, 1.9).save(os.path.join(ROOT, "covers", s + "_cover.jpg"), quality=88)
        e = BY_SLUG[s]
        json.dump({"title": e["title"], "caption": e["caption"]}, open(os.path.join(ROOT, "videos", s + ".json"), "w"), ensure_ascii=False, indent=1)
