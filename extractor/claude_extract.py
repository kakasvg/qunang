"""
把一段中/日/英自然语言（微博/X/YouTube 简介）→ 结构化 observation。

走 Claude Haiku（便宜 + 快）+ 强约束的 system prompt + 启用 prompt cache。
返回 None 表示这条文本不是包包相关、可丢弃。

成本控制：
  - 用 Haiku 4.5 / 4.6（按主 CLAUDE.md 偏好用最新）
  - system prompt 标 cache_control
  - 单次输出限制 tokens 200
"""
from __future__ import annotations
import json
import os
from typing import Optional

try:
    import anthropic
except ImportError:
    anthropic = None  # 让 stub 模式下也能 import

MODEL = os.getenv("EXTRACTOR_MODEL", "claude-haiku-4-5-20251001")

SYSTEM = """\
You extract structured purchase observations about luxury bags from social media posts.
Input: one short post (Chinese / Japanese / English).
Output: JSON with fields:
  product_match: short slug like "chanel_25_small_black" or null if no specific bag
  price: number or null
  currency: "JPY" | "CNY" | "USD" | null
  location: store / city in source language, or null
  stock: "in_stock" | "out_of_stock" | "limited" | "restocked" | null
  is_relevant: bool — whether this post is about a luxury bag price/stock at all
Return ONLY the JSON object, no preamble.
"""


def extract_observation(
    *, text: str, platform: str, url: str, author: str
) -> Optional[dict]:
    if not anthropic or not os.getenv("ANTHROPIC_API_KEY"):
        # Stub mode: 把原文塞进去，标低置信度，让人工/聚合层过滤
        return {
            "product_id": None,
            "raw_text": text[:500],
            "source": {"platform": platform, "url": url, "author": author},
            "ai_confidence": 0.0,
            "_stub": True,
        }

    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=MODEL,
        max_tokens=200,
        system=[{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": text[:1500]}],
    )
    raw = resp.content[0].text.strip()
    try:
        d = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not d.get("is_relevant"):
        return None

    return {
        "product_id": d.get("product_match"),
        "price": d.get("price"),
        "currency": d.get("currency"),
        "location": d.get("location"),
        "stock": d.get("stock"),
        "raw_text": text[:500],
        "source": {"platform": platform, "url": url, "author": author},
        "ai_confidence": 0.9,  # 后续可以让模型自报置信度
    }
