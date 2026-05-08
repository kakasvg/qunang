"""
Observation 写入与去重的统一入口。
所有 scraper 把抓到的原始记录交给 emit()，由它写到 data/observations.jsonl。

一条 observation 必须含：
  product_id   主表 key（chanel_22bag_medium_black_gold 这种）
  source       {platform, url, author, captured_at}
  price?       价格观察（数字 + currency）
  location?    门店/地点
  stock?       现货/缺货/限购/补货
  raw_text     原文片段（溯源用）
  ai_confidence  0~1，stub 阶段先写 1.0
"""
from __future__ import annotations
import hashlib, json, os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OBS_FILE = DATA_DIR / "observations.jsonl"


def _obs_id(rec: dict) -> str:
    """基于 (source.url + raw_text 前 200 字) 做幂等 id，避免重复写入。"""
    seed = (rec["source"]["url"] + "|" + (rec.get("raw_text") or "")[:200]).encode()
    return "obs_" + hashlib.sha1(seed).hexdigest()[:16]


def _existing_ids() -> set[str]:
    if not OBS_FILE.exists():
        return set()
    ids = set()
    with OBS_FILE.open() as f:
        for line in f:
            try:
                ids.add(json.loads(line)["id"])
            except Exception:
                continue
    return ids


def emit(records: list[dict]) -> int:
    """写入新观察，返回新增条数。"""
    DATA_DIR.mkdir(exist_ok=True)
    seen = _existing_ids()
    added = 0
    with OBS_FILE.open("a") as f:
        for r in records:
            r.setdefault("source", {}).setdefault(
                "captured_at", datetime.now(timezone.utc).isoformat()
            )
            r.setdefault("ai_confidence", 1.0)
            r["id"] = _obs_id(r)
            if r["id"] in seen:
                continue
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            seen.add(r["id"])
            added += 1
    return added


def load_products() -> dict:
    p = DATA_DIR / "products.json"
    if not p.exists():
        return {}
    return json.loads(p.read_text())
