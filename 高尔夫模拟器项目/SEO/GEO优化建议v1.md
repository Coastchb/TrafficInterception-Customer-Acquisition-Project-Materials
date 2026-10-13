我已经把压缩包里的**源码、SSG 构建脚本、`dist` 实际生成页面、sitemap、robots**都检查了一遍。

先说结论：

> **这版相比上一版已经从“SEO 架构明显不友好”升级到了“基本具备 SEO/GEO 上线基础”，方向是正确的。**
>
> 但目前还有几个**非常关键的问题没有处理干净**，其中有一个属于 **P0 级问题：所有内页的 canonical 和 `og:url` 都错误地指向首页**。

如果现在直接上线，我会给：

| 项目                  |       当前评分 | 评价                     |
| ------------------- | ---------: | ---------------------- |
| URL 架构              |      ⭐⭐⭐⭐⭐ | 已经很好                   |
| 静态 HTML / 可抓取性      |      ⭐⭐⭐⭐⭐ | 明显改善                   |
| Title / Description |      ⭐⭐⭐⭐☆ | 基本完善                   |
| Sitemap             |      ⭐⭐⭐⭐☆ | 已具备                    |
| Robots              |      ⭐⭐⭐⭐⭐ | 没明显问题                  |
| 内链                  |      ⭐⭐⭐⭐☆ | 基础很好                   |
| Product Schema      |      ⭐⭐⭐⭐☆ | 已经有，但需要增强              |
| Canonical           |      ⭐☆☆☆☆ | **存在严重错误**             |
| OG / Social         |      ⭐⭐☆☆☆ | URL 和图片需要修             |
| Case Study SEO      |      ⭐⭐☆☆☆ | 目前仍偏弱                  |
| GEO                 |      ⭐⭐⭐☆☆ | 已有基础，但还没真正发挥产品数据优势     |
| E-E-A-T / Entity    |      ⭐⭐⭐☆☆ | 有基础，证据链还不够             |
| 性能 SEO              |      ⭐⭐⭐☆☆ | Tailwind CDN 等问题需要处理   |
| **综合**              | **约 7/10** | **修完几个关键点可以到 8.5+/10** |

---

# 一、最大的进步：你已经真正解决了上一版最核心的问题

上一版最大的问题是：

```text
index.html
    ↓
JavaScript
    ↓
Hash 路由
    ↓
#detail/...
```

现在已经改成：

```text
/
├── golf-simulators/
│   ├── golfpai-s1/
│   ├── golfpai-a1/
│   ├── golfpai-x1/
│   ├── rg-ruge/
│   └── faya-motion/
│
├── golf-ball-dispensers/
│   ├── dispenser-machine/
│   └── vending-machine/
│
├── catalog/
├── case-studies/
└── about/
```

而且这些页面是真正生成出来的：

```text
dist/golf-simulators/golfpai-s1/index.html
dist/golf-simulators/golfpai-a1/index.html
...
```

这点非常重要。

你的 `build.mjs` 已经采用 SSG，把产品数据直接生成到 HTML，而不是依赖浏览器执行 JS 后才出现。

**这是这次优化最大的成功。**

---

# 二、现在第一个必须马上修的问题：Canonical 全错了

这是目前最严重的问题。

我检查了：

```text
/golf-simulators/
```

```text
/golf-simulators/golfpai-s1/
```

```text
/golf-simulators/golfpai-a1/
```

```text
/golf-ball-dispensers/dispenser-machine/
```

```text
/about/
```

```text
/case-studies/
```

结果全部是：

```html
<link rel="canonical" href="https://www.neaglegolf.com/">
```

也就是说：

> **每个页面都告诉 Google：“我的规范 URL 是首页。”**

这是明显错误。

例如：

### GOLFPAI S1

应该：

```html
<link
  rel="canonical"
  href="https://www.neaglegolf.com/golf-simulators/golfpai-s1/"
>
```

而现在：

```html
<link
  rel="canonical"
  href="https://www.neaglegolf.com/"
>
```

---

# 三、为什么这个问题非常严重？

因为你现在已经花了大量精力生成：

```text
/golf-simulators/golfpai-s1/
```

这样的独立 SEO 页面。

但 canonical 又告诉搜索引擎：

> “不要把这个页面作为独立页面，首页才是规范页面。”

这会削弱甚至阻碍产品页独立获得搜索排名。

---

# 四、而且 `og:url` 也全部错了

例如 GOLFPAI S1：

```html
<meta property="og:url"
      content="https://www.neaglegolf.com/">
```

正确应该：

```html
<meta
  property="og:url"
  content="https://www.neaglegolf.com/golf-simulators/golfpai-s1/"
>
```

所以现在：

### Canonical

❌ 错

### OG URL

❌ 错

这两个必须一起改。

---

# 五、其实你的 `build.mjs` 已经非常容易修

现在：

```javascript
function page({ title, description, extraHead = '', bodyClass = '', main, navActive = '' }) {
```

这里应该增加：

```javascript
url
```

然后：

```javascript
.replace(
  /<link rel="canonical"[^>]*>/i,
  `<link rel="canonical" href="${esc(url)}">`
)
```

同时：

```javascript
.replace(
  /<meta property="og:url"[^>]*>/i,
  `<meta property="og:url" content="${esc(url)}">`
)
```

---

# 六、建议进一步把 `og:image` 也变成每页独立

目前我发现：

**所有页面都使用同一张：**

```text
card_bg_1.jpg
```

例如：

```text
GOLFPAI S1
GOLFPAI A1
GOLFPAI X1
About
Case Studies
```

全部是这个 OG Image。

这对于 GEO 不是致命问题，但对于：

* Google Discover
* 社交分享
* WhatsApp 分享
* Facebook
* LinkedIn
* X
* AI 页面理解

都不是最佳方案。

---

## GOLFPAI S1 应该：

```text
og:image =
/images/S1/0.jpg
```

A1：

```text
/images/A1/0.jpg
```

X1：

```text
/images/X1/0.jpg
```

案例：

```text
/images/case-studies/xxx.jpg
```

首页才用：

```text
card_bg_1.jpg
```

---

# 七、第二个明显问题：Case Study 还是没有真正独立页面

这个是我认为**下一阶段最重要的 GEO 改造点**。

目前 build 里面：

```javascript
const caseCards = caseStudies.map(c => `
  <div class="card-glow ...">
```

最终只是：

```text
/case-studies/
```

里面有很多卡片。

但是：

> **每一个 Case Study 没有独立 URL。**

而且卡片甚至不是 `<a>`：

```html
<div class="card-glow">
```

不是：

```html
<a href="/case-studies/clubhouse-indoor-golf/">
```

---

# 八、这意味着你之前网站里非常宝贵的案例数据，现在仍然没有被充分 SEO 化

你原来的 `caseStudies` 数据其实非常适合 GEO。

比如：

```text
客户
地点
项目类型
使用设备
安装数量
空间
项目成果
```

这些东西对于 AI 回答：

> Which golf simulator companies have experience with commercial indoor golf facilities?

是非常有价值的。

---

# 九、建议把 Case Study 做成真正的页面

例如：

```text
/case-studies/clubhouse-indoor-golf/
```

页面：

```text
H1
Clubhouse Indoor Golf

Project Overview

Location
Richmond, BC

Facility Type
Commercial Indoor Golf

Equipment
RG Eagleye III

Number of Bays
6

VIP Rooms
3

Course Library
180+

Project Challenges

Solution

Results

Gallery

Related Products
```

---

# 十、这会极大增强 GEO

比如 AI 被问：

> Has NEAGLE GOLF worked on commercial indoor golf facilities?

它就可能从你的案例页面找到：

```text
Clubhouse Indoor Golf
6 simulator bays
3 VIP rooms
180+ courses
commercial indoor golf facility
```

这比一个 `/case-studies/` 卡片列表强很多。

---

# 十一、第三个问题：目前 GEO 已经开始做了，但还不够“答案化”

你首页现在增加了：

```text
Frequently Asked Questions
```

这是一个明显的进步。

而且问题本身很好：

```text
What is the best golf simulator for a commercial range?

Do you supply automated ball dispensers?

Where do you ship?
```

这是 GEO 正确方向。

---

# 十二、但目前 FAQ 还缺 Schema

这是一个非常值得补的地方。

目前 FAQ 是：

```html
<h3>Frequently Asked Questions</h3>
```

然后：

```html
<p>What is the best golf simulator for a commercial range?</p>
<p>A ceiling or overhead launch-monitor system...</p>
```

内容存在。

但是没有：

```json
{
  "@type": "FAQPage"
}
```

---

## 建议增加

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is the best golf simulator for a commercial range?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "..."
      }
    }
  ]
}
```

不过这里要注意：

**Schema 不是为了“骗 Google”，而是要和页面真实可见 FAQ 内容一致。**

---

# 十三、产品 Schema 已经有了，这一点很好

例如 GOLFPAI S1 已经生成：

```json
{
  "@type": "Product",
  "name": "GOLFPAI S1 Indoor Golf Simulator",
  "description": "...",
  "image": [...],
  "brand": {
    "@type": "Brand",
    "name": "NEAGLE GOLF"
  },
  "offers": {
    "@type": "Offer",
    "price": "42516.00",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  }
}
```

这是正确方向。

---

# 十四、但是 Product Schema 还可以增强

目前只有：

```text
name
description
image
brand
offers
category
```

建议增加：

```text
sku
url
seller
itemCondition
```

例如：

```json
{
  "@type": "Product",
  "name": "GOLFPAI S1 Indoor Golf Simulator",
  "sku": "golfpai-s1",
  "url": "https://www.neaglegolf.com/golf-simulators/golfpai-s1/",
  "brand": {
    "@type": "Brand",
    "name": "NEAGLE GOLF"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://www.neaglegolf.com/golf-simulators/golfpai-s1/",
    "price": "42516.00",
    "priceCurrency": "USD",
    "itemCondition": "https://schema.org/NewCondition",
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "Organization",
      "name": "NEAGLE GOLF"
    }
  }
}
```

---

# 十五、这里还有一个需要特别确认的问题：`InStock`

你现在所有产品都写：

```json
"availability": "https://schema.org/InStock"
```

这必须和真实业务一致。

如果实际上是：

```text
询价
定制
生产
预售
下单后生产
```

就不要简单写 `InStock`。

否则结构化数据和真实商业状态不一致。

如果不是现货，更适合根据实际业务使用相应状态，或者干脆暂时不提供 availability。

---

# 十六、Organization Schema 目前也有一个问题

现在：

```json
"logo":
"https://.../images/card_bg_1.jpg"
```

这张实际上更像视觉背景图。

**不建议拿它作为 Organization Logo。**

应该使用真正的：

```text
NEAGLE GOLF logo
```

最好是：

```text
logo.svg
```

或者高质量 PNG。

---

# 十七、`sameAs` 也比较弱

现在：

```json
"sameAs": [
  "https://api.whatsapp.com/send?phone=13142242264"
]
```

WhatsApp 联系地址不太适合作为品牌实体的 `sameAs`。

`sameAs` 最适合：

```text
LinkedIn
Facebook
Instagram
YouTube
Wikipedia
Crunchbase
官方品牌社交账号
```

如果你们有真实官方账号，建议加入。

**不要为了 GEO 编造账号。**

---

# 十八、你的 WebSite Schema 还有一个小问题

现在：

```json
"potentialAction": {
  "@type": "SearchAction",
  "target": "https://www.neaglegolf.com/#directory?q={search_term_string}"
}
```

但你现在真正部署的是静态多页面站点。

也就是说：

```text
#directory?q=xxx
```

并不是一个真正的服务器搜索 URL。

所以这个 `SearchAction`：

> **建议删除。**

除非网站实际上有一个可以处理：

```text
/search?q=xxx
```

的搜索页面。

---

# 十九、这是一个很容易被忽略的问题

以前 SPA：

```text
#directory
```

有意义。

现在 SSG：

```text
/catalog/
```

已经是实际页面。

所以你的 Schema 仍然保留：

```text
#directory
```

实际上说明：

> **Schema 已经更新了一半，但没有完全跟着新架构迁移。**

建议彻底清理旧 SPA 逻辑。

---

# 二十、首页 H1 现在是：

```text
Precision Golf Simulation, Redefined
```

视觉上很漂亮。

但从 SEO/GEO 来说，我还是建议稍微增强。

比如：

```text
Premium Golf Simulators & Indoor Golf Systems
```

或者：

```text
Golf Simulators, Launch Monitors & Automated Golf Systems
```

然后副标题再负责品牌调性：

```text
Precision Golf Simulation, Redefined.
```

---

## 原因很简单：

现在：

```text
Precision Golf Simulation, Redefined
```

用户知道它是高尔夫。

但 Google / AI 还需要推断：

> 你具体卖什么？

而：

```text
Golf Simulators & Indoor Golf Systems
```

属于非常明确的实体表达。

---

# 二十一、不过你首页正文已经比上一版好很多

现在已经有：

> NEAGLE GOLF is a global provider of tour-grade golf simulators, launch monitors, and 4K golf simulation systems...

这个非常好。

而且又增加：

> automated golf ball dispensers

这使首页主题更加明确。

所以：

**首页正文方向我基本认可。**

不建议继续无脑增加关键词。

---

# 二十二、产品页目前的 SEO 内容也已经达到“合格线”

例如 S1：

```text
H1
GOLFPAI S1 Indoor Golf Simulator

Key Highlights

Specifications

More from Golf Simulators
```

同时还有：

```text
tagline
price
use cases
highlights
specification table
images
related products
```

这是一个比较标准的产品 SEO 页面。

---

# 二十三、但是 GEO 还可以再加强一个非常重要的模块

目前产品页面：

```text
Key Highlights
Specifications
```

建议中间增加：

# Best For

例如 S1：

```text
Best For

• Luxury residential golf rooms
• Premium golf clubs
• Commercial indoor golf facilities
• Luxury hotels
• Corporate showrooms
```

然后：

# Why Choose GOLFPAI S1?

用 3～5 条完整句子回答。

---

# 二十四、为什么我要特别强调这一点？

因为现在：

```text
Private Villas
Premium Clubs
Corporate Showrooms
Elite Clubs
Luxury Hotels
```

只是几个标签。

AI 可以理解，但不如：

> GOLFPAI S1 is designed for luxury residential golf rooms, premium golf clubs, hotels, corporate showrooms, and other high-end indoor golf facilities.

这种自然语言更容易作为答案的一部分被引用。

---

# 二十五、建议产品页增加“Quick Answer”

例如：

## GOLFPAI S1 — Quick Answer

> **GOLFPAI S1 is a premium indoor golf simulator designed for luxury homes, premium golf clubs, hotels, and commercial facilities. It combines 6,000 FPS vision tracking, 4K laser projection, and more than 110 photorealistic courses.**

这种内容对于 GEO 非常有价值。

---

# 二十六、你的规格表非常适合 AI

这一点做得很好：

```html
<table>
  <tr>
    <th>...</th>
    <td>...</td>
  </tr>
</table>
```

这是比：

```text
<div>6,000 FPS</div>
<div>4K</div>
<div>110+</div>
```

更好的结构。

因为 AI 可以明确建立：

```text
Product
→ Tracking
→ 6000 FPS

Product
→ Projection
→ 4K

Product
→ Course Library
→ 110+
```

所以**规格表建议保留**。

---

# 二十七、Category 页面目前稍微偏薄

例如：

```text
Golf Simulators
Professional golf simulators for every space, venue, and skill level — indoors or out.
```

然后直接产品卡片。

SEO 基础上没问题。

但如果你想竞争：

```text
golf simulator
commercial golf simulator
indoor golf simulator
```

这种词，分类页应该至少有：

```text
H1

Intro

Types of Golf Simulators

How to Choose

Recommended for Different Spaces

Comparison

FAQ

Products
```

---

# 二十八、我建议 `/golf-simulators/` 增加 500～1000 英文词左右的高质量内容

不是为了凑字数。

而是覆盖：

```text
What is an indoor golf simulator?

Types of golf simulators

Home vs commercial golf simulators

Golf simulator space requirements

Tracking technology

Projection systems

How to choose
```

然后产品列表。

这样它才会从：

> 产品目录页

升级成：

> **Golf Simulator Topic Hub**

---

# 二十九、`/golf-ball-dispensers/` 也是一样

目前：

```text
Dispenser Machines
Automated golf ball dispensing and vending solutions for driving ranges and golf facilities.
```

然后两个产品。

建议增加：

```text
Automatic Golf Ball Dispensers

Golf Ball Vending Machines

How Automated Ball Dispensing Works

Benefits for Driving Ranges

Cashless Payment

Labor Cost Reduction

Revenue Optimization

Which System Should You Choose?

FAQ
```

这会明显提升 GEO 覆盖面。

---

# 三十、目前 Case Studies 是 SEO/GEO 最大的内容浪费

因为你已经有：

```text
caseStudies
```

数据。

但现在只是：

```text
卡片
+
图片
+
标题
+
描述
```

没有：

```text
URL
H1
项目详情
结构化数据
内部链接
产品关联
地点
Facility Type
Result
```

---

# 三十一、我建议 Case Study 至少做到这个程度

例如：

```text
/case-studies/clubhouse-indoor-golf/
```

页面：

```text
H1
Clubhouse Indoor Golf

Commercial Indoor Golf Installation in Richmond

Project Summary

Facility Type
Commercial Indoor Golf

Location
Richmond, BC

Installation
6 simulator bays

VIP Rooms
3

Golf Courses
180+

Technology

Results

Gallery

Related Golf Simulator
```

---

# 三十二、这对于 GEO 特别重要

因为 AI 很喜欢：

> “具体事实 + 具体实体 + 数字”

比如：

```text
6 simulator bays
3 VIP rooms
180+ courses
Richmond
commercial indoor golf
```

这就是非常好的：

**Citation Material**

---

# 三十三、还有一个比较大的 SEO 性能问题：Tailwind CDN

你的 `build.mjs` 明确写着：

> keeps Tailwind CDN

生成页面仍然加载：

```html
<script src="https://cdn.tailwindcss.com"></script>
```

这对于开发原型非常方便。

但是如果是正式生产站：

**我不建议继续使用 Tailwind CDN。**

---

# 三十四、为什么？

因为生产站现在是：

```text
HTML
+
Tailwind CDN JS
+
FontAwesome CDN
+
Tailwind runtime processing
```

这会增加：

* JS 执行
* Main Thread 工作
* 页面加载时间
* Core Web Vitals 风险
* 移动端性能开销

SEO 不是只看内容。

Google 的页面体验也很重要。

---

# 三十五、建议生产环境：

```text
Tailwind CLI
        ↓
purge unused classes
        ↓
生成 static CSS
        ↓
<link rel="stylesheet" href="/assets/site.css">
```

而不是：

```html
<script src="https://cdn.tailwindcss.com"></script>
```

---

# 三十六、FontAwesome 也可以进一步优化

现在：

```html
cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css
```

整个 FontAwesome CSS 都加载。

实际上网站使用的图标数量有限。

可以考虑：

```text
SVG inline
```

或者只加载需要的 icon。

这对性能比 SEO 本身更重要。

---

# 三十七、图片方面，这一版已经不错

我检查了生成页面：

```text
img
alt
loading
```

产品图片：

```html
<img
  src="..."
  alt="GOLFPAI S1 Indoor Golf Simulator"
>
```

基本都有 alt。

这是正确的。

---

# 三十八、但是首屏 Hero 图片需要特别处理

现在很多图片用了：

```text
loading="lazy"
```

这对于下面的产品卡片是对的。

但：

> **LCP 图片绝对不要 lazy。**

如果首页 Hero 使用真正的 `<img>`，应该：

```html
fetchpriority="high"
loading="eager"
```

并考虑：

```html
<link rel="preload" as="image">
```

---

# 三十九、图片 URL 目前使用 `r2.dev`

`DEPLOY.md` 自己也已经意识到了这个问题：

> product images currently use `*.r2.dev` dev URLs.

这个判断是正确的。

正式上线建议：

```text
cdn.neaglegolf.com
```

例如：

```text
https://cdn.neaglegolf.com/images/S1/0.jpg
```

而不是：

```text
https://pub-xxxx.r2.dev/images/S1/0.jpg
```

---

# 四十、这不仅是“好不好看”的问题

统一 CDN 域名以后：

```text
cdn.neaglegolf.com
```

有利于：

* 品牌可信度
* 图片长期稳定
* 缓存策略
* URL 管理
* 后续迁移
* 图片 SEO
* OG image 稳定性

---

# 四十一、Sitemap 现在已经正确很多

目前：

```text
/
 /golf-simulators/
 /golf-simulators/golfpai-s1/
 /golf-simulators/golfpai-a1/
 ...
```

这已经是正确方向。

上一版 Hash URL 已经消失。

这是一个明显进步。

---

# 四十二、但 sitemap 还有两个建议

目前所有页面：

```xml
<changefreq>weekly</changefreq>
<priority>0.8</priority>
```

我不会把它当成严重问题。

Google 不会因为：

```text
priority=0.8
```

就给你更高排名。

所以不用过度纠结。

反而建议增加：

```xml
<lastmod>2026-08-25</lastmod>
```

并在内容真正修改时更新。

---

# 四十三、robots.txt 目前没问题

现在：

```text
User-agent: *
Allow: /

Sitemap: https://www.neaglegolf.com/sitemap.xml
```

完全可以。

暂时不需要搞复杂。

---

# 四十四、还有一个很容易忽略的问题：404 页面

我检查了：

```text
dist/404.html
```

它现在的：

```html
canonical
```

居然也是：

```text
https://www.neaglegolf.com/
```

404 页面最好：

**不要有 canonical 指向首页。**

甚至建议：

```html
<meta name="robots" content="noindex, follow">
```

404 本身应该返回 HTTP 404 状态。

---

# 四十五、现在 Organization Schema 还可以进一步完善

目前：

```json
{
 "@type": "Organization",
 "name": "NEAGLE GOLF",
 "email": "...",
 "areaServed": "Worldwide"
}
```

基础不错。

如果是真实信息，可以继续增加：

```text
telephone
logo
address
contactPoint
foundingDate
sameAs
```

尤其：

```json
"contactPoint": {
  "@type": "ContactPoint",
  "contactType": "sales",
  "email": "service@neaglegolf.com",
  "telephone": "+1..."
}
```

---

# 四十六、GEO 角度还有一个更重要的问题：缺少“谁、在哪里、服务谁”

现在网站强调：

```text
Worldwide
```

但是如果你们有真实的：

```text
US
Canada
Europe
Asia
```

服务区域，最好明确写出来。

例如：

> NEAGLE GOLF supplies and installs golf simulator systems for residential and commercial customers across the United States, Canada, and other international markets.

**前提是业务事实确实如此。**

不要为了 GEO 虚构服务区域。

---

# 四十七、我还建议增加一个“实体身份页面”

也就是 About 页面不要只有：

> Engineering Physical Authenticity Indoors.

这种品牌文案。

还应该非常直接地回答：

### Who is NEAGLE GOLF?

### What does NEAGLE GOLF sell?

### Who are its products designed for?

### Does NEAGLE GOLF provide installation?

### Where does NEAGLE GOLF operate?

### What technologies are used?

### What products does NEAGLE GOLF offer?

这种结构对 AI 非常友好。

---

# 四十八、目前 About 页有一个 GEO 优势

这一段其实很好：

> Formed by a collective of aerospace radar developers, acoustic research physicists, and competitive touring professionals...

以及：

> 99.9% Trajectory Precision

这类内容可以作为：

**品牌专业性 / 技术背景**

但是要注意：

> 如果这些表述没有真实业务证据，建议谨慎。

尤其是：

```text
99.9%
sub-millimetric
micro-Doppler
LiDAR
100,000 strikes
```

这些都是非常具体的技术声明。

GEO 不仅需要“听起来专业”，还需要**可验证的事实一致性**。

---

# 四十九、这版最大的 GEO 缺口，我总结成一句话：

> **你已经把“产品”做成了 SEO 页面，但还没有把“产品 + 场景 + 问题 + 案例”做成 GEO 知识网络。**

目前：

```text
Product
   ↓
Product Page
```

已经完成。

下一步应该：

```text
Product
   ↓
Use Case
   ↓
Problem
   ↓
Solution
   ↓
Case Study
   ↓
Evidence
```

---

# 五十、我建议最终形成这样的内容网络

```text
                         NEAGLE GOLF
                              │
          ┌───────────────────┼───────────────────┐
          ↓                   ↓                   ↓
       Products           Solutions           Knowledge
          │                   │                   │
      S1 / A1 / X1        Home                  Cost
      Ruge / FAYA          Hotel                 Space
      Dispenser            Club                  Installation
          │                Range                 Comparison
          │                Venue                 FAQ
          └───────────────────┼───────────────────┘
                              ↓
                         Case Studies
                              ↓
                          Evidence
```

这才是我认为比较完整的 **GEO Architecture**。

---

# 五十一、如果按照优先级，我建议你现在不要再“大改 UI”

这版 UI / 页面视觉我认为已经够用了。

现在应该停止：

> “继续设计页面”

转而：

> **SEO/GEO 技术收尾 + 内容架构补齐。**

---

# 五十二、我的 P0 清单

这几个我建议**上线前必须修**：

### P0-1

**修 canonical**

```text
/golf-simulators/
→ /golf-simulators/

/golf-simulators/golfpai-s1/
→ /golf-simulators/golfpai-s1/
```

### P0-2

**修 OG URL**

同上。

### P0-3

**每个页面使用独立 OG Image**

### P0-4

**删除 WebSite Schema 中无效的 Hash SearchAction**

### P0-5

**404 不要 canonical 到首页**

### P0-6

**确认 Product `InStock` 是否真实**

---

# 五十三、P1：强烈建议

### P1-1

Case Study 独立页面。

### P1-2

Case Study `<a href>` 内链。

### P1-3

FAQ Schema。

### P1-4

Product Schema 增加：

```text
sku
url
seller
itemCondition
```

### P1-5

Organization Schema 增加真实：

```text
logo
telephone
contactPoint
sameAs
```

---

# 五十四、P2：GEO 核心建设

建议增加：

```text
/golf-simulator-buying-guide/

/golf-simulator-cost/

/golf-simulator-room-size/

/golf-simulator-installation/

/golf-simulator-comparison/

/radar-vs-camera-golf-simulator/
```

以及：

```text
/golf-simulators/for-home/

/golf-simulators/for-hotels/

/golf-simulators/for-golf-clubs/

/golf-simulators/for-driving-ranges/

/golf-simulators/for-commercial-facilities/
```

---

# 五十五、我特别推荐你做一个“产品比较系统”

你现在已经有非常结构化的产品数据。

例如：

```text
GOLFPAI S1
GOLFPAI A1
GOLFPAI X1
Ruge
FAYA
```

可以自动生成：

```text
Golf Simulator Comparison
```

然后：

|            | S1     | A1     | X1             | Ruge        | FAYA               |
| ---------- | ------ | ------ | -------------- | ----------- | ------------------ |
| Best For   | Luxury | Home   | Range          | Commercial  | Home/Entertainment |
| Tracking   | Vision | Vision | Radar + Vision | Triple Lens | Dual Sensor        |
| Projection | 4K     | 4K     | 4K             | 4K          | 4K                 |
| Courses    | 110+   | 80+    | ...            | 180+        | 100+               |
| Space      | ...    | ...    | ...            | ...         | ...                |
| Price      | ...    | ...    | ...            | ...         | ...                |

这种页面非常适合：

**Google SEO + AI GEO + 用户转化。**

---

# 五十六、最终判断

如果拿你上一版和现在这版相比：

### 上一版：

```text
漂亮官网
      +
SPA
      +
大量 JS
      ↓
SEO 很弱
GEO 很弱
```

### 现在：

```text
漂亮官网
      +
SSG
      +
独立 URL
      +
独立产品 HTML
      +
Product Schema
      +
Breadcrumb
      +
Sitemap
      +
FAQ 内容
      ↓
SEO 已经基本合格
GEO 开始具备基础
```

这是一个**非常明显的进步**。

---

# 但现在最需要警惕的就是这个问题

```text
所有页面
        ↓
canonical
        ↓
https://www.neaglegolf.com/
```

这是目前我最建议你**第一时间修掉**的。

因为你已经完成了最难的：

> **SSG + 独立 URL + 产品页面**

结果 canonical 把这些页面又全部“指回首页”了。

---

## 我给这版的最终评价

### SEO

**7.5 / 10**

把 canonical、OG、404、Schema、性能几个问题修完：

**8.5～9 / 10**

### GEO

现在：

**6.5 / 10**

如果进一步补：

```text
Case Study 独立页面
+
Solution 页面
+
FAQ
+
Comparison
+
Buying Guide
+
Installation Guide
+
Cost Guide
+
Entity / E-E-A-T
```

可以做到：

**8.5～9 / 10**

---

**最重要的一点：你现在已经不需要再推倒重做。**

当前 `build.mjs` 的 SSG 思路是对的，`catalogDb` → 产品页的自动生成也非常适合后续扩展。下一步应该直接在这个构建系统上补齐 **canonical/OG → Case Study → FAQ/Schema → Solution → GEO 内容集群**，而不是再回到 SPA 或重新设计一套网站。
