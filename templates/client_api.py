import requests
import json
from templates.client_credentials import API_KEY, PASSWORD, STORE_NAME, API_VERSION
import aiohttp


def search(query: str) -> list:
    """Call search api to return products"""

    response = requests.get(
        url=f"https://{API_KEY}:{PASSWORD}@{STORE_NAME}"
            f".myshopify.com/search/suggest.json?q={query}&resources[type]=product"
    )

    return response.json()['resources']['results']['products']

# TODO: Make below code runnable.
# async def fetch_category_image(smart_collection_ids: list) -> list:
#     async with aiohttp.ClientSession() as session:
#         images = []
#         for category in smart_collection_ids:
#             async with session.get(
#                     f"https://{API_KEY}:{PASSWORD}@{STORE_NAME}.myshopify.com/admin/api/{API_VERSION}/collections/"
#                     f"{category}/products.json"
#             ) as response:
#                 result = await response.json()
#                 y = await parse(result)
#                 images.append(y)
#         return images
#
#
# async def parse(response: dict) -> str:
#     return response["products"][0]["image"]["src"]


def fetch_category_image(smart_collection_ids: list) -> list:
    """Takes smart collection ids as input and return image
    of the first product of the smart collection"""

    images = list()
    for collection_id in smart_collection_ids:
        response = requests.get(
            f"https://{API_KEY}:{PASSWORD}@{STORE_NAME}.myshopify.com/admin/api/{API_VERSION}/collections/"
            f"{collection_id}/products.json"
        )
        result = response.json()["products"][0]["image"]["src"]
        images.append(result)

    return images


if __name__ == '__main__':
    print(search("Body lotion"))
