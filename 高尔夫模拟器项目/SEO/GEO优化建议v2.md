我已经对这次上传的 `website(1).zip` 做了完整源码检查，重点看了：

* `index.html`
* `build.mjs`
* `dist/` 实际生成的所有页面
* `sitemap.xml`
* `robots.txt`
* 产品页
* 产品对比页
* Buying Guide
* Case Study 列表及独立案例页
* JSON-LD Schema
* Title / Description / Canonical / OG
* H1/H2
* 图片 Alt
* 内链结构
* 产品数据及规格数据
* 404 页面

这次版本和之前相比，**SEO/GEO 架构已经明显成熟很多**。尤其是已经从 SPA/Hash 路由真正变成了 SSG 多页面，并且现在已经加入了独立 Case Study、Comparison、Buying Guide，这几个方向都是对的。

不过，我认为目前仍然存在几个**比较重要的 SEO/GEO 问题**，尤其是：

> **Case Study 的 Schema 使用方式不正确、产品页存在双 H1、首页/分类页内容深度仍不足、GEO 的“问题—答案—证据”体系还没有完全建立。**

下面我按优先级详细拆解。

---

# 一、整体评价

我会给当前版本：

| 维度                |         当前评分 | 评价                  |
| ----------------- | -----------: | ------------------- |
| URL 架构            |         9/10 | 很好                  |
| SSG / HTML 可抓取性   |         9/10 | 很好                  |
| Title             |       8.5/10 | 基本完善                |
| Meta Description  |         8/10 | 基本完善                |
| Canonical         |         9/10 | **上一版问题已经修复**       |
| Sitemap           |         9/10 | 完整                  |
| Robots            |         9/10 | 正常                  |
| 产品页 SEO           |       8.5/10 | 基础很好                |
| Product Schema    |         8/10 | 已比较完整               |
| Breadcrumb Schema |         8/10 | 已加入                 |
| Case Study SEO    |       6.5/10 | 有页面，但 Schema/内容仍需优化 |
| Comparison SEO    |         8/10 | 很有价值                |
| Buying Guide      |       7.5/10 | 方向正确，但内容偏薄          |
| 内链                |         8/10 | 基础较好                |
| 图片 SEO            |         8/10 | Alt 基本完整            |
| GEO               |         7/10 | 已经有明显基础             |
| E-E-A-T / Entity  |       6.5/10 | 需要加强证据              |
| Core Web Vitals   |         6/10 | 仍有性能优化空间            |
| **综合**            | **约 7.8/10** | 已经接近正式上线版本          |

如果把几个关键问题修掉，我认为可以达到：

**SEO：8.5～9/10**

**GEO：8～8.5/10**

---

# 二、最大的好消息：之前最严重的 Canonical 问题已经修好了

这一版我重点检查了所有页面。

例如：

### S1

```html
<link rel="canonical"
href="https://www.neaglegolf.com/golf-simulators/golfpai-s1/">
```

### A1

```html
<link rel="canonical"
href="https://www.neaglegolf.com/golf-simulators/golfpai-a1/">
```

### Case Study

```html
<link rel="canonical"
href="https://www.neaglegolf.com/case-studies/clubhouse/">
```

### Buying Guide

```html
<link rel="canonical"
href="https://www.neaglegolf.com/golf-simulators/buying-guide/">
```

这是正确的。

---

# 三、OG URL 也已经同步正确

比如 S1：

```html
<meta property="og:url"
content="https://www.neaglegolf.com/golf-simulators/golfpai-s1/">
```

而且产品页已经开始使用独立图片：

```text
/images/S1/0.jpg
```

这一点比之前版本明显好。

---

# 四、现在 URL 架构已经是非常标准的 SEO 架构

目前：

```text
/
├── golf-simulators/
│   ├── golfpai-s1/
│   ├── golfpai-a1/
│   ├── golfpai-x1/
│   ├── rg-ruge/
│   ├── faya-motion/
│   ├── compare/
│   └── buying-guide/
│
├── golf-ball-dispensers/
│   ├── dispenser-machine/
│   └── vending-machine/
│
├── catalog/
│
├── case-studies/
│   ├── clubhouse/
│   ├── lincoln-4s/
│   ├── shanghai-g-town/
│   └── ...
│
└── about/
```

这个结构非常适合：

* Google
* Bing
* ChatGPT
* Gemini
* Perplexity
* Claude
* AI 搜索引擎

因为 URL 本身已经表达了实体层级。

---

# 五、Sitemap 也已经很好

目前 Sitemap 已经包含：

```text
/
golf-simulators/
golf-simulators/golfpai-s1/
golf-simulators/golfpai-a1/
...
golf-simulators/compare/
golf-simulators/buying-guide/
case-studies/
case-studies/clubhouse/
case-studies/lincoln-4s/
...
about/
```

而且有：

```xml
<lastmod>2026-08-25</lastmod>
```

这比之前版本明显成熟。

---

# 六、但 Sitemap 有一个小问题：所有页面都统一 weekly / 0.8

现在：

```xml
<changefreq>weekly</changefreq>
<priority>0.8</priority>
```

几乎全部一样。

这不是严重问题。

实际上 Google 对：

```xml
priority
changefreq
```

并不会给予你想象中的权重。

所以我的建议反而是：

> **不用花太多时间优化 priority。**

真正应该关注的是：

```text
lastmod
```

而且 `lastmod` 最好是真实内容更新时间，而不是每次 build 都统一刷新。

现在：

```javascript
const LASTMOD = new Date().toISOString().slice(0, 10);
```

意味着：

> 每次构建网站，所有页面都变成当天更新。

这个不太理想。

建议以后改成：

```text
页面实际更新时间
```

---

# 七、P0：Case Study 使用 `NewsArticle` Schema 是目前最明显的问题

现在 Case Study：

```javascript
const csSchema = {
  '@context': 'https://schema.org',
  '@type': 'NewsArticle',
  headline: c.title,
  ...
  datePublished: '2025-01-01',
}
```

这个我不建议。

因为这些页面本质上是：

> **Customer Case Study / Project Case Study**

而不是：

> News Article

例如：

```text
Clubhouse Indoor Golf
Lincoln 4S Dealership
Jitang Club
Sushi Omakase
```

这些都是项目案例。

使用：

```json
"@type": "NewsArticle"
```

语义上不准确。

---

# 八、而且 `datePublished: 2025-01-01` 非常值得警惕

所有 Case Study 都写：

```json
"datePublished": "2025-01-01"
```

如果这个日期不是实际发布时间：

> **建议立即删除。**

不要为了 Schema 而制造一个假的发布日期。

GEO 更强调：

> factual consistency

也就是说：

**宁可没有 datePublished，也不要虚构。**

---

# 九、Case Study 更适合改成 `Article` / `WebPage`

例如可以：

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "@id": "https://www.neaglegolf.com/case-studies/clubhouse/#article",
  "headline": "Clubhouse Indoor Golf...",
  "description": "...",
  "image": [
    "..."
  ],
  "author": {
    "@type": "Organization",
    "@id": "https://www.neaglegolf.com/#organization"
  },
  "publisher": {
    "@type": "Organization",
    "@id": "https://www.neaglegolf.com/#organization"
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://www.neaglegolf.com/case-studies/clubhouse/"
  }
}
```

甚至更简单：

```json
{
  "@type": "WebPage"
}
```

都比 `NewsArticle` 更稳妥。

---

# 十、Case Study 目前已经从“列表”升级成了独立页面，这是非常大的进步

现在已经有：

```text
/case-studies/clubhouse/
/case-studies/lincoln-4s/
/case-studies/shanghai-g-town/
/case-studies/in-house/
...
```

而且列表页已经真正链接：

```html
<a href="/case-studies/clubhouse/">
```

这个架构非常好。

---

# 十一、但是 Case Study 内容仍然太薄

目前一个案例页核心内容基本是：

```text
标题
↓
图片
↓
description
↓
一句通用说明
↓
CTA
↓
More Case Studies
```

核心代码：

```html
<p>${c.description}</p>

<p>
This installation demonstrates how NEAGLE GOLF's tour-grade simulation...
</p>
```

这里有一个问题：

> **AI 能知道“这个案例存在”，但还不知道这个案例到底解决了什么问题。**

---

# 十二、GEO 最重要的是把 Case Study 做成“事实数据库”

例如一个案例最好明确：

```text
Client
Location
Facility Type
Project Type
Products Used
Number of Bays
Room Size
Installation Scope
Challenge
Solution
Result
Technology
```

例如：

```text
Project:
Clubhouse Indoor Golf

Location:
Richmond, British Columbia

Facility Type:
Commercial Indoor Golf

System:
GOLFPAI S1

Number of Bays:
6

VIP Rooms:
3
```

这种数据对于 AI 极其有价值。

---

# 十三、你现在其实已经有 `caseStudies` 数据源

这是非常好的。

`build.mjs` 里面：

```javascript
const caseStudies = ...
```

并且每个案例已经有：

```text
id
title
image
description
keywords
```

所以你现在不需要重新做架构。

只需要把数据模型扩充：

```javascript
{
  id,
  title,
  location,
  facilityType,
  products,
  bays,
  projectType,
  challenge,
  solution,
  result,
  description,
  image
}
```

然后 SSG 自动生成。

---

# 十四、这会直接形成 GEO 的“证据层”

你的整个网站就会从：

```text
Product
```

变成：

```text
Product
    ↓
Use Case
    ↓
Installation
    ↓
Customer
    ↓
Location
    ↓
Result
```

这比单纯增加关键词有效得多。

---

# 十五、第二个 P0/P1 问题：产品页有两个 H1

我扫描了所有产品页：

```text
S1 → H1 2
A1 → H1 2
X1 → H1 2
Ruge → H1 2
FAYA → H1 2
Dispenser → H1 2
Vending → H1 2
```

例如 S1：

```text
H1:
GOLFPAI S1 Indoor Golf Simulator
```

另外 embedded specs 中还有：

```text
H1:
GOLFPAI S1 — Indoor Golf Simulator
```

也就是说：

```html
<h1>GOLFPAI S1 Indoor Golf Simulator</h1>
```

之后嵌入的 specs 又出现一个：

```html
<h1>GOLFPAI S1 — Indoor Golf Simulator</h1>
```

---

# 十六、这不属于“SEO 灾难”，但建议修

Google 并不是看到两个 H1 就处罚。

但从语义结构来说：

```text
Page
 └── H1
      └── product identity
```

最好只有一个核心 H1。

建议：

### 页面主 H1

```text
GOLFPAI S1 Indoor Golf Simulator
```

### specs 内部

改成：

```text
<h2>GOLFPAI S1 Specifications</h2>
```

或者干脆：

```text
<h2>Technical Specifications</h2>
```

---

# 十七、这对 GEO 也有帮助

AI 抽取页面主题时：

```text
H1
↓
H2
↓
H3
```

层级越清晰越好。

建议：

```text
H1
GOLFPAI S1 Indoor Golf Simulator

H2
Key Highlights

H2
Specifications

H2
Who Is GOLFPAI S1 For?

H2
How GOLFPAI S1 Works

H2
Installation Requirements

H2
Frequently Asked Questions
```

---

# 十八、产品页目前最大的 GEO 内容缺口：缺少“Best For”

你现在已经有：

```javascript
const useCases = p.useCases
```

最终页面只是：

```text
Private Villas
Premium Clubs
Corporate Showrooms
Luxury Hotels
```

这些是标签。

建议把它们进一步转成自然语言。

例如：

## Who Is GOLFPAI S1 For?

> GOLFPAI S1 is designed for premium residential golf rooms, luxury hotels, golf clubs, corporate showrooms, and commercial indoor golf facilities.

这样 AI 更容易直接引用。

---

# 十九、产品页建议统一增加一个“Quick Answer”

这是我认为非常值得做的 GEO 模块。

例如：

## GOLFPAI S1 at a Glance

> **GOLFPAI S1 is a premium indoor golf simulator featuring 6,000 FPS vision tracking, 4K laser projection, and 110+ photorealistic courses. It is designed for luxury homes, premium golf clubs, hotels, and commercial indoor golf facilities.**

下面再：

```text
Key Highlights
Specifications
```

这类内容非常适合 AI Answer Extraction。

---

# 二十、Product Schema 这一版已经做得不错

现在有：

```json
Product
name
sku
url
description
image
brand
category
offers
price
priceCurrency
itemCondition
availability
seller
```

这已经是比较完整的 Product Schema。

---

# 二十一、但是这里有一个需要确认的业务问题

现在统一写：

```json
"availability": "https://schema.org/PreOrder"
```

这个比上一版 `InStock` 更谨慎，我认为方向是对的。

但是：

> **必须和真实销售状态一致。**

如果网站是：

```text
询价
定制
人工报价
项目制销售
```

那么 `PreOrder` 也未必准确。

如果没有真正的在线预订/预售机制：

**可以考虑不写 availability。**

---

# 二十二、另一个需要注意的问题：价格

代码：

```javascript
price: p.price.replace(/[^0-9.]/g, '')
```

如果页面显示：

```text
$42,516
```

Schema 变成：

```json
"price": "42516"
```

这个没问题。

但如果某些产品：

```text
Contact Us
From $XX
Custom
```

就不能简单转换。

建议产品数据中单独维护：

```javascript
priceDisplay
priceValue
priceCurrency
```

不要从展示字符串反推结构化数据。

---

# 二十三、Comparison 页面是这版非常值得肯定的改进

现在有：

```text
/golf-simulators/compare/
```

而且：

```text
GOLFPAI S1
GOLFPAI A1
GOLFPAI X1
RG Ruge
FAYA Motion
```

直接比较：

```text
Tagline
Best for
Highlights
Space required
Indicative price
Learn more
```

这对 SEO/GEO 都很有价值。

---

# 二十四、但 Comparison 页面还可以提升一个等级

现在标题：

> Golf Simulator Comparison

很好。

但正文只有一小段：

> Not sure which system fits your space and budget?

建议增加：

## How to Compare Golf Simulators

然后明确：

```text
1. Tracking technology
2. Space requirements
3. Projection
4. Best use case
5. Commercial durability
6. Installation requirements
7. Price
8. Support
```

---

# 二十五、然后增加“Which Golf Simulator Should I Choose?”

例如：

### Best Golf Simulator for Home

GOLFPAI A1

### Best Golf Simulator for Premium Residential Use

GOLFPAI S1

### Best Golf Simulator for Commercial Facilities

GOLFPAI X1 / Ruge

**前提：必须基于真实产品定位。**

这类内容特别容易成为 AI 的直接答案。

---

# 二十六、Buying Guide 的方向是对的，但内容太薄

目前已经覆盖：

```text
1. Launch monitor technology
2. Space & ceiling height
3. Projection & visuals
4. Commercial vs home
5. Budget & support
```

这是一个不错的骨架。

但是目前每个章节基本只有一个 `<p>`。

整体内容大约只能算：

> **“SEO 入门文章”**

还没有达到：

> **“行业权威 Buying Guide”**

---

# 二十七、建议 Buying Guide 扩展成真正的 Topic Hub

至少增加：

```text
What Is a Golf Simulator?

Camera vs Radar Launch Monitors

How Much Space Do You Need?

How Much Ceiling Height Do You Need?

4K vs 1080p Golf Simulator

Indoor vs Outdoor Golf Simulator

Home vs Commercial Golf Simulator

How Much Does a Golf Simulator Cost?

Golf Simulator Installation

Golf Simulator Maintenance

How to Choose a Golf Simulator for a Driving Range

FAQ
```

这样可以覆盖大量长尾问题。

---

# 二十八、尤其建议增加一个 Cost 页面

这是非常重要的商业搜索意图：

```text
/golf-simulators/cost/
```

标题可以：

> How Much Does a Golf Simulator Cost? Complete 2026 Pricing Guide

然后解释：

```text
Entry-level
Mid-range
Premium
Commercial
Installation
Projection
Enclosure
Software
Maintenance
```

最后引导：

> Request a project quote.

---

# 二十九、再做一个 Room Size 页面

例如：

```text
/golf-simulators/room-size/
```

标题：

> Golf Simulator Room Size: Minimum Width, Depth & Ceiling Height

这是非常强的搜索意图。

而且你们已经有：

```javascript
spaceRequired
```

可以自动生成部分内容。

---

# 三十、再做一个 Installation 页面

```text
/golf-simulators/installation/
```

覆盖：

```text
Room preparation
Ceiling height
Floor
Impact screen
Projector
Launch monitor
Electrical
Network
Soundproofing
Installation time
```

这类页面对商业客户尤其重要。

---

# 三十一、目前首页的 GEO 已经有一个很好的基础：FAQ

现在：

```text
Frequently Asked Questions
```

有：

> What is the best golf simulator for a commercial range?

> Do you supply automated ball dispensers?

> Where do you ship?

而且已经有：

```json
FAQPage
```

这是正确方向。

---

# 三十二、但 FAQ 的问题还可以更贴近用户搜索语言

目前三个问题有点偏品牌导向。

建议增加：

```text
How much does a commercial golf simulator cost?

What is the best golf simulator for a home?

How much room do I need for a golf simulator?

What is the difference between radar and camera golf simulators?

Can NEAGLE GOLF install a complete golf simulator?

Do you provide golf simulator installation?

Which golf simulator is best for a driving range?

What golf simulator is best for a golf club?
```

---

# 三十三、不过不要在首页塞 30 个 FAQ

建议：

**首页 5～8 个。**

剩余问题分散到：

```text
Buying Guide
Cost Guide
Installation Guide
Comparison
Product pages
Case Studies
```

这就是：

> **GEO Topic Cluster**

---

# 三十四、你的 About 页面目前有一个明显的 GEO 风险

现在有很多非常强的技术声明：

```text
99.9% Trajectory Precision
100,000 strikes
micro-Doppler radar
sub-millimetric
LiDAR
aerospace radar developers
acoustic research physicists
touring professionals
```

这些内容本身非常有价值。

但：

> **如果没有真实可验证的证据，反而可能削弱 E-E-A-T。**

---

# 三十五、建议给这些技术声明增加“证据”

比如：

### 99.9% Trajectory Precision

不要只有：

```text
99.9%
```

可以增加：

```text
Measurement method
Testing environment
Sample size
What is measured
```

例如：

> Tested across X shots under X launch conditions...

当然必须是真实数据。

---

# 三十六、同样：

> 100,000 strikes

最好解释：

```text
100,000 strikes per unit?
100,000 strikes during development?
100,000 test shots?
```

否则 AI 可能无法准确理解。

---

# 三十七、GEO 非常重视“事实粒度”

例如：

```text
Bad:
Tour-grade accuracy.

Better:
The S1 uses a 6,000 FPS vision-based tracking system.

Best:
GOLFPAI S1 uses a 6,000 FPS vision tracking system and is designed for...
```

越具体，AI 越容易引用。

---

# 三十八、Organization Schema 已经不错

目前：

```json
Organization
name
url
description
email
areaServed
contactPoint
telephone
availableLanguage
```

这已经是不错的实体基础。

---

# 三十九、但建议增加真正的品牌 Entity 信息

如果真实存在，可以加入：

```text
logo
sameAs
address
foundingDate
telephone
contactPoint
```

特别是：

```json
sameAs
```

可以加入：

* LinkedIn
* YouTube
* Instagram
* Facebook
* 其他官方品牌页面

**必须是真实官方账号。**

---

# 四十、Organization Logo 这一版需要重点确认

当前源站的 Schema 中如果还是使用：

```text
card_bg_1.jpg
```

作为品牌 Logo：

不推荐。

应该提供真正的：

```text
NEAGLE GOLF logo
```

例如：

```text
/images/brand/neagle-golf-logo.svg
```

---

# 四十一、建议把整个 Schema 从“每页重复”升级为 Entity Graph

目前每页都有：

```text
Organization
WebSite
```

产品页再：

```text
Product
BreadcrumbList
```

这是能用的。

但更好的架构是：

```text
Organization
       │
       ├── WebSite
       │
       ├── Product
       │
       ├── Case Study
       │
       └── ContactPoint
```

统一：

```text
@id
https://www.neaglegolf.com/#organization
```

这样搜索引擎/AI 更容易确认：

> 所有产品、案例都属于同一个品牌实体。

---

# 四十二、还有一个细节：Product 页面出现 2 个 Organization

我扫描发现：

```text
产品页：
Organization × 2
```

Case Study：

```text
Organization × 3
```

这通常是因为：

> 主站 head 已经有 Organization Schema，而嵌入的 specs / case schema 又重复产生。

不是一定有问题，但建议最终统一成一个 JSON-LD `@graph`。

例如：

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "..."
    },
    {
      "@type": "WebSite",
      "@id": "..."
    },
    {
      "@type": "Product",
      "@id": "..."
    },
    {
      "@type": "BreadcrumbList",
      ...
    }
  ]
}
```

结构会更干净。

---

# 四十三、产品页有大量 specs HTML，这一点既是优势也是风险

你的构建器：

```javascript
embedSpecs(p.id)
```

把：

```text
products/
```

下面的完整 specs HTML 嵌进产品页。

优势：

> 产品规格真正出现在服务器生成的 HTML 中。

这是非常好的 SEO/GEO 做法。

---

# 四十四、但要检查 Specs HTML 中是否有：

```text
title
meta
h1
canonical
schema
body
```

因为你只是把：

```html
<body>...</body>
```

嵌入。

如果 specs 原文件内部还有完整文档结构或 Schema：

就容易产生：

```text
重复 H1
重复 Schema
重复语义
```

目前扫描出来的“双 H1”就是这个问题的直接结果。

---

# 四十五、建议最终产品页面保持这个结构

```text
HTML
│
├── Head
│   ├── title
│   ├── description
│   ├── canonical
│   ├── OG
│   └── JSON-LD
│
└── Body
    │
    ├── Breadcrumb
    │
    ├── H1 Product Name
    │
    ├── Quick Answer
    │
    ├── Product Images
    │
    ├── Key Highlights
    │
    ├── Best For
    │
    ├── Specifications
    │
    ├── Installation Requirements
    │
    ├── FAQ
    │
    └── Related Products
```

这是我最推荐的产品 GEO 模板。

---

# 四十六、图片 SEO 当前已经不错

我扫描所有页面：

**图片 Alt 基本全部存在。**

产品页：

```html
alt="GOLFPAI S1 Indoor Golf Simulator"
```

案例页：

```html
alt="Clubhouse Indoor Golf ..."
```

这部分已经达到合格标准。

---

# 四十七、但是图片 Alt 可以更具体

例如现在：

```html
alt="GOLFPAI S1 Indoor Golf Simulator"
```

如果图片是具体场景，可以：

```text
GOLFPAI S1 indoor golf simulator installed in a premium residential golf room
```

如果是技术图：

```text
GOLFPAI S1 golf simulator vision tracking system
```

如果是商业案例：

```text
Clubhouse Indoor Golf commercial simulator installation in Richmond
```

---

# 四十八、不要所有图片都用产品名

否则：

```text
17 images
↓
17 × "GOLFPAI S1 Indoor Golf Simulator"
```

会浪费图片语义信息。

应该根据图片内容分别命名。

---

# 四十九、Hero / LCP 图片还有性能优化空间

我注意到产品卡片：

```html
loading="lazy"
```

这是正确的。

但：

> 首屏最大图片不要 lazy。

建议真正的 LCP 图片：

```html
loading="eager"
fetchpriority="high"
```

其他图片：

```html
loading="lazy"
```

---

# 五十、生产环境仍然不建议继续使用 Tailwind CDN

`build.mjs` 自己就写了：

```text
keeps Tailwind CDN
```

目前还是：

```html
<script src="https://cdn.tailwindcss.com"></script>
```

开发阶段没问题。

正式生产建议改成：

```text
Tailwind CLI
↓
生成 CSS
↓
Purge unused styles
↓
static CSS
```

然后：

```html
<link rel="stylesheet" href="/assets/site.css">
```

---

# 五十一、这是目前性能 SEO 最大的问题之一

因为现在页面加载：

```text
HTML
+
Tailwind runtime
+
FontAwesome
+
Tabler Icons
+
大量 CSS
+
产品 Specs CSS
+
JS
```

尤其产品页因为嵌入 Specs，HTML 也比较大。

---

# 五十二、产品页 HTML 体积值得关注

我扫描到：

```text
S1 ~17 张图片
A1 ~19 张图片
X1 ~17 张图片
Ruge ~19 张图片
```

而且 Specs 内容也直接嵌入。

这对于 GEO 是好事。

但对于性能：

> 有可能过重。

建议：

* 首图 preload
* 其余 lazy
* WebP/AVIF
* width/height
* srcset
* 压缩图片
* CSS 外置
* specs CSS 合并

---

# 五十三、视频现在是点击 Lightbox 才播放，这一点不错

当前：

```javascript
openVideoLightbox()
```

点击后才加载/播放。

这比：

```html
<video autoplay>
```

要好很多。

---

# 五十四、但是视频最好增加 VideoObject Schema

如果产品视频是官方原创内容，可以进一步：

```json
{
  "@type": "VideoObject",
  "name": "GOLFPAI S1 Introduction",
  "description": "...",
  "thumbnailUrl": "...",
  "contentUrl": "...",
  "uploadDate": "..."
}
```

这样：

> Product + Video + Brand

可以形成更完整的内容实体。

前提当然是视频 URL、缩略图、日期等信息真实存在。

---

# 五十五、内部链接结构现在已经不错

例如：

```text
Home
 ↓
Golf Simulators
 ↓
S1
```

以及：

```text
S1
 ↓
A1
X1
Ruge
```

Comparison：

```text
Compare
 ↓
S1
A1
X1
Ruge
FAYA
```

Buying Guide：

```text
Buying Guide
 ↓
Product
```

这是非常好的。

---

# 五十六、下一步应该把内部链接升级成“Topic Cluster”

现在：

```text
Golf Simulators
       ↓
Products
```

建议变成：

```text
Golf Simulators
│
├── Products
│
├── Comparison
│
├── Buying Guide
│
├── Cost Guide
│
├── Room Size
│
├── Installation
│
├── Home Golf Simulator
│
├── Commercial Golf Simulator
│
└── Case Studies
```

这会非常适合 SEO + GEO。

---

# 五十七、建议重点建设这些 URL

我按商业价值排序：

### 1

```text
/golf-simulators/
```

核心 Category Hub

### 2

```text
/golf-simulators/compare/
```

已经有

### 3

```text
/golf-simulators/buying-guide/
```

已经有

### 4

```text
/golf-simulators/cost/
```

强烈建议

### 5

```text
/golf-simulators/room-size/
```

强烈建议

### 6

```text
/golf-simulators/installation/
```

强烈建议

### 7

```text
/golf-simulators/for-home/
```

### 8

```text
/golf-simulators/for-commercial/
```

### 9

```text
/golf-simulators/for-golf-clubs/
```

### 10

```text
/golf-simulators/for-driving-ranges/
```

---

# 五十八、GEO 最核心的页面结构，我建议变成这样

```text
                    Golf Simulators
                          │
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
     Products          Guides            Use Cases
        │                 │                 │
    S1/A1/X1         Buying Guide        Home
    Ruge/FAYA        Cost                Club
                     Room Size            Range
                     Installation         Hotel
                     Comparison           Commercial
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ↓
                    Case Studies
                          ↓
                       Evidence
```

这才是比较完整的 GEO 内容网络。

---

# 五十九、关于首页 H1，我建议暂时不要急着改

现在：

```text
Precision Golf
Simulation, Redefined
```

品牌视觉很好。

从 SEO 角度，它不是最理想的关键词 H1。

但是首页正文已经明确：

> tour-grade golf simulators, launch monitors, 4K golf simulation systems...

所以目前：

**可以接受。**

如果未来想更激进一点，可以：

```text
Golf Simulators & Indoor Golf Systems
```

再配：

> Precision Golf Simulation, Redefined.

但我不会把它列为当前最高优先级。

---

# 六十、首页现在有一个非常好的 SEO/GEO 内容：

```text
One Partner for Golf Simulation & Automation
```

以及：

> NEAGLE GOLF is a global provider of tour-grade golf simulators...

这一段是非常有价值的。

因为它明确回答：

```text
Who?
NEAGLE GOLF

What?
Golf simulators
Launch monitors
4K systems
Ball dispensers

Who for?
Clubs
Ranges
Home studios
```

这是典型 GEO 实体描述。

---

# 六十一、首页的 FAQ 可以继续增强成“直接回答”

比如：

### What is the best golf simulator for a commercial range?

当前回答：

> A ceiling or overhead launch-monitor system...

不错。

但可以进一步：

> For a commercial golf range, the best simulator typically combines overhead launch-monitor tracking, durable enclosure construction, 4K projection, automated ball dispensing, and range-management integration. NEAGLE GOLF provides systems designed around these requirements.

这会更像 AI 可以直接复述的答案。

---

# 六十二、一个非常重要的 GEO 原则：少写“营销形容词”，多写“可验证事实”

目前网站有很多：

```text
tour-grade
absolute apex
ultimate
premium
next-gen
precision
immersive
enterprise
```

这些可以保留。

但是建议逐渐增加：

```text
具体数字
具体产品
具体地点
具体客户
具体安装数量
具体规格
具体技术
具体结果
```

例如：

```text
6 simulator bays
3 VIP rooms
180+ courses
Richmond, BC
4K projection
6,000 FPS
```

这些内容的 GEO 价值远高于：

> premium / next-generation / revolutionary

---

# 六十三、E-E-A-T 建议下一阶段重点做

可以增加：

## Engineering & Technology

讲：

```text
Tracking
Radar
Camera
Projection
Software
Cloud
Automation
```

## Installation Expertise

讲：

```text
Room planning
Structural framing
Sound isolation
Airflow
Electrical
Calibration
```

## Customer Evidence

就是：

```text
Case Studies
```

## Company Identity

就是：

```text
About
Contact
Support
```

这样网站的可信度体系才完整。

---

# 六十四、还有一个非常值得做的页面：Contact

目前主要 CTA：

```text
WhatsApp
Email
```

但建议正式增加：

```text
/contact/
```

页面明确：

```text
NEAGLE GOLF

Sales
service@neaglegolf.com

Phone
+1...

WhatsApp

Global Support

Business Hours

Service Areas
```

这样：

> Brand Entity → Contact Point

会更加完整。

---

# 六十五、另外建议增加一个“FAQ 总页面”

例如：

```text
/faq/
```

集中回答：

```text
Golf Simulator
Launch Monitor
Installation
Room Size
Pricing
Commercial
Home
Ball Dispenser
Shipping
Support
```

首页只放精选 FAQ。

---

# 六十六、现在网站最值得做的不是“继续加关键词”

这一点非常重要。

目前已经有：

```text
golf simulator
launch monitor
4K
ball dispenser
commercial
home
clubs
ranges
```

继续堆：

```text
best golf simulator
best golf simulator company
golf simulator manufacturer
...
```

并不是最优策略。

真正应该做的是：

> **建立实体之间的关系。**

---

# 六十七、最终 GEO 知识图谱建议

最终希望 AI 能理解：

```text
NEAGLE GOLF
│
├── manufactures/supplies
│     │
│     ├── GOLFPAI S1
│     ├── GOLFPAI A1
│     ├── GOLFPAI X1
│     ├── RG Ruge
│     └── FAYA Motion
│
├── provides
│     ├── golf simulator systems
│     ├── launch monitors
│     ├── ball dispensers
│     └── installation/support
│
├── serves
│     ├── homes
│     ├── golf clubs
│     ├── driving ranges
│     ├── hotels
│     └── commercial facilities
│
└── has completed
      ├── Clubhouse
      ├── Lincoln 4S
      ├── Jitang Club
      ├── O'Clock
      └── ...
```

这就是 GEO 的核心。

---

# 六十八、我给你一个明确的优化优先级

## P0 — 上线前建议解决

### ① Case Study Schema

把：

```text
NewsArticle
```

改掉。

同时删除：

```text
datePublished: '2025-01-01'
```

除非是真实日期。

---

### ② 产品页双 H1

Embedded specs 中：

```text
H1
```

改成：

```text
H2
```

---

### ③ 清理重复 Schema

统一：

```text
Organization
WebSite
Product
BreadcrumbList
```

形成一个 JSON-LD Graph。

---

### ④ 检查 Product `PreOrder`

确保与真实销售状态一致。

---

### ⑤ 检查所有强技术声明

尤其：

```text
99.9%
100,000 strikes
sub-millimetric
LiDAR
aerospace radar developers
```

必须保证真实可验证。

---

# 六十九、P1 — 强烈建议

### ⑥ Case Study 丰富数据

增加：

```text
Location
Facility Type
Products
Installation
Bays
Challenge
Solution
Result
```

---

### ⑦ Product 增加：

```text
Quick Answer
Best For
Installation Requirements
FAQ
```

---

### ⑧ Buying Guide 扩充

从现在的 5 个章节扩展成完整 Guide。

---

### ⑨ Comparison 增加：

```text
Best for Home
Best for Commercial
Best for Clubs
Best for Driving Ranges
```

---

### ⑩ 新增：

```text
Cost
Room Size
Installation
```

---

# 七十、P2 — SEO/GEO 增长阶段

建立：

```text
Home
 ↓
Category
 ↓
Product
 ↓
Comparison
 ↓
Buying Guide
 ↓
Use Case
 ↓
Case Study
 ↓
Evidence
```

然后持续增加真实案例。

---

# 七十一、P3 — 性能

最后再处理：

```text
Tailwind CDN
FontAwesome CDN
Tabler CDN
Image optimization
WebP/AVIF
srcset
LCP
CSS extraction
```

这部分对 SEO 也有帮助，但优先级低于内容架构。

---

# 七十二、最终结论

这次这个压缩包，我认为已经**不是“SEO 需要重新做”的网站了**。

现在的架构已经基本正确：

```text
SSG
✓

Clean URLs
✓

Independent pages
✓

Canonical
✓

Sitemap
✓

Robots
✓

Product Schema
✓

Breadcrumb Schema
✓

FAQ Schema
✓

Case Study pages
✓

Comparison page
✓

Buying Guide
✓

Internal linking
✓

Image alt
✓
```

真正的问题已经从：

> **“搜索引擎能不能理解这个网站？”**

变成：

> **“如何让 Google / ChatGPT / Gemini / Perplexity 更愿意把 NEAGLE GOLF 当成高尔夫模拟器领域的权威来源？”**

这两者是完全不同的阶段。

---

## 我认为当前最值得做的 5 件事

如果只让我选 5 个：

**1. 修正 Case Study 的 Schema，删除假的 `datePublished`。**

**2. 消除产品页双 H1，统一页面语义层级。**

**3. 把 Case Study 从“项目介绍”升级为“结构化项目证据”。**

**4. 把 Buying Guide 扩展成完整的 Golf Simulator Knowledge Hub，并新增 Cost / Room Size / Installation。**

**5. 给每个产品增加 `Quick Answer + Best For + Installation Requirements + FAQ`，形成真正的 GEO 产品知识页。**

做到这一步之后，这个网站的 SEO/GEO 就会从现在的：

> **“搜索引擎友好的产品官网”**

进一步升级成：

> **“搜索引擎 + AI 搜索都容易理解、引用和推荐的高尔夫模拟器知识型商业网站”。**

另外，这一版源码的 **SSG + `catalogDb` + `caseStudies` 数据驱动方式非常适合继续做 GEO**。我不建议再改架构，直接在现有 `build.mjs` 上继续扩展即可。
