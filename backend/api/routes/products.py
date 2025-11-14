"""
产品推荐路由
处理护肤品推荐和产品查询
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import json

router = APIRouter()

# 请求模型
class RecommendationRequest(BaseModel):
    analysis_id: Optional[str] = None
    skin_type: str
    concerns: List[str] = []
    budget: Optional[str] = "medium"  # low, medium, high
    preferences: List[str] = []  # organic, fragrance-free, vegan, etc.

# 响应模型
class Product(BaseModel):
    product_id: str
    name: str
    brand: str
    category: str
    subcategory: Optional[str] = None
    price: float
    currency: str = "USD"
    rating: float
    review_count: int
    ingredients: dict
    tags: List[str]
    description: str
    image_url: str
    why_recommended: str
    match_score: float

# 模拟产品数据（实际应该从数据库或文件加载）
MOCK_PRODUCTS = [
    {
        "product_id": "prod_001",
        "name": "Hydrating Facial Cleanser",
        "brand": "CeraVe",
        "category": "cleanser",
        "subcategory": "gel",
        "price": 14.99,
        "currency": "USD",
        "rating": 4.7,
        "review_count": 15420,
        "skin_types": ["dry", "normal", "combination"],
        "concerns": ["hydration", "sensitive"],
        "ingredients": {
            "active": ["ceramides", "hyaluronic acid"],
            "full_list": "Water, Glycerin, Ceramides, Hyaluronic Acid..."
        },
        "tags": ["fragrance-free", "non-comedogenic", "dermatologist-tested"],
        "description": "温和的保湿洁面乳，含有神经酰胺和透明质酸",
        "image_url": "/products/cerave-cleanser.jpg",
    },
    {
        "product_id": "prod_002",
        "name": "Oil-Free Acne Wash",
        "brand": "Neutrogena",
        "category": "cleanser",
        "subcategory": "foam",
        "price": 7.99,
        "currency": "USD",
        "rating": 4.4,
        "review_count": 8920,
        "skin_types": ["oily", "combination"],
        "concerns": ["acne", "oily_skin"],
        "ingredients": {
            "active": ["salicylic acid"],
            "full_list": "Salicylic Acid, Water, Glycerin..."
        },
        "tags": ["oil-free", "non-comedogenic"],
        "description": "控油祛痘洁面乳，含有水杨酸成分",
        "image_url": "/products/neutrogena-acne.jpg",
    },
    {
        "product_id": "prod_003",
        "name": "Ultra Facial Cream",
        "brand": "Kiehl's",
        "category": "moisturizer",
        "subcategory": "cream",
        "price": 32.00,
        "currency": "USD",
        "rating": 4.6,
        "review_count": 12340,
        "skin_types": ["dry", "normal", "combination"],
        "concerns": ["hydration", "dryness"],
        "ingredients": {
            "active": ["squalane", "glacial glycoprotein"],
            "full_list": "Squalane, Glacial Glycoprotein, Vitamin E..."
        },
        "tags": ["lightweight", "24h-hydration"],
        "description": "轻盈保湿面霜，提供24小时长效保湿",
        "image_url": "/products/kiehls-cream.jpg",
    }
]

@router.post("/recommend", response_model=dict)
async def get_recommendations(request: RecommendationRequest):
    """
    根据皮肤分析结果推荐产品

    Parameters:
    - analysis_id: 分析ID（可选）
    - skin_type: 肤质类型
    - concerns: 肌肤问题列表
    - budget: 预算范围
    - preferences: 偏好标签

    Returns:
    - recommendations: 推荐产品列表
    """
    try:
        # 根据肤质和问题筛选产品
        filtered_products = []

        for product in MOCK_PRODUCTS:
            # 检查肤质匹配
            if request.skin_type not in product.get("skin_types", []):
                continue

            # 检查问题匹配
            concern_match = False
            if request.concerns:
                for concern in request.concerns:
                    if concern in product.get("concerns", []):
                        concern_match = True
                        break
            else:
                concern_match = True  # 如果没有特定问题，所有产品都匹配

            if not concern_match:
                continue

            # 检查偏好标签
            if request.preferences:
                preference_match = any(
                    pref in product.get("tags", [])
                    for pref in request.preferences
                )
                if not preference_match:
                    continue

            # 检查预算
            if request.budget:
                if request.budget == "low" and product["price"] > 20:
                    continue
                elif request.budget == "medium" and (product["price"] < 10 or product["price"] > 50):
                    continue
                elif request.budget == "high" and product["price"] < 30:
                    continue

            # 计算匹配分数
            match_score = calculate_match_score(product, request)

            # 生成推荐理由
            why_recommended = generate_recommendation_reason(product, request)

            # 添加到结果
            filtered_products.append({
                **product,
                "match_score": match_score,
                "why_recommended": why_recommended
            })

        # 按匹配分数排序
        filtered_products.sort(key=lambda x: x["match_score"], reverse=True)

        return {
            "total": len(filtered_products),
            "recommendations": filtered_products[:10]  # 返回前10个
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        )

@router.get("/{product_id}", response_model=dict)
async def get_product_details(product_id: str):
    """
    获取单个产品的详细信息

    Parameters:
    - product_id: 产品ID

    Returns:
    - 产品详细信息
    """
    # 查找产品
    product = next(
        (p for p in MOCK_PRODUCTS if p["product_id"] == product_id),
        None
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

@router.get("/", response_model=dict)
async def search_products(
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    skin_type: Optional[str] = None,
    limit: int = Query(default=20, le=100)
):
    """
    搜索和筛选产品

    Parameters:
    - category: 产品类别
    - brand: 品牌
    - min_price, max_price: 价格范围
    - skin_type: 肤质类型
    - limit: 返回数量限制

    Returns:
    - products: 产品列表
    """
    filtered = MOCK_PRODUCTS.copy()

    if category:
        filtered = [p for p in filtered if p["category"] == category]

    if brand:
        filtered = [p for p in filtered if p["brand"].lower() == brand.lower()]

    if min_price is not None:
        filtered = [p for p in filtered if p["price"] >= min_price]

    if max_price is not None:
        filtered = [p for p in filtered if p["price"] <= max_price]

    if skin_type:
        filtered = [p for p in filtered if skin_type in p.get("skin_types", [])]

    return {
        "total": len(filtered),
        "products": filtered[:limit]
    }

def calculate_match_score(product: dict, request: RecommendationRequest) -> float:
    """计算产品与需求的匹配分数（0-1）"""
    score = 0.0
    total_factors = 0

    # 肤质匹配（权重 30%）
    if request.skin_type in product.get("skin_types", []):
        score += 0.3
    total_factors += 0.3

    # 问题匹配（权重 40%）
    if request.concerns:
        concern_matches = sum(
            1 for c in request.concerns
            if c in product.get("concerns", [])
        )
        concern_score = (concern_matches / len(request.concerns)) * 0.4
        score += concern_score
    total_factors += 0.4

    # 偏好匹配（权重 20%）
    if request.preferences:
        pref_matches = sum(
            1 for p in request.preferences
            if p in product.get("tags", [])
        )
        pref_score = (pref_matches / len(request.preferences)) * 0.2
        score += pref_score
    total_factors += 0.2

    # 评分（权重 10%）
    rating_score = (product.get("rating", 0) / 5.0) * 0.1
    score += rating_score
    total_factors += 0.1

    return round(score, 2)

def generate_recommendation_reason(product: dict, request: RecommendationRequest) -> str:
    """生成推荐理由"""
    reasons = []

    # 肤质匹配
    skin_type_names = {
        "oily": "油性",
        "dry": "干性",
        "combination": "混合性",
        "normal": "中性"
    }
    reasons.append(f"适合{skin_type_names.get(request.skin_type, request.skin_type)}肌肤")

    # 主要成分
    if product.get("ingredients", {}).get("active"):
        active = product["ingredients"]["active"]
        if active:
            reasons.append(f"含有{active[0]}等有效成分")

    # 特殊标签
    tag_descriptions = {
        "fragrance-free": "无香料配方",
        "non-comedogenic": "不堵塞毛孔",
        "dermatologist-tested": "经皮肤科医生测试",
        "oil-free": "无油配方"
    }

    for tag in product.get("tags", []):
        if tag in tag_descriptions:
            reasons.append(tag_descriptions[tag])
            break

    return "，".join(reasons) + "。"
