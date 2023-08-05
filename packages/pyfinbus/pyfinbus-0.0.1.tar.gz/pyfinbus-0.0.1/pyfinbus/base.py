import requests
import json


def fetch_xueqiu(url, host="stock.xueqiu.com"):
    HEADERS = {'Host': host,
        'Accept': 'application/json',
        'Cookie': 'device_id=84c4cb8ea5c257a794f5a124af973832; s=bu11kgnqv3; '
                  'xq_a_token=51d351b43f9ca116112b30f56fbed181c7acbbf4; '
                  'xqat=51d351b43f9ca116112b30f56fbed181c7acbbf4; '
                  'xq_r_token=d5c015e44d4eb51cf9fee6298d2cace7b94ba8c8; '
                  'xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9'
                  '.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTY4MTI1OTA1MywiY3RtIjoxNjc5NDg3NzU5NjI0LCJjaWQiOiJkOWQwbjRBWnVwIn0.d_C3HZwGFxJcmWTi4uvLhBFWUBeOZLzh7n8pItPcXfM6NMY-it4rE8y1jKXwnSGpRICrh0-O87ayWgBGOEDdf_XwtC34303EuQBOUowS9hQ3yT_K5m5zDBDqJPe4VCilaFjzgFbbD7JD-Lt979yj__q8H2AJlip7sZbpJtzK1KZCcKef4pcQSM-e34C_TzSnX9DTGggG3ODWfYHCmqsPM2oerFumS8D1klLT74Xr1pwrpJ2-042iT53UuwLNHakeGcVUl3X4Xf2Y6OZGXhVNQ74dw4SJy6-8EL5jD6rQ4V8MHDmMb84nTiHz4MzXGvckgUOPNK87mkuUdUwoifAEXA; u=501679487793501; Hm_lvt_1db88642e346389874251b5a1eded6e3=1677137381,1678008203,1678326979,1679487795; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1679542547',
        'User-Agent': 'Xueqiu iPhone 14.12',
        'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
        'Accept-Encoding': 'br, gzip, deflate',
        'Connection': 'keep-alive',
        'X-Device-Model-Name': 'iPhone 13 Pro Max',
        'X-Device-OS': 'iOS 16.3.1',
        'X-Device-ID': '0EA05EE7-67B1-6Y7Y-AC78-F32189CFA347'
    }

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise Exception(response.content)

    return json.loads(response.content)
