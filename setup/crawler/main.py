import requests
from typing import Union, Any
import json
from tqdm import tqdm

from model import ProductInfo, ProductDescription, ProductStatus


class PCHomeApi:
    """PCHome 24h API"""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36",  # noqa: E501
        }
        self.callback = "json+"
        self.base_url = "https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2"

        self.product_list_url = self.base_url + "/store/{}/prod"
        self.product_list_fields = ["Id"]

        self.product_url = f"{self.base_url}/prod"
        self.product_info_url = self.product_url + "/{}"
        self.product_info_fields = ["Id", "Name", "Pic", "Price"]

        self.product_desc_url = f"{self.product_info_url}/desc"
        self.product_desc_fields = ["Slogan"]

        self.product_status_url = self.product_url + "/button"
        self.product_status_fields = ["Qty", "SaleStatus"]

    def _get_request(self, url: str, to_json: bool = True) -> Union[str, None]:
        """送出 GET 請求

        Args:
            url (str): 請求網址
        """
        response = requests.get(url)
        if not response.ok:
            print(f"請求失敗: {url}")
            print(f"失敗訊息: {response.text}")
        else:
            if to_json:
                data = response.json()
            else:
                data = response.text
            return data
        return None

    def _joined_with_comma(self, fields: list[str]):
        return ",".join(fields)

    def get_product_ids(
        self, brand_id: str, offset: int = 0, limit: int = 10
    ) -> list[str]:
        url = (
            self.product_list_url.format(brand_id)
            + f"&offset={offset}"
            + f"&limit={limit}"
            + f"&fields={self._joined_with_comma(self.product_list_fields)}"
            + f"&_callback={self.callback}"
        )
        data = self._get_request(url, to_json=True)

        return list(map(lambda x: x["Id"], data))

    def get_product_info(self, product_id: str) -> dict[str, Any]:
        url = (
            self.product_info_url.format(product_id)
            + f"&fields={self._joined_with_comma(self.product_info_fields)}"
            + f"&_callback={self.callback}"
        )
        data = self._get_request(url, to_json=True)

        return ProductInfo().load(data[product_id])

    def get_product_desc(self, product_id: str):
        url = (
            self.product_desc_url.format(product_id)
            + f"&fields={self._joined_with_comma(self.product_desc_fields)}"
            + f"&_callback={self.callback}"
        )
        data = self._get_request(url, to_json=True)

        # remove postfix -000
        id = product_id[:-4]
        return ProductDescription().load(data[id])

    def get_products_status(self, product_ids: list[str]):
        url = (
            self.product_status_url
            + f"&id={self._joined_with_comma(product_ids)}"
            + f"&fields={self._joined_with_comma(self.product_status_fields)}"
        )
        data = self._get_request(url, to_json=True)

        return ProductStatus(many=True).load(data)


if __name__ == "__main__":
    product_list_offset = 0
    product_list_limit = 100

    brands = {
        "AMD": "DRAD50",
        "ASUS": "DRAD1N",
        "GIGABYTE": "DRAD1K",
        "INNO3D": "DRADGJ",
        "LEADTEK": "DRAD1Q",
        "MSI": "DRAD1R",
        "NVIDIA": "DRADD4",
        "PNY": "DRADJ4",
        "PowerColor": "DRAD1Y",
        "ZOTAC": "DRADD7",
    }

    api = PCHomeApi()

    results = []
    for key, value in tqdm(brands.items(), desc="Loading"):
        product_ids = api.get_product_ids(value)

        products = []
        for id in tqdm(product_ids, desc="Fetching", leave=False):
            product = api.get_product_info(id)
            description = api.get_product_desc(id)
            product.update(description)
            product["brand"] = key

            products.append(product)

        products_status = api.get_products_status(product_ids)
        for index, product in tqdm(
            enumerate(products), desc="Merging", leave=False
        ):  # noqa: E501
            product.update(products_status[index])

        results.extend(products)

    with open("./data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
