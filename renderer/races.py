"""Race-Episoden. Rendern: python3 renderer/races.py [slug ...]"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import race

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
AO, RG, WI, US = 0.07, 0.44, 0.53, 0.69   # ungefähre Lage der Grand Slams im Jahr
def slams(*items): return [y + s for y, s in items]

RACES = [
 {"slug": "14_big3_grand_slam_race", "kicker": "FEDERER vs NADAL vs DJOKOVIC",
  "headline": "Federer led for 17 years. Then this happened…", "unit": "Grand Slam titles (men's singles)",
  "xrange": (2003.0, 2026.8), "ymax": 26, "grid": [0, 5, 10, 15, 20, 25], "ticks": [2005, 2010, 2015, 2020, 2025],
  "race_dur": 16.0, "end_dur": 3.4, "slow": [(2017.0, 2023.8, 2.4)],
  "callouts": [(2009.53, "Federer breaks the record: 15"), (2020.8, "Nadal ties Federer: 20–20"),
               (2021.53, "20 – 20 – 20 !"), (2022.07, "Nadal takes the lead"), (2023.44, "Djokovic takes over"),
               (2023.69, "24 – the all-time record", 2.4)],
  "end_q": "Who is the real GOAT?",
  "source": "ATP / Grand Slam men's singles champions 2003–2026",
  "title": "The Big 3 Grand Slam race 🎾",
  "caption": "Federer was ahead for 17 years… then Nadal and Djokovic caught him 🎾 Who's the real GOAT? 👇\n\nSource: Grand Slam men's singles champions 2003–2026\n\n#tennis #djokovic #nadal #federer #grandslam #goat #atp #sports #whohasmore",
  "people": [
   {"short": "Federer", "col": (235, 70, 70), "look": {"skin": "fair", "hair": "short", "hair_col": (60, 45, 35), "shirt": (240, 240, 240)},
    "events": slams((2003, WI), (2004, AO), (2004, WI), (2004, US), (2005, WI), (2005, US), (2006, AO), (2006, WI), (2006, US),
                    (2007, AO), (2007, WI), (2007, US), (2008, US), (2009, RG), (2009, WI), (2010, AO), (2012, WI),
                    (2017, AO), (2017, WI), (2018, AO))},
   {"short": "Nadal", "col": (245, 195, 50), "look": {"skin": "tan", "hair": "long", "hair_col": (45, 35, 30), "shirt": (240, 200, 40)},
    "events": slams((2005, RG), (2006, RG), (2007, RG), (2008, RG), (2008, WI), (2009, AO), (2010, RG), (2010, WI), (2010, US),
                    (2011, RG), (2012, RG), (2013, RG), (2013, US), (2014, RG), (2017, RG), (2017, US), (2018, RG),
                    (2019, RG), (2019, US), (2020, 0.78), (2022, AO), (2022, RG))},   # French Open 2020 fand im Oktober statt
   {"short": "Djokovic", "col": (80, 150, 255), "look": {"skin": "fair", "hair": "short", "hair_col": (45, 35, 30), "beard": "stubble", "beard_col": (60, 50, 45), "shirt": (40, 80, 170)},
    "events": slams((2008, AO), (2011, AO), (2011, WI), (2011, US), (2012, AO), (2013, AO), (2014, WI), (2015, AO), (2015, WI),
                    (2015, US), (2016, AO), (2016, RG), (2018, WI), (2018, US), (2019, AO), (2019, WI), (2020, AO),
                    (2021, AO), (2021, RG), (2021, WI), (2022, WI), (2023, AO), (2023, RG), (2023, US))},
  ]},
]
BY_SLUG = {r["slug"]: r for r in RACES}

if __name__ == "__main__":
    slugs = sys.argv[1:] or list(BY_SLUG)
    for s in slugs:
        r = BY_SLUG[s]
        for p in r["people"]: assert p["events"] == sorted(p["events"]), p["short"]
        print(race.render(r, os.path.join(ROOT, "videos")))
        json.dump({"title": r["title"], "caption": r["caption"]}, open(os.path.join(ROOT, "videos", s + ".json"), "w"), ensure_ascii=False, indent=1)
