import requests
import json
import re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup


class MutationService:
    def __init__(self, user_agent: str):
        self.user_agent = user_agent

        self.raw_file = Path("data/mutations_raw.json")
        self.clean_file = Path("data/mutations.json")

        self.api_url = "https://fischipedia.org/w/api.php"

        self.params = {
            "action": "parse",
            "page": "Mutations",
            "prop": "text",
            "format": "json"
        }

    # ----------------------------
    # FILE IO
    # ----------------------------

    def load(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ----------------------------
    # REFRESH LOGIC
    # ----------------------------

    def get_last_refreshed(self):
        if not self.clean_file.exists():
            return None
        return datetime.fromtimestamp(self.clean_file.stat().st_mtime)

    def get_last_refreshed_str(self):
        dt = self.get_last_refreshed()
        return "never" if not dt else dt.strftime("%Y-%m-%d")

    def can_refresh_today(self):
        dt = self.get_last_refreshed()
        return dt is None or dt.date() != datetime.now().date()

    # ----------------------------
    # API
    # ----------------------------

    def fetch(self):
        headers = {
            "User-Agent": self.user_agent
        }

        r = requests.get(self.api_url, params=self.params, headers=headers)
        r.raise_for_status()
        return r.json()

    # ----------------------------
    # PARSER
    # ----------------------------

    def extract_hex_color(self, soup, name: str):
        selector = f".mutation-{name.lower()}"

        for style in soup.find_all("style"):
            if not style.string:
                continue

            css = style.string
            pattern = rf"{re.escape(selector)}\s*\{{(.*?)\}}"
            match = re.search(pattern, css, re.DOTALL)

            if match:
                block = match.group(1)
                hex_match = re.search(r"#([0-9a-fA-F]{3,6})", block)
                if hex_match:
                    return f"#{hex_match.group(1)}"

        return None

    def extract_mutations(self, raw):
        html = raw["parse"]["text"]["*"]
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", {"id": "mutation-table-1"})
        tbody = table.find("tbody")

        rows = []

        for tr in tbody.find_all("tr")[2:]:
            cell = tr.find("td", class_="appraisable")
            if not cell or cell.get("title", "").lower() != "yes":
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

    # ----------------------------
    # MAIN ENTRY
    # ----------------------------

    def get_data(self, refresh=False):
        if self.clean_file.exists() and not refresh:
            return self.load(self.clean_file)

        if self.raw_file.exists() and not refresh:
            raw = self.load(self.raw_file)
        else:
            raw = self.fetch()

        data = self.extract_mutations(raw)
        self.save(self.clean_file, data)

        return data