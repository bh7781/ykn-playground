import requests
import pandas as pd
from typing import List, Dict, Any

API_KEY = "your_api_key"
API_URL = "https://api.apilayer.com/exchangerates_data/convert?to={}&from=USD&amount=1"

CURRENCIES = [
    "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD",
    "MXN", "SGD", "HKD", "NOK", "KRW", "TRY", "INR", "RUB", "BRL", "ZAR",
    "DKK", "PLN", "TWD", "THB", "IDR", "HUF", "CZK", "ILS", "CLP", "PHP",
    "AED", "COP", "SAR", "MYR", "RON", "BGN", "HRK", "UAH", "MAD", "KZT",
    "BHD", "OMR", "RSD", "ISK", "LKR", "PKR", "KES", "GHS", "BDT", "UGX",
    "TND", "DZD", "QAR", "JOD", "PEN", "KWD", "BWP", "IRR", "VND", "NGN",
    "ARS", "GEL", "XAF", "XOF", "CRC", "TMT", "TJS", "UZS", "AZN", "AFN",
    "BYN", "VEF", "SCR", "IQD", "SYP", "YER", "SLL", "SDG", "XDR", "MZN",
    "FJD", "ETB", "BIF", "MWK", "GMD", "MRO", "ERN", "SZL", "CVE", "MUR",
    "XCD", "HTG", "KYD", "AWG", "BMD", "LRD", "NAD", "ZMW", "XPF", "TTD"
]



def fetch_currency_conversion_rates(api_key: str, api_url: str, currencies: List[str]) -> List[Dict[str, Any]]:
    headers = {"apikey": api_key}
    data = []

    for currency in currencies:
        print(f'---------------------{currency}---------------------')
        response = requests.get(api_url.format(currency), headers=headers)
        response_data = response.json()
        print(response_data)
        if response_data["success"]:
            data.append({
                "date": response_data["date"],
                "from_currency": response_data["query"]["from"],
                "to_currency": currency,
                "rate": response_data["info"]["rate"],
                "timestamp": response_data["info"]["timestamp"]
            })

    return data


def main():
    conversion_data = fetch_currency_conversion_rates(API_KEY, API_URL, CURRENCIES)
    df = pd.DataFrame(conversion_data)
    df.to_csv(r'exchange_rates.csv', index=False)


if __name__ == "__main__":
    main()
