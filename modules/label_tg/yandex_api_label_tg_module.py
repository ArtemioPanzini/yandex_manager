import config
import requests
from retry import retry


# Получаем API response в формате PDF
@retry(exceptions=requests.exceptions.RequestException, tries=3, delay=2, backoff=2, max_delay=10)
def get_pdf(campaign_id='', order_id='', api_key=config.yandex_api_token):
    url = f"https://api.partner.market.yandex.ru/campaigns/{campaign_id}/orders/{order_id}/delivery/labels?format="
    headers = {
        "Authorization": api_key,
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.content
