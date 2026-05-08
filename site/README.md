# site/

GitHub Pages 部署的实际看板。

`index.html` 当前是从 `mockups/02-cute.html` 直接复制过来的静态版（数据硬编码在 `<script>` 里）。

## 接入真实数据的下一步

把硬编码的 `top30` / `feedData` / `prices` 数组替换成从 JSON 文件读取：

```js
const [aggregates, products, observations, rate] = await Promise.all([
  fetch('data/aggregates.json').then(r => r.json()),
  fetch('data/products.json').then(r => r.json()),
  fetch('data/observations.jsonl').then(r => r.text()).then(t =>
    t.trim().split('\n').map(JSON.parse)
  ),
  fetch('data/rate.json').then(r => r.json()),
]);
```

`pages.yml` 工作流会把仓库根的 `data/` 和 `snapshots/` 拷到 `_site/`，所以从前端看：

```
/data/aggregates.json
/data/products.json
/data/observations.jsonl
/data/rate.json
/snapshots/<obs-id>.png
```

都能直接 fetch。
