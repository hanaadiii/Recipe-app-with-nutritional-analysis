import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict
import re

FALLBACK_NUTRITION = {
    "egg": {"calories": 155, "proteins": 13.0, "fats": 11.0, "carbs": 1.1},
    "chicken breast": {"calories": 165, "proteins": 31.0, "fats": 3.6, "carbs": 0.0},
    "flour": {"calories": 364, "proteins": 10.0, "fats": 1.0, "carbs": 76.0},
    "sugar": {"calories": 387, "proteins": 0.0, "fats": 0.0, "carbs": 100.0},
    "butter": {"calories": 717, "proteins": 0.85, "fats": 81.0, "carbs": 0.06},
    "milk": {"calories": 42, "proteins": 3.4, "fats": 1.0, "carbs": 5.0},
    "olive oil": {"calories": 884, "proteins": 0.0, "fats": 100.0, "carbs": 0.0},
}

def parse_number(text: str) -> Optional[float]:
    if text is None:
        return None
    m = re.search(r"[\d,.]+", text)
    if not m:
        return None
    s = m.group(0).replace(",", ".")
    try:
        return float(s)
    except:
        return None

def scrape_nutrition_by_name(name: str) -> Dict[str, float]:

    key = name.strip().lower()

    if key in FALLBACK_NUTRITION:
        return FALLBACK_NUTRITION[key]

    try:
        search_url = f"https://www.nutritionvalue.org/search.php?food_query={requests.utils.requote_uri(name)}"
        resp = requests.get(search_url, timeout=6)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            a = soup.find("a", href=True, string=re.compile(re.escape(name), re.IGNORECASE))
            if not a:
                first_result = soup.select_one("div#content a[href]")
                if first_result:
                    href = first_result["href"]
                else:
                    href = None
            else:
                href = a["href"]

            if href:
                if href.startswith("/"):
                    href = "https://www.nutritionvalue.org" + href
                r2 = requests.get(href, timeout=6)
                if r2.status_code == 200:
                    s2 = BeautifulSoup(r2.text, "html.parser")
                    text = s2.get_text(" ", strip=True)
                    def find_after(term):
                        idx = text.lower().find(term.lower())
                        if idx == -1:
                            return None
                        snippet = text[idx: idx + 200]
                        return parse_number(snippet)

                    calories = find_after("calories")
                    proteins = find_after("protein")
                    fats = find_after("fat")
                    carbs = find_after("carbohydrate") or find_after("carb")
                    if calories is not None:
                        return {
                            "calories": float(calories) if calories is not None else 0.0,
                            "proteins": float(proteins) if proteins is not None else 0.0,
                            "fats": float(fats) if fats is not None else 0.0,
                            "carbs": float(carbs) if carbs is not None else 0.0,
                        }
    except Exception:
        pass
    return FALLBACK_NUTRITION.get(key, {"calories": 0.0, "proteins": 0.0, "fats": 0.0, "carbs": 0.0})
