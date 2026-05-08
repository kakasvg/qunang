"""
读 aggregates.json，把 target_hit=true 的款推到 Telegram。
对每个款用 data/notified.json 记录已推送的 (pid, lowest_cny) 防重复。
"""
from __future__ import annotations
import json, os
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
NOTIFIED = DATA / "notified.json"


def send(text: str) -> bool:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat:
        print("[telegram] no credentials, skip")
        return False
    try:
        r = httpx.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat, "text": text, "parse_mode": "Markdown"},
            timeout=10,
        )
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"[telegram] send failed: {e}")
        return False


def main():
    agg_path = DATA / "aggregates.json"
    if not agg_path.exists():
        print("[telegram] no aggregates.json, skip")
        return
    agg = json.loads(agg_path.read_text())
    notified = json.loads(NOTIFIED.read_text()) if NOTIFIED.exists() else {}

    sent = 0
    for pid, info in agg["products"].items():
        if not info.get("target_hit"):
            continue
        key = f"{pid}@{info['lowest_cny']}"
        if notified.get(pid) == key:
            continue
        msg = (
            f"🎯 *目标价命中*\n"
            f"*{info['name']}*\n"
            f"最低价 ¥{info['lowest_cny']:,} · 比官方省 ¥{abs(info.get('diff_vs_official') or 0):,}\n"
            f"24h 观察数 {info['observations_24h']}"
        )
        if send(msg):
            notified[pid] = key
            sent += 1

    NOTIFIED.write_text(json.dumps(notified, ensure_ascii=False, indent=2))
    print(f"[telegram] sent {sent} alerts")


if __name__ == "__main__":
    main()
