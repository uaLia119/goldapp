from flask import Flask, render_template, jsonify
import requests
import threading
import time

app = Flask(__name__)
data = {"gold": {}, "silver": {}, "gold_oz": 0.0, "silver_oz": 0.0}

# Umrechnungsfaktor von Troy Oz in Gramm
TROY_OZ_IN_GRAMM = 31.1034768

# Mapping für Gold-Legierungen
GOLD_LEGIERUNGEN = {
    "999er": 999,
    "986er": 986,
    "916er": 916,
    "900er": 900,
    "750er": 750,
    "585er": 585,
    "333er": 333
}

# Mapping für Silber-Legierungen
SILBER_LEGIERUNGEN = {
    "999er": 999,
    "925er": 925,
    "900er": 900,
    "835er": 835,
    "800er": 800,
    "750er": 750,
    "625er": 625
}

def fetch_prices():
    while True:
        try:
            # --- GOLD ---
            res_gold = requests.get("https://forex-data-feed.swissquote.com/public-quotes/bboquotes/instrument/XAU/EUR")
            if res_gold.status_code == 200:
                json_gold = res_gold.json()
                print("GOLD API ANTWORT:", json_gold)

                for entry in json_gold:
                    prices = entry.get("spreadProfilePrices")
                    if isinstance(prices, list):
                        for profile in prices:
                            if "bid" in profile:
                                preis_oz_gold = profile["bid"]
                                preis_gramm_gold = preis_oz_gold / TROY_OZ_IN_GRAMM

                                data["gold"] = {
                                    legierung: round(preis_gramm_gold * (wert / 999), 2)
                                    for legierung, wert in GOLD_LEGIERUNGEN.items()
                                }

                                data["gold_oz"] = round(preis_oz_gold, 2)
                                break
                        if "gold" in data:
                            break

            # --- SILBER ---
            res_silver = requests.get("https://forex-data-feed.swissquote.com/public-quotes/bboquotes/instrument/XAG/EUR")
            if res_silver.status_code == 200:
                json_silver = res_silver.json()
                print("SILBER API ANTWORT:", json_silver)

                for entry in json_silver:
                    prices = entry.get("spreadProfilePrices")
                    if isinstance(prices, list):
                        for profile in prices:
                            if "bid" in profile:
                                preis_oz_silver = profile["bid"]
                                preis_gramm_silver = preis_oz_silver / TROY_OZ_IN_GRAMM

                                data["silver"] = {
                                    legierung: round(preis_gramm_silver * (wert / 999), 2)
                                    for legierung, wert in SILBER_LEGIERUNGEN.items()
                                }

                                data["silver_oz"] = round(preis_oz_silver, 2)
                                break
                        if "silver" in data:
                            break

        except Exception as e:
            print("Fehler beim Abrufen der Preise:", e)

        time.sleep(1)  # sekündlich

@app.route("/")
def index():
    return render_template("index.html", data=data)

@app.route("/api/prices")
def api_prices():
    return jsonify(data)

if __name__ == "__main__":
    threading.Thread(target=fetch_prices, daemon=True).start()
    app.run(debug=True, port=5050)
