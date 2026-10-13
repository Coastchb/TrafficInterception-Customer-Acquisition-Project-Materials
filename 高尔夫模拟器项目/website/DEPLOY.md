# NEAGLE GOLF — 静态站点 & Cloudflare 部署说明

本站是**多页静态站点**，由最初的单文件 SPA（`index.html`）通过 `build.mjs` 生成，
用于改善 SEO / GEO。

---

## ⚠️ 部署前必读：不要乱敲 `npx wrangler deploy`

`wrangler` 查找配置的方式是：**从当前目录开始，逐级向上搜索父目录**。
如果它找不到配置，会**交互式地"帮你生成一个"**，生成的默认名字是 `my-worker`。

这个坑已经踩过两次，造成了真实的线上故障：

| 时间 | 现象 |
|---|---|
| 第一次 | 在 `高尔夫模拟器项目/` 跑的 deploy 生成了 `wrangler.jsonc`（`name = "y"`），部署到了一个多余的 Worker `y` |
| 第二次 | 同样位置又生成了 `wrangler.jsonc`（`name = "my-worker"`），部署出多余的 `my-worker`，并把整个 `website/`（107 个文件）当成静态资源上传 |

失败的后果不只是多一个垃圾 Worker —— 因为配置被劫持，
**你以为的"部署更新"实际上从没到达 `neaglegolf.com`**。

现在已加了两道防护，正常情况不会再出现：

1. `高尔夫模拟器项目/wrangler.toml` — 防护配置。即使在该目录误敲
   `npx wrangler deploy`，也会部署到**正确的 Worker + 正确的目录**，
   而不会再生成垃圾配置。
2. 仓库根目录的 `package.json` — 在任何位置执行 `npm run deploy` 都能正确部署。

> 如果 wrangler 弹窗问 *"No configuration file found. Create one?"* — **回答 No**。

---

## 目录结构

```
website/
├── index.html        # 原始 SPA（数据 / 样式的唯一来源）
├── build.mjs         # 静态站点生成器：读 index.html → 输出 ./dist
├── worker.js         # Worker 入口：HTTPS/主机名规范化 + 服务 ./dist 静态资源
├── wrangler.toml     # ★ 唯一权威的部署配置
├── dist/             # ← 生成的静态站点（部署的就是这个目录）
│   ├── index.html
│   ├── golf-simulators/
│   │   ├── index.html
│   │   ├── golfpai-s1/index.html
│   │   ├── golfpai-a1/index.html
│   │   ├── golfpai-x1/index.html
│   │   ├── rg-ruge/index.html
│   │   ├── faya-motion/index.html
│   │   ├── compare/index.html
│   │   └── buying-guide/index.html
│   ├── golf-ball-dispensers/
│   │   ├── index.html
│   │   ├── dispenser-machine/index.html
│   │   └── vending-machine/index.html
│   ├── catalog/index.html
│   ├── case-studies/
│   │   ├── index.html
│   │   ├── lincoln-4s/index.html
│   │   ├── automatives/index.html
│   │   ├── in-house/index.html
│   │   ├── clubhouse-indoor-golf/index.html
│   │   └── shenzhen-golf-range/index.html
│   ├── about/index.html
│   ├── 404.html
│   ├── sitemap.xml
│   └── robots.txt
└── DEPLOY.md
```

## 本地构建

```bash
node build.mjs      # 重新生成 ./dist
```

生成器复用 `index.html` 的 `<head>`（Tailwind CDN、字体、全部 CSS），
提取真实的产品 / 案例数据，再把每个页面渲染成**服务端 HTML**，
各自带上独立的 `<title>`、`meta description`、Open Graph 标签和 JSON-LD
（产品页为 `Product` + `BreadcrumbList`，全站为 `Organization` / `WebSite`）。

---

## 部署

目标是一个 **Worker**（静态资源模式），不是 Pages：

- Worker 名：`neaglegolf-website`
- 自定义域：`neaglegolf.com`（以及一条其他路由）
- 账号 ID：`ba841932e7978c0420ae8f031289ce2f`

### 方式 A — 命令行手动部署（推荐）

```bash
cd 高尔夫模拟器项目/website
npx wrangler deploy --config wrangler.toml
```

或在**任意目录**：

```bash
npm run deploy          # 仓库根目录
```

`--config wrangler.toml` 建议始终带上，可避免上级目录的配置劫持。
部署前若改了 `index.html` 或 `products/`，记得先 `node build.mjs`。

### 方式 B — GitHub Actions 自动部署

`.github/workflows/deploy.yml`：push 到 `main` 且改动了
`website/**` 或 `products/**/*.html` 时，自动构建 + 部署。

需要配置两个 Repository Secrets：

| Secret | 值 |
|---|---|
| `CLOUDFLARE_API_TOKEN` | 用 **Edit Cloudflare Workers** 模板创建的 Token |
| `CLOUDFLARE_ACCOUNT_ID` | `ba841932e7978c0420ae8f031289ce2f` |

> 为什么不用 Cloudflare 面板自带的 Workers Builds？
> 它在本仓库反复报 `Initializing build environment` 内部错误（官方仅建议重试 /
> 重建 Token / 重装 GitHub 集成）。而且即使构建成功，它执行的
> `npx wrangler deploy` 同样会被上级目录配置劫持。建议在面板里关闭该自动部署，
> 避免与 Actions 冲突。

### 方式 C — 绑定域名（已配置完成，供参考）

1. `neaglegolf.com` 已在 Cloudflare 管理。
2. Worker → **Settings → Domains & Routes** 添加 `neaglegolf.com` / `www.neaglegolf.com`。
3. Cloudflare 自动签发 **Universal SSL**，HTTPS 自动生效。
4. **SSL/TLS** 设为 **Full (strict)**，开启 **Always Use HTTPS**。

> 注意：产品图片目前用的是 `*.r2.dev` 开发域名。正式环境建议绑定自定义 R2 域名
> （如 `cdn.neaglegolf.com`），并同步更新 `index.html` 里 `catalogDb` 的 `image` URL。

---

## 部署后 SEO 检查清单

- [ ] GSC / Bing 提交 `https://neaglegolf.com/sitemap.xml`
- [ ] 用 Rich Results Test 验证产品页 `Product` 结构化数据
- [ ] 关注 GSC 的"页面编入索引"报告与 Core Web Vitals
- [ ] 确认 `canonical` / OG URL 与所选主域（apex 或 www）一致
- [ ] `/chatSend`、`/chatMessages`、`/profileSave`、`/profileGet` 是对外部代理的调用，
      不属于本站页面；它们返回 **410 Gone** 且在 `robots.txt` 中被 `Disallow`，
      用于清理 GSC 里的 404 报告
