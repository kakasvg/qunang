"""
LV 中国官网 + 日本官网 → 关注款页面价格基线。
LV 是少数几个公开标价的奢侈品，比 UGC 数据靠谱得多。

⚠️ STUB：实际页面 selector 和反爬策略未实现。
跑通前需要：
  1. 用 Playwright 看一眼实际 DOM
  2. 处理 LV 的地理重定向（cn.louisvuitton.com / jp.louisvuitton.com）
  3. 解析 JSON-LD（LV 页面里有 schema.org Product）
"""
from __future__ import annotations

PRODUCTS_TO_TRACK = [
    # 等用户给具体款号 + URL
    # {"product_id": "lv_neverfull_mm_damier_ebene", "cn_url": "...", "jp_url": "..."},
]


def main():
    if not PRODUCTS_TO_TRACK:
        print("[lv] no products configured, skip")
        return
    print("[lv] STUB — implement DOM scraping + JSON-LD parsing")


if __name__ == "__main__":
    main()
