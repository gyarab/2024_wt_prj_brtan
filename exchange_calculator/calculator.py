import httpx
import json

def exchange_rate():
    url = "https://www.cnb.cz/en/financial_markets/foreign_exchange_market/exchange_rate_fixing/daily.txt"
    try:
        response = httpx.get(url)
        response.raise_for_status()
        lines = response.text.split('\n')
        for line in lines:
            parts = line.split('|')
            if len(parts) > 1 and parts[0] == 'EUR':
                return float(parts[2].replace(',', '.'))
    except httpx.HTTPError as e:
        print(f"Chyba při načítání dat: {e}")
        return None

def convert_currency(amount, rate, direction):
    if direction == "EUR->CZK":
        return amount * rate
    elif direction == "CZK->EUR":a
        return amount / rate

def main():
    rate = exchange_rate()
    if rate is None:
        print("Nepodařilo se načíst aktuální kurz.")
        return
    
    print(f"Aktuální kurz EUR -> CZK: {rate}")
    while True:
        try:
            amount = float(input("Zadejte částku: "))
            if amount < 0:
                print("Částka musí být kladná.")
                continue
            direction = input("Zvolte směr převodu (EUR->CZK nebo CZK->EUR): ").strip()
            if direction not in ["EUR->CZK", "CZK->EUR"]:
                print("Neplatný směr převodu.")
                continue
            result = convert_currency(amount, rate, direction)
            print(f"Výsledek: {result:.2f} {direction.split('->')[-1]}")
        except ValueError:
            print("Neplatný vstup, zadejte číslo.")
        
        again = input("Chcete provést další převod? (ano/ne): ").strip().lower()
        if again != "ano":
            break

if __name__ == "__main__":
    main()
