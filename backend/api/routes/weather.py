"""
天气API路由 - 使用OpenWeatherMap API代理以避免CORS问题
"""
from fastapi import APIRouter, HTTPException
import httpx
from typing import Optional
import os

router = APIRouter()

# OpenWeatherMap API配置
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "bd5e378503939ddaee76f12ad7a97608")
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@router.get("/weather")
async def get_weather(lat: Optional[float] = None, lon: Optional[float] = None, lang: str = "en"):
    """
    获取天气信息
    如果提供了经纬度，使用经纬度查询；否则使用默认城市(Boston)

    参数:
    - lat: 纬度
    - lon: 经度
    - lang: 语言 (zh_cn 或 en)
    """
    try:
        # 构建API URL参数
        params = {
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",  # 使用摄氏度
            "lang": lang
        }

        # 根据经纬度或城市名查询
        if lat is not None and lon is not None:
            params["lat"] = lat
            params["lon"] = lon
        else:
            # 默认使用Boston
            params["q"] = "Boston"

        # 使用httpx发送请求（支持异步）
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(OPENWEATHER_BASE_URL, params=params)
            response.raise_for_status()

            data = response.json()

            # 转换为统一格式，保持与wttr.in兼容
            formatted_data = {
                "current_condition": [{
                    "temp_C": str(round(data["main"]["temp"])),
                    "weatherDesc": [{"value": data["weather"][0]["description"]}],
                    "humidity": str(data["main"]["humidity"]),
                    "FeelsLikeC": str(round(data["main"]["feels_like"]))
                }],
                "nearest_area": [{
                    "areaName": [{"value": data["name"]}],
                    "region": [{"value": data["sys"]["country"]}]
                }]
            }

            return formatted_data

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Weather API error: {e.response.text}"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to connect to weather service: {str(e)}"
        )
    except KeyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected API response format: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
