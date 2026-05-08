"""
JPY → CNY 汇率，写到 data/rate.json。
免费 API: open.er-api.com（无需 key）。失败时不写，让上游用上次的值。
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
RATE_FILE = ROOT / "data" / "rate.json"


def fetch() -> dict | None:
    try:
        r = httpx.get("https://open.er-api.com/v6/latest/JPY", timeout=10)
        r.raise_for_status()
        d = r.json()
        cny = d["rates"]["CNY"]
        return {
            "jpy_to_cny": cny,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "source": "open.er-api.com",
        }
    except Exception as e:
        print(f"[rate] fetch failed: {e}")
        return None


def main():
    rate = fetch()
    if rate is None:
        return
    RATE_FILE.parent.mkdir(exist_ok=True)
    RATE_FILE.write_text(json.dumps(rate, ensure_ascii=False, indent=2))
    print(f"[rate] JPY 1 = CNY {rate['jpy_to_cny']:.4f}")


if __name__ == "__main__":
    main()
