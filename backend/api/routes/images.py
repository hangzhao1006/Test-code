"""
图片搜索路由
为产品获取图片URL
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import requests
import urllib.parse
import hashlib

router = APIRouter()

class ProductImageResponse(BaseModel):
    product_name: str
    image_url: str
    source: str  # "duckduckgo", "placeholder", "amazon"

def generate_placeholder_image(product_name: str) -> str:
    """
    生成一个基于产品名的占位图片URL
    使用UI Avatars服务生成带产品首字母的图片
    """
    # 提取产品名的前两个字符
    initials = ''.join([word[0] for word in product_name.split()[:2]]).upper()
    if not initials:
        initials = "SK"

    # 生成一个基于产品名的颜色（确保一致性）
    hash_obj = hashlib.md5(product_name.encode())
    hash_hex = hash_obj.hexdigest()
    bg_color = hash_hex[:6]

    # 使用ui-avatars.com生成占位图
    url = f"https://ui-avatars.com/api/?name={urllib.parse.quote(initials)}&size=200&background={bg_color}&color=fff&bold=true"
    return url

def search_product_image_duckduckgo(product_name: str) -> Optional[str]:
    """
    使用DuckDuckGo搜索产品图片

    Parameters:
    - product_name: 产品名称

    Returns:
    - 图片URL或None
    """
    try:
        # DuckDuckGo图片搜索API（非官方，但免费）
        search_query = f"{product_name} skincare product"
        url = "https://duckduckgo.com/"

        # 第一步：获取vqd token
        params = {"q": search_query}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        response = requests.get(url, params=params, headers=headers, timeout=5)

        # 从响应中提取vqd
        vqd_search = 'vqd="'
        vqd_start = response.text.find(vqd_search)
        if vqd_start == -1:
            return None

        vqd_start += len(vqd_search)
        vqd_end = response.text.find('"', vqd_start)
        vqd = response.text[vqd_start:vqd_end]

        # 第二步：使用vqd获取图片
        image_url = "https://duckduckgo.com/i.js"
        params = {
            "l": "us-en",
            "o": "json",
            "q": search_query,
            "vqd": vqd,
            "f": ",,,",
            "p": "1"
        }

        response = requests.get(image_url, params=params, headers=headers, timeout=5)
        data = response.json()

        # 提取第一张图片
        if data.get("results") and len(data["results"]) > 0:
            return data["results"][0].get("image")

        return None

    except Exception as e:
        print(f"DuckDuckGo image search error: {e}")
        return None

def search_product_image_serpapi(product_name: str, api_key: Optional[str] = None) -> Optional[str]:
    """
    使用SerpAPI搜索Google图片（需要API key，但有免费额度）

    Parameters:
    - product_name: 产品名称
    - api_key: SerpAPI key（可选）

    Returns:
    - 图片URL或None
    """
    if not api_key:
        return None

    try:
        search_query = f"{product_name} skincare"
        url = "https://serpapi.com/search.json"
        params = {
            "q": search_query,
            "tbm": "isch",  # 图片搜索
            "api_key": api_key,
            "num": 1
        }

        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if data.get("images_results") and len(data["images_results"]) > 0:
            return data["images_results"][0].get("original")

        return None

    except Exception as e:
        print(f"SerpAPI image search error: {e}")
        return None

@router.get("/product-image", response_model=ProductImageResponse)
async def get_product_image(
    product_name: str = Query(..., description="产品名称"),
    use_placeholder: bool = Query(False, description="强制使用占位图")
):
    """
    获取产品图片URL

    尝试顺序：
    1. DuckDuckGo图片搜索
    2. 占位图片

    Parameters:
    - product_name: 产品名称
    - use_placeholder: 是否强制使用占位图

    Returns:
    - 产品图片信息
    """
    try:
        if use_placeholder:
            # 直接返回占位图
            placeholder_url = generate_placeholder_image(product_name)
            return ProductImageResponse(
                product_name=product_name,
                image_url=placeholder_url,
                source="placeholder"
            )

        # 尝试DuckDuckGo搜索
        image_url = search_product_image_duckduckgo(product_name)

        if image_url:
            return ProductImageResponse(
                product_name=product_name,
                image_url=image_url,
                source="duckduckgo"
            )

        # 降级到占位图
        placeholder_url = generate_placeholder_image(product_name)
        return ProductImageResponse(
            product_name=product_name,
            image_url=placeholder_url,
            source="placeholder"
        )

    except Exception as e:
        # 错误时返回占位图
        placeholder_url = generate_placeholder_image(product_name)
        return ProductImageResponse(
            product_name=product_name,
            image_url=placeholder_url,
            source="placeholder"
        )

@router.get("/batch-product-images")
async def get_batch_product_images(
    product_names: str = Query(..., description="产品名称列表（逗号分隔）"),
    use_placeholder: bool = Query(False, description="强制使用占位图")
):
    """
    批量获取产品图片URL

    Parameters:
    - product_names: 产品名称列表，用逗号分隔
    - use_placeholder: 是否强制使用占位图

    Returns:
    - 产品图片信息列表
    """
    try:
        names = [name.strip() for name in product_names.split(',')]
        results = []

        for name in names:
            if not name:
                continue

            if use_placeholder:
                placeholder_url = generate_placeholder_image(name)
                results.append({
                    "product_name": name,
                    "image_url": placeholder_url,
                    "source": "placeholder"
                })
            else:
                # 尝试搜索
                image_url = search_product_image_duckduckgo(name)

                if image_url:
                    results.append({
                        "product_name": name,
                        "image_url": image_url,
                        "source": "duckduckgo"
                    })
                else:
                    # 降级到占位图
                    placeholder_url = generate_placeholder_image(name)
                    results.append({
                        "product_name": name,
                        "image_url": placeholder_url,
                        "source": "placeholder"
                    })

        return {
            "total": len(results),
            "images": results
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch image search error: {str(e)}"
        )
