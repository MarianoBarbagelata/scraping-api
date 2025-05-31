import requests
from bs4 import BeautifulSoup
import json
import subprocess

values = dict()

def scrape_url(url, values):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"Error al acceder a {url}: {res.status_code}")
        return
    soup = BeautifulSoup(res.text, "html.parser")
    script_tag = soup.find("script", id="__NEXT_DATA__")
    if script_tag:
        data = json.loads(script_tag.string)
        for instrument in data['props']['pageProps']['instruments']:
            ticker = instrument['ticker'] + '.BA'
            values[ticker] = instrument['lastPrice']

def main():
    urls = [
        "https://www.portfoliopersonal.com/Cotizaciones/Cedears",
        "https://www.portfoliopersonal.com/Cotizaciones/Acciones"
    ]
    for url in urls:
        scrape_url(url, values)

    if not values:
        print("No se encontraron valores para los tickers indicados.")
        return

    with open("prices.json", "w", encoding="utf-8") as f:
        json.dump(values, f, indent=2, ensure_ascii=False)
    print("Archivo prices.json actualizado.")

    try:
        subprocess.run(["git", "add", "prices.json"], check=True)
        subprocess.run(["git", "commit", "-m", "Actualizo prices.json con nuevos valores"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Cambios subidos a GitHub correctamente.")
    except subprocess.CalledProcessError as e:
        print("Error al hacer git commit/push:", e)

if __name__ == "__main__":
    main()