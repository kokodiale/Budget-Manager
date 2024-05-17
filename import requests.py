# import requests

# # Ustawienia API
# api_url = "https://api.nbp.pl/api/exchangerates/tables/A?format=json"

# # Wykonaj żądanie do API
# response = requests.get(api_url)

# # Sprawdź status żądania
# if response.status_code == 200:
#     data = response.json()
#     # Wyciągnij kursy walut
#     if data and len(data) > 0:
#         table = data[0]
#         effective_date = table.get("effectiveDate", "")
#         rates = table.get("rates", [])
#         print(f"Kursy walut z dnia: {effective_date}")
#         for rate in rates:
#             currency = rate.get("currency", "Unknown currency")
#             code = rate.get("code", "Unknown code")
#             mid_rate = rate.get("mid", "Unknown rate")
#             print(f"{currency} ({code}): {mid_rate}")
# else:
#     print(f"Coś poszło nie tak. Status kod: {response.status_code}")


import os

all_files = os.listdir()
xlsx_files = [file for file in all_files if file.endswith('.xlsx')]

if len(xlsx_files) == 0:
    print(len(xlsx_files))
elif len(xlsx_files) == 1:
    print(len(xlsx_files))
else:
    print(len(xlsx_files))

