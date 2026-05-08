"""
Mercari 日本二手 → 关注款的搜索结果 → 卖家信誉 + 上架时间 + 价格。

Mercari 有半官方搜索 API。先做最小实现：单次 GET，按关键词搜，提前 5 条。

⚠️ STUB：搜索关键词来自 products.json 的 mercari_keywords 字段，
当前 products.json 里还没填这字段。
"""
from __future__ import annotations

from scrapers.base import load_products


def main():
    products = load_products()
    targets = [
        (pid, p) for pid, p in products.items() if p.get("mercari_keywords")
    ]
    if not targets:
        print("[mercari] no products with mercari_keywords, skip")
        return
    print(f"[mercari] STUB — would search for {len(targets)} products")


if __name__ == "__main__":
    main()
