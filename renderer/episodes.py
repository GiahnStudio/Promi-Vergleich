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
