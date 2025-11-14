"""
重新加载数据到ChromaDB，包含购买链接
"""
import os
import sys
import json
import chromadb
import glob

# 添加backend目录到路径
sys.path.insert(0, os.path.dirname(__file__))
from cli import load_jsonl

# ChromaDB配置
CHROMADB_HOST = os.getenv("CHROMADB_HOST", "chromadb")
CHROMADB_PORT = int(os.getenv("CHROMADB_PORT", "8000"))

# 数据路径
STRUCTURED_DATA = "/app/backend/input-datasets/structured/ewg_face_label_structured.jsonl"
EMBEDDINGS_FOLDER = "/app/backend/input-datasets/outputs"

def load_structured_data():
    """加载原始EWG数据，构建产品名到元数据的映射"""
    print(f"Loading structured data from {STRUCTURED_DATA}...")

    product_map = {}

    with open(STRUCTURED_DATA, 'r') as f:
        for line in f:
            item = json.loads(line)
            title = item.get('title', '')

            # 提取购买链接
            buy_urls = item.get('buy_button_urls', [])
            amazon_url = buy_urls[0] if buy_urls else None

            # 提取EWG URL
            ewg_url = item.get('url', '')

            # 存储元数据
            product_map[title] = {
                'title': title,
                'brand': item.get('brand', ''),
                'category': item.get('category', ''),
                'amazon_url': amazon_url,
                'ewg_url': ewg_url,
                'has_website_button': item.get('has_website_button', False)
            }

    print(f"Loaded {len(product_map)} products with metadata")
    return product_map

def extract_product_name_from_filename(filename):
    """
    从embedding文件名提取产品名
    例如: embeddings-char-split-0000-Cliganic 100% Pure & Natural Neem Oil.jsonl
    返回: Cliganic 100% Pure & Natural Neem Oil
    """
    base = os.path.basename(filename)
    # 移除 "embeddings-char-split-" 前缀和 ".jsonl" 后缀
    if base.startswith('embeddings-char-split-'):
        base = base[len('embeddings-char-split-'):]
    if base.endswith('.jsonl'):
        base = base[:-6]

    # 移除文件名开头的数字部分（例如 "0000-"）
    parts = base.split('-', 1)
    if len(parts) == 2 and parts[0].isdigit():
        return parts[1]

    return base

def reload_chromadb_with_links():
    """重新加载ChromaDB，包含购买链接"""
    print("Starting ChromaDB reload with purchase links...")

    # 加载原始产品数据
    product_map = load_structured_data()

    # 连接ChromaDB
    print(f"Connecting to ChromaDB at {CHROMADB_HOST}:{CHROMADB_PORT}...")
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)

    # 删除旧集合（如果存在）
    try:
        client.delete_collection(name="char-split-collection")
        print("Deleted existing collection")
    except:
        print("No existing collection to delete")

    # 创建新集合
    collection = client.create_collection(
        name="char-split-collection",
        metadata={"hnsw:space": "cosine"}
    )
    print("Created new collection: char-split-collection")

    # 加载所有embedding文件
    embedding_pattern = os.path.join(EMBEDDINGS_FOLDER, "embeddings-char-split-*.jsonl")
    embedding_files = sorted(glob.glob(embedding_pattern))

    print(f"Found {len(embedding_files)} embedding files")

    total_loaded = 0
    products_with_links = 0
    products_without_links = 0

    for idx, emb_file in enumerate(embedding_files):
        # 从文件名提取产品名
        product_name = extract_product_name_from_filename(emb_file)

        # 加载embedding数据
        data = list(load_jsonl(emb_file))

        # 查找对应的产品元数据
        product_meta = product_map.get(product_name, {})

        if product_meta.get('amazon_url'):
            products_with_links += 1
        else:
            products_without_links += 1

        # 准备批量插入数据
        documents = []
        metadatas = []
        embeddings = []
        ids = []

        for i, item in enumerate(data):
            doc_id = f"{idx:04d}-{i:04d}"

            documents.append(item.get("chunk", ""))

            # 构建完整的metadata（只添加非空值）
            metadata = {
                "book": item.get("book", "Unknown")
            }

            # 添加产品名（如果有）
            if product_name:
                metadata["product_name"] = product_name

            # 添加品牌（如果有）
            if product_meta.get('brand'):
                metadata["brand"] = product_meta.get('brand')

            # 添加分类（如果有）
            if product_meta.get('category'):
                metadata["category"] = product_meta.get('category')

            # 添加Amazon URL（如果有）
            if product_meta.get('amazon_url'):
                metadata["amazon_url"] = product_meta.get('amazon_url')

            # 添加EWG URL（如果有）
            if product_meta.get('ewg_url'):
                metadata["ewg_url"] = product_meta.get('ewg_url')

            metadatas.append(metadata)

            embeddings.append(item.get("embedding", []))
            ids.append(doc_id)

        # 批量插入
        if documents:
            collection.add(
                documents=documents,
                metadatas=metadatas,
                embeddings=embeddings,
                ids=ids
            )
            total_loaded += len(documents)

        if (idx + 1) % 100 == 0:
            print(f"Progress: {idx + 1}/{len(embedding_files)} files ({total_loaded} chunks)")

    print(f"\n=== Reload Complete ===")
    print(f"Total chunks loaded: {total_loaded}")
    print(f"Products with Amazon links: {products_with_links}")
    print(f"Products without links: {products_without_links}")
    print(f"Collection count: {collection.count()}")

if __name__ == "__main__":
    reload_chromadb_with_links()
