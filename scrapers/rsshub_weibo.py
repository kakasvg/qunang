"""
微博博主主页 → RSSHub feed → 提取候选条目 → extractor 提结构化字段 → emit。

⚠️ 当前为 STUB：
  - 博主清单（USERS）需要用户提供真实 UID
  - 现在是空数组，跑起来就是 no-op
  - RSSHub 公共实例不稳，跑通后再考虑自建
"""
from __future__ import annotations
import os
from typing import Iterable

import feedparser

from extractor.claude_extract import extract_observation
from scrapers.base import emit

RSSHUB_BASE = os.getenv("RSSHUB_BASE", "https://rsshub.app").rstrip("/")

# 等用户填入真实微博 uid。见 COWORK.md 的 TODO。
USERS: list[dict] = [
    # {"uid": "1234567890", "name": "@xxx 代购"},
]


def fetch_user(uid: str) -> Iterable[dict]:
    url = f"{RSSHUB_BASE}/weibo/user/{uid}"
    feed = feedparser.parse(url)
    for entry in feed.entries[:20]:
        yield {
            "title": entry.get("title", ""),
            "summary": entry.get("summary", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "author": entry.get("author", ""),
        }


def main():
    if not USERS:
        print("[weibo] no users configured, skip")
        return
    new_total = 0
    for u in USERS:
        for entry in fetch_user(u["uid"]):
            obs = extract_observation(
                text=f"{entry['title']}\n{entry['summary']}",
                platform="weibo",
                url=entry["link"],
                author=u["name"],
            )
            if obs is None:
                continue
            new_total += emit([obs])
    print(f"[weibo] new observations: {new_total}")


if __name__ == "__main__":
    main()
