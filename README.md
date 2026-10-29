# 奶蛙艺术圣殿 · 素材仓库（wallpaper）

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/贡献-指南-green" alt="贡献指南"></a>
  <a href="https://github.com/Nailong-Studio/wallpaper/issues"><img src="https://img.shields.io/github/issues/Nailong-Studio/wallpaper" alt="Issues"></a>
  <a href="assets.json"><img src="https://img.shields.io/badge/资源清单-assets.json-gold" alt="资源清单"></a>
  <a href="https://nailong-studio.github.io/NaiLoong-Universe/"> <img src="https://img.shields.io/badge/交付对象-奶蛙艺术圣殿-FFD700" alt="交付对象"></a>
</p>

> **库房重地，闲人免进——但你是股东，所以请进。**
>
> 本仓库是「奶蛙艺术圣殿」官网与「奶蛙壁纸」插件的唯一供货方。
> 库房只做一件事：把每一张奶蛙图登记在册，配好档案，然后交出去。
> 奶蛙的编制为：黄色、圆润、浅米色腹部、绿色眼圈、灰褐色小爪。不合编制的图不予入库。

**这个仓库是取货窗口，不是展馆。** 这里按分类平铺存放原始素材、机器可读清单与取用直链；
策展、布展、导览、沉浸式浏览都在展示仓 [NaiLoong-Universe](https://github.com/Nailong-Studio/NaiLoong-Universe) 里做。
两边分工固定：库房只管**登记与交付**，展馆只管**讲故事**。

> **香油钱箱在这里**：素材免费拿，快乐不限量。拿完回主仓 [NaiLoong-Universe](https://github.com/Nailong-Studio/NaiLoong-Universe) 点个 ⭐，库房管理员会记住你的工号。

> **想交货？看 [CONTRIBUTING.md](CONTRIBUTING.md)——交货即入股，库房不设试用期。**

---

## 一、库房编制

| 目录 | 存放内容 | 备注 |
|---|---|---|
| `classic/` | 圣典名画系列 | 奶蛙主演的古典名画再创作，原作不参与分红 |
| `laugh-gallery/` | 大笑藏馆 | 全网搜集的大笑奶蛙变体 |
| `emotes/` | 表情收藏 | 表情包、官方姿态、立绘与动图 |
| `poses/` | 姿势立绘 | 3D 奶蛙换装立绘：职业、道具与表情（24 件，MIT） |
| `poses-wall/` | 姿势壁纸 | 3D 立绘合成的 1080×1920 竖屏壁纸（24 件） |
| `mobile/` | 手机壁纸 | 1080×1936 竖屏场景（6 件，MIT） |
| `pet/` | 桌宠动作 | 待机 / 捧腹大笑 / 倾听 / 躺平循环 GIF 与动作帧 |
| `art/` | 艺术场景 | AI 生成的生活场景与艺术脑洞 |
| `hd/` | 高清壁纸 | 桌面圣像，适合长时间凝视 |
| `4k/` | 4K 大图 | 壁纸插件的内置库存 |
| `frames/` | 视频帧图 | 圣影抽帧与竖屏壁纸 |
| `videos/` | 官方圣影 | 巡行、隧道、巡展与原片 |
| `fan-videos/` | 同人短片 | 粉丝二创的场景动画 |
| `audio/` | 音效语音 | 笑声、语音与可用音效 |
| `assets/` | 品牌资产 | 奶蛙 logo 与品牌图 |
| `thumbs/` | 缩略图 | 每件素材的 480px WebP，供索引页与清单使用 |

每件素材配一份同名 `.txt` 档案，内容含：一句话叙事、来源、许可、署名与下架声明。档案不全的素材，按库房规定不予上架。

> **[奶蛙壁纸插件](https://github.com/Nailong-Studio/naiwa-wallpaper)** 从本库取走 211 张可作壁纸的素材（横屏 / 竖屏 / 方形 / 4K / 姿势壁纸）。要换图、改图、加图，都在这个库房办手续，插件那边只管取货，不重复生产。

**什么算「可作壁纸」**：短边 ≥ 720px 的位图，横屏（≥1.5:1）、竖屏（≤0.72:1）、近方形各成一组；纯表情小图、桌宠帧序列、音视频不入壁纸包。

---

## 二、档案与清单

- **`assets.json`**：全库机器可读清单——分类、标题、叙事、类型、体积、尺寸、原图直链与缩略图路径。官网「圣物全图鉴」、壁纸插件与第三方项目均以此为准。
- **`thumbs/`**：每件素材的 480px WebP 缩略图；音频则生成波形图。用于总览页，避免为了看一眼而搬运整仓原图。
- **`SOURCES.md`**：来源、许可与排除名单。每批入库都有据可查，不搞口头承诺。
- **重新生成**：`python3 scripts/build_assets.py`；**只校验**：`python3 scripts/build_assets.py --check`；**同步到官网**：`python3 scripts/build_assets.py --site ../NaiLoong-Universe/docs`。
- **`Assets Check` CI**：素材、清单或脚本有变动时自动核对数量、分类、缩略图完整性与孤儿文件。库房不养闲文件。

---

## 三、命名法

- 统一前缀：`奶蛙-`。官方旧名「奶龙」字样全部替换为「奶蛙」，库房不留旧账。
- 系列内按语义或序号命名：`奶蛙-弯腰大笑.png`、`奶蛙-表情-01.jpeg`、`奶蛙-艺术-01.png`。
- 视频帧图保留原秒数标记：`奶蛙-帧图-最伟大的奶蛙-05s.png`。
- 中文语义优先。文件名要能让三个月后的你一眼认出，而不是打开才知道。

---

## 四、影像档案

| 文件 | 说明 |
|---|---|
| `videos/奶蛙-圣殿巡行.mp4` | 官方圣影 · 一：巨型奶蛙缓步巡行圣殿（重构版，替换旧版游动形象） |
| `videos/奶蛙-壁纸隧道.mp4` | 官方圣影 · 二：壁纸隧道 |
| `videos/奶蛙-大笑藏馆巡展.mp4` | 巡展圣影 · 三：Ken Burns 大笑藏馆巡展 |
| `videos/奶蛙-大笑.mp4` | 圣影素材：连续大笑原片，裸片，可直接二次剪辑 |

**同人短片（`fan-videos/`）**

| 文件 | 说明 |
|---|---|
| `fan-videos/奶蛙-西斯廷奶蛙.mp4` | 粉丝二创：奶蛙群像巡游西斯廷穹顶 |
| `fan-videos/奶蛙-宿舍熄灯后.mp4` | 粉丝二创：熄灯后的奶蛙宿舍夜生活 |

---

## 五、许可与责任

- 代码、清单与脚本以 **MIT** 发布；每件素材的来源与许可在各自 `.txt` 与 `SOURCES.md` 中逐条登记。
- 只收**许可明确允许再分发**的素材。许可不明、只许可代码不许可美术、或与本仓协议不兼容的来源，一律登记为「已勘察，未入库」。
- 奶蛙是民间二创形象，角色原型权利归原权利人。若你是权利人并认为某件不宜收录，请开 Issue，库房会在核实后第一时间下架，不辩论。

---

## 六、入库流程

1. 先搜一遍库房，确认没有重复。库房最忌讳一货两单。
2. 按命名法改名，配同名 `.txt` 档案（叙事、来源、许可、署名）。
3. 提 PR，说明来源与授权依据。
4. CI 自动核对清单与缩略图；通过后由管理员验收。
5. 主仓官网与插件会在下一次同步时取货，你不需要手动通知它们。

---

## 变更记录

- v2.7：新增桌宠动作分类；补齐循环 GIF 与透明缩略图生成；第二批同人素材入库。
- v2.6：建立 `assets.json` 与 `thumbs/` 制度，官网图鉴接入。
- v2.5：全仓命名规范化，修正伪动图，补齐配套档案。
- v2：全仓重命名「奶龙 → 奶蛙」，按系列分目录，每件素材配套档案；旧版游动形象开场视频退休，由「圣殿巡行」接任。

---

<div align="center">

**库房长明，欢迎交货。**

拿图请随意，[点星](https://github.com/Nailong-Studio/NaiLoong-Universe) 请顺手。

</div>
