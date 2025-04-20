import requests
from my_client import MyClient


def fetch_gini_index(country_searched: str, year_searched: str) -> float:
    api_url = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectarse a la API: {e}")
        return -1

    for item in data[1]:
        if (item.get('country', {}).get('value') == country_searched
                and item.get('date') == year_searched):
            return item.get('value') or -1

    return -1


# Función principal
def main():
    while True:
        print("\n")
        country = input("Ingrese el país: ").strip()
        year = input("Ingrese el año (ej: 2020): ").strip()

        old_gini = fetch_gini_index(country, year)
        if old_gini == -1:
            print(f"No se encontró el índice GINI para {country} en {year}.")
            continue

        # Connect to the 32-bit library using msl-loadlib
        c_program = MyClient()

        # Print GINI values
        print("Gini viejo: ", old_gini)
        print("Gini actualizado: ", c_program._gini(old_gini))


if __name__ == "__main__":
    main()