# 去買 QuMai

个人自用的"日本买奢侈品包比价 + 现货情报"聚合工具。

不变现，不接其他人。看板把分散在 微博 / X / YouTube / Mercari / 大黑屋 / 品牌官网 上的价格 & 现货信息聚到一处，每个数字都带溯源链接。

## 当前阶段

骨架阶段。UI mockup 已就绪（见 `mockups/`），抓取/聚合/通知模块为占位实现，待接入真实数据源。

## 架构（一图）

```
GitHub Actions (cron 每 10 分钟)
  ├─ scrapers/*.py       拉数据（RSSHub / 官方 API / 网页）
  ├─ extractor/          Claude Haiku 把非结构化文本提成字段
  ├─ aggregator/         按款号聚合 + 算价差
  ├─ data/*.json         JSON 文件存（git 即数据库）
  └─ notifier/           命中目标价 → Telegram / Bark 推送

       ↓
GitHub Pages (静态站)
  └─ site/index.html     读 ../data/*.json 渲染看板
```

## 目录

| 路径 | 用途 |
| --- | --- |
| `mockups/` | 三套 UI mock，cute 版为主 |
| `site/` | GitHub Pages 部署的实际看板 |
| `scrapers/` | 各数据源的抓取脚本 |
| `extractor/` | Claude Haiku 结构化提取 |
| `aggregator/` | 按款号聚合价格视图 |
| `notifier/` | 推送通道 |
| `data/products.json` | 关注款主表（手维护） |
| `data/observations.jsonl` | 所有原始观察 · append-only · 永不删 |
| `data/aggregates.json` | 计算结果，每次 cron 重算 |
| `snapshots/` | 原帖截图归档（溯源用） |
| `.github/workflows/` | GitHub Actions cron + Pages 部署 |
| `COWORK.md` | 给 Cowork Agent 的项目说明书 |

## 跑起来

```bash
# 本地预览看板
python -m http.server 8080 -d site
# → 浏览器开 http://localhost:8080

# 跑一次抓取（需要 .env 配 API key）
cp .env.example .env  # 然后填 ANTHROPIC_API_KEY 等
python -m scrapers.exchange_rate
python -m aggregator.compute
```

## 下一步

见 [COWORK.md](COWORK.md) 项目交接文档，里面有当前 TODO 清单和决策上下文。

## License

私人用途，未公开授权。
