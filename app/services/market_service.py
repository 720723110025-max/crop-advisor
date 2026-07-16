import requests

class MarketService:

    def get_prices(self):

        try:
            url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

            params = {
                "api-key": "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b",
                "format": "json",
                "limit": 20
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                return response.json().get("records", [])

        except Exception:
            pass

        return []