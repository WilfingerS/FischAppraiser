import requests
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

class MutationModel:
    def __init__(self, user_agent: str):
        self.user_agent = user_agent

        self.raw_file = Path("src/data/mutations_raw.json")
        self.clean_file = Path("src/data/mutations.json")

        self.api_url = "https://fischipedia.org/w/api.php"

        self.params = {
            "action": "parse",
            "page": "Mutations",
            "prop": "text",
            "format": "json"
        }

        self.headers = {
            "User-Agent": user_agent
        }

        self.mutations = []
        self.selected = []

    # ----------------------------
    # DATA IO
    # ----------------------------

    def load(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ----------------------------
    # FETCH
    # ----------------------------

    def fetch(self):
        r = requests.get(self.api_url, params=self.params, headers=self.headers)
        r.raise_for_status()
        return r.json()

    # ----------------------------
    # PARSE
    # ----------------------------

    def extract_mutations(self, raw):
        html = raw["parse"]["text"]["*"]
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", {"id": "mutation-table-1"})
        tbody = table.find("tbody")

        rows = []

        for tr in tbody.find_all("tr")[2:]:
            cell = tr.find("td", class_="appraisable")
            if not cell:
                continue

            if cell.get("title", "").strip().lower() != "yes":
                continue

            name = tr.find("td", class_="name").get_text(strip=True)
            value = tr.find("td", class_="value").get_text(strip=True)

            color = self.extract_hex_color(soup, name)

            rows.append({
                "name": name,
                "value": value,
                "color": color
            })

        return rows

    def extract_hex_color(self, soup, name):
        selector = f".mutation-{name.lower()}"

        for style in soup.find_all("style"):
            if not style.string:
                continue

            css = style.string
            pattern = rf"{re.escape(selector)}\s*\{{(.*?)\}}"
            match = re.search(pattern, css, re.DOTALL)

            if match:
                hex_match = re.search(r"#([0-9a-fA-F]{3,6})", match.group(1))
                if hex_match:
                    return f"#{hex_match.group(1)}"

        return None

    # ----------------------------
    # MAIN GET
    # ----------------------------

    def get_data(self, refresh=False):
        if self.clean_file.exists() and not refresh:
            self.mutations = self.load(self.clean_file)
            return self.mutations

        if self.raw_file.exists() and not refresh:
            raw = self.load(self.raw_file)
        else:
            raw = self.fetch()

        self.mutations = self.extract_mutations(raw)
        self.save(self.clean_file, self.mutations)

        return self.mutations

    def set_area(self, area):
        self.area = area
