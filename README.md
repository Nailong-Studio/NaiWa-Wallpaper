# 奶蛙艺术圣殿 · 素材仓库（wallpaper）

<p align="center">
  <a href="https://github.com/Nailong-Studio/wallpaper"><img src="https://img.shields.io/badge/素材总数-247-gold" alt="素材总数"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/贡献-指南-green" alt="贡献指南"></a>
  <a href="https://github.com/Nailong-Studio/wallpaper/issues"><img src="https://img.shields.io/github/issues/Nailong-Studio/wallpaper" alt="Issues"></a>
  <a href="assets.json"><img src="https://img.shields.io/badge/资源清单-assets.json-gold" alt="资源清单"></a>
</p>

> 本仓库为「奶蛙艺术圣殿」官网（[NaiLong-Universe](https://github.com/Nailong-Studio/NaiLong-Universe)）的全部素材源。
> 奶蛙为官方奶龙角色的民间 AI 变异体：黄圆润 / 浅米腹 / 绿眼 / 灰爪。本仓素材统一以「奶蛙」命名。
> **香油钱箱在这里**：素材免费拿，快乐不限量。看完全仓觉得不错，回主仓 [NaiLong-Universe](https://github.com/Nailong-Studio/NaiLong-Universe) 点个 ⭐ 再走，奶蛙会记住你的。

> **想贡献素材？看 [CONTRIBUTING.md](CONTRIBUTING.md)——交了素材就是圣殿股东。**


## 目录结构

| 目录 | 内容 | 数量 |
|---|---|---|
| `classic/` | 圣典名画系列（奶蛙主演的古典名画再创作） | 38 |
| `laugh-gallery/` | 大笑藏馆（全网搜集大笑奶蛙变体） | 22 |
| `emotes/` | 表情收藏（奶蛙表情包 + 官方姿态 + 立绘/动图） | 67 |
| `art/` | 艺术场景图（AI 生成，奶蛙生活场景/艺术脑洞） | 47 |
| `hd/` | 高清表情壁纸 | 22 |
| `4k/` | 4K 大图（新标签页插件内置素材） | 5 |
| `frames/` | 视频帧图（最伟大的奶蛙 / 孤独奶蛙主义 抽帧） | 38 |
| `videos/` | 官方圣影视频（圣殿巡行 / 壁纸隧道 / 大笑藏馆巡展 / 大笑原片） | 4 |
| `fan-videos/` | 同人短片（粉丝二创场景动画） | 2 |
| `audio/` | 音效语音（奶蛙笑声与可用音效） | 1 |
| `assets/` | 品牌资产（奶蛙 logo） | 1 |

合计：247 件素材文件，每件配套同名 `.txt` 描述（与官网展厅叙事一致）。

> `4k/` 系列的 5 张大图同时是 **[奶蛙壁纸插件](https://github.com/Nailong-Studio/naiwa-wallpaper)** 的内置素材（仓库根目录即扩展本体，`chrome://extensions` 加载解压目录即可）。要换图、改图、加图，都在这个素材仓库做，插件侧只管取用。

## 资源清单与缩略图

- **`assets.json`**：全仓 247 件素材的机器可读清单——分类、标题、叙事、类型、体积、尺寸、原图直链与缩略图路径，供官网「圣物全图鉴」、壁纸插件与第三方项目直接取用。
- **`thumbs/`**：每件素材对应的 480px WebP 缩略图（音频为波形图），官网以它做素材总览，避免加载数百 MB 原图。
- **`SOURCES.md`**：收录素材的来源、许可与排除清单；本次同人素材批次均可追溯。
- 重新生成：`python3 scripts/build_assets.py`；只校验：`python3 scripts/build_assets.py --check`；同步到官网：`python3 scripts/build_assets.py --site ../NaiLong-Universe/docs`。
- GitHub Actions 会在素材、清单或脚本变更时自动运行 `Assets Check`，保证清单、缩略图与实际文件一致。

## 命名规范

- 统一前缀：`奶蛙-`；官方旧名「奶龙」字样全部替换为「奶蛙」。
- 系列内按语义/序号命名：`奶蛙-弯腰大笑.png`、`奶蛙-表情-01.jpeg`、`奶蛙-艺术-01.png`。
- 视频帧图保留原秒数标记：`奶蛙-帧图-最伟大的奶蛙-05s.png`。

## 视频

| 文件 | 说明 |
|---|---|
| `videos/奶蛙-圣殿巡行.mp4` | 官方圣影 · 一：巨型奶蛙缓步巡行圣殿（重构版，替换旧版游动形象） |
| `videos/奶蛙-壁纸隧道.mp4` | 官方圣影 · 二：壁纸隧道 |
| `videos/奶蛙-大笑藏馆巡展.mp4` | 巡展圣影 · 三：Ken Burns 大笑藏馆巡展 |
| `videos/奶蛙-大笑.mp4` | 圣影素材：15.4 秒连续大笑原片（裸片，可直接二次剪辑） |

**同人短片（`fan-videos/`）**

| 文件 | 说明 |
|---|---|
| `fan-videos/奶蛙-西斯廷奶蛙.mp4` | 粉丝二创：奶蛙群像巡游西斯廷穹顶 |
| `fan-videos/奶蛙-宿舍熄灯后.mp4` | 粉丝二创：熄灯后的奶蛙宿舍夜生活 |

## 变更记录

- v2（2026-09-24）：全仓重命名「奶龙→奶蛙」；按系列分目录；每件素材配套 txt 描述；删除旧版游动形象开场视频（`promo/nailong-hero.mp4`），以「圣殿巡行」重构版替代。
