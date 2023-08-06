import asyncio
import time
import httpx


POLL_INTERVAL = 5
ENVIRONMENTS = {
    'local': 'LOCAL',
    'cloud': 'DC',
    'unblockable': 'RESID',
}


# Configuration variables
api_key = None
api_base = "https://parsagon.io/api"


def _request_to_exception(response):
    if response.status_code == 500:
        raise Exception('A server error occurred. Please notify Parsagon.')
    if response.status_code in (502, 503, 504):
        raise Exception('Lost connection to server.')
    errors = response.json()
    if 'non_field_errors' in errors:
        raise Exception(errors['non_field_errors'])
    else:
        raise Exception(errors)


def _extract(api_endpoint, data):
    headers = {"Authorization": f"Token {api_key}"}
    r = httpx.post(api_endpoint, headers=headers, json=data)
    if not r.is_success:
        _request_to_exception(r)
    poll_key = r.json()["poll_key"]
    while True:
        time.sleep(POLL_INTERVAL)
        r = httpx.get(f"{api_base}/extract/poll/?poll_key={poll_key}", headers=headers)
        if not r.is_success:
            _request_to_exception(r)
        data = r.json()
        if data["done"]:
            return data


async def _aextract(api_endpoint, data):
    headers = {"Authorization": f"Token {api_key}"}
    async with httpx.AsyncClient() as client:
        r = await client.post(api_endpoint, headers=headers, json=data)
        if not r.is_success:
            _request_to_exception(r)
        poll_key = r.json()["poll_key"]
        while True:
            asyncio.sleep(POLL_INTERVAL)
            r = await client.get(f"{api_base}/extract/poll/?poll_key={poll_key}", headers=headers)
            if not r.is_success:
                _request_to_exception(r)
            data = r.json()
            if data["done"]:
                return data


def get_product(url):
    return _extract(f"{api_base}/extract/product/", {"url": url})


async def aget_product(url):
    return await _aextract(f"{api_base}/extract/product/", {"url": url})


def get_product_list(url):
    return _extract(f"{api_base}/extract/product-list/", {"url": url})


async def aget_product_list(url):
    return await _aextract(f"{api_base}/extract/product-list/", {"url": url})
