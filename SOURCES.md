# 素材来源与许可

本文件记录 2026-10「同人素材批次」的调研、收录与排除依据。奶蛙是民间二创形象；本批素材只从**许可证明确允许再分发**的开源仓库收录，并在每件素材的同名 `.txt` 中保留来源与许可。角色原型权利仍归原权利人，如权利人认为不宜收录，请开 Issue，我们会下架。

## 第二批 · 桌宠动作包（16 件）

| 来源仓库 | 许可 | 收录数量 | 许可依据 |
|---|---|---|---|
| [liaosongjie/Codex-Voice-Input](https://github.com/liaosongjie/Codex-Voice-Input) | **MIT** | 14 件（10 PNG 动作帧 + 4 循环 GIF） | `assets/pet/ASSET-NOTICE.md`：奶蛙源视频、动画与笑声由作者原创，派生动画帧与 `sounds/laugh.wav` 以 MIT 分发 |
| [woainiunai/milk-frog-desktoppet](https://github.com/woainiunai/milk-frog-desktoppet) | **MIT** | 1 件 1024×1536 立绘 | 仓库 LICENSE 为 MIT，README 与 LICENSE 均未对 `assets/` 作额外限制 |
| liaosongjie/Codex-Voice-Input | **MIT** | 1 件 `audio/`（1.8s 笑声 WAV） | 同上 `ASSET-NOTICE.md` 明确 `sounds/laugh.wav` 以 MIT 分发 |

- 新增分类：`pet/`「桌宠动作」——由 19 / 25 / 22 / 8 张动画帧合成的待机、捧腹大笑、倾听、躺平四态循环 GIF，以及每态 2 张透明动作帧。
- GIF 以调色板索引 255 标记透明，缩略图沿用源帧透明通道；`scripts/build_assets.py` 同步修正了 GIF 透明缩略图转 RGB 丢通道的问题。
- 精确去重：本批 16 件与仓库既有 247 件做 Git blob SHA1 比对，0 重复。
- 许可复核淘汰：`syydaniel/naiwa-beyond`（`images/` 声明 all rights reserved）、`hedong433664/naiwa-pet`（素材派生自本仓库，无新增）、`jiasjdia/naiwa`、`hardworkingwhale/naiwa`（无许可 / 保留所有权利）均未收录。

## 第一批 · 同人素材（32 件）

| 来源仓库 | 许可 | 收录数量 | 许可依据 |
|---|---|---|---|
| [Maple498/nai-wa-codex-pet](https://github.com/Maple498/nai-wa-codex-pet) | **CC BY 4.0** | 4 件 GIF | `ASSET-LICENSE.md`：本项目制作的像素动画与预览资产采用 CC BY 4.0，要求署名 |
| [sandytruant/codex-pet-naiwa](https://github.com/sandytruant/codex-pet-naiwa) | **MIT** | 4 件 GIF | README：代码和宠物素材以 MIT License 开源 |
| [TarelX/Milk-Frog](https://github.com/TarelX/Milk-Frog) | **MIT** | 12 件 PNG | `NOTICE.md`：代码、角色设计、动画帧、道具图与设计文档统一 MIT，作者 Ti |
| [WencueCryforme/NaiWa-Universe](https://github.com/WencueCryforme/NaiWa-Universe) | **MIT** | 9 图 + 2 短片 + 1 音频 | README/LICENSE：仓库 MIT；`COPYRIGHT` 声明奶蛙为粉丝二创形象，不属于任何个人 |

> 注：Wencue 的两段同人短片原声可能包含第三方音乐/音效，其权利未单独核实；如权利人异议，我们会下架对应文件。

### 分类明细

| 分类 | 数量 | 来源 |
|---|---|---|
| `laugh-gallery/` | 2 | WencueCryforme（仰头捧腹大笑、拍墙大笑） |
| `emotes/` | 18 | Maple498 4、sandytruant 4、TarelX 7、WencueCryforme 3 |
| `art/` | 9 | TarelX 5（打盹/看书/记笔记/捧杯/泡泡浴）、WencueCryforme 4（思索/雨夜/喝奶茶/背书包） |
| `fan-videos/` | 2 | WencueCryforme（西斯廷奶蛙、宿舍熄灯后） |
| `audio/` | 1 | WencueCryforme（奶蛙爆笑原声） |


## 第三批 · 3D 立绘与竖屏场景（30 件，2026-10）

官方站 milkyfrog.com 为设计师李想的商业站点，页脚为「© 2026 naiwa · 保留所有权利」，全站未提供素材包、
未开放任何仓库、未给出素材授权条款，因此**不抓取、不收录**。本批只从许可证明确的开源仓库收录。

| 来源仓库 | 许可 | 收录数量 | 许可依据 |
|---|---|---|---|
| [66970010-boop/frog-miner](https://github.com/66970010-boop/frog-miner) | **MIT** | 24 件 3D 姿势立绘（`poses/`） | 仓库 `LICENSE` 为 MIT，`Copyright (c) 2026 66970010-boop (original author of frog-miner)`；README 的 Contributors 明示作者负责游戏创意、美术与核心实现 |
| [junjunya2020/nailegewa](https://github.com/junjunya2020/nailegewa) | **MIT** | 6 件 1080×1936 竖屏场景（`mobile/`） | 仓库 `LICENSE` 为 MIT，`Copyright (c) 2026 junjunya2020` |

### 派生作品

| 产物 | 数量 | 说明 |
|---|---|---|
| `poses-wall/` | 24 件 | 以 `poses/` 的 3D 立绘为主体，本仓库加渐变背景与主体辉光合成的 1080×1920 竖屏壁纸；立绘权利仍按上游 MIT 处理 |

### 为什么只收这两个仓库

- 三消类 `nailegewa` 与挖矿类 `frog-miner` 是 GitHub 上仅有的两个「MIT + 含成规模奶蛙美术」的仓库；
- 其余奶蛙相关仓库要么无 LICENSE（`yhsome/BigNaiWa`、`yhsome/Nai2048`、`yhsome/SmallNaiWa`、
  `22hewang/naiwa-ultimate`、`LynnShaw/naiwa-pet`），要么 GPL（`CHENGONGSHUO/Naiwa`、
  `SbongeBobybl/NaiWaChatPet`），与本库 MIT 授权不兼容；
- 官网与 App Store 素材为商业版权，全部不收录。

## 第四批 · 3D 动画帧与立绘（68 件，2026-10-31）

本轮把检索面扩到 GitHub 全站 28 组关键词（243 个去重仓库）、Gitee、GitCode、npm，逐个核验许可证范围。

| 来源仓库 | 许可 | 收录数量 | 许可依据 |
|---|---|---|---|
| [lin-alg/NaiLoong](https://github.com/lin-alg/NaiLoong) | **MIT** | 65 帧动画 + 2 张立绘 + 1 张场景 | `LICENSE` 为 MIT；README「项目中的图片可以随意使用吗」明确：**本仓库自带的图片可随意使用，仅需注明来源** |

### 本批详情

| 分类 | 数量 | 内容 |
|---|---|---|
| `pet/` | 65 | 3D 奶蛙 10 组动画逐帧：待机 6 / 行走 8 / 奔跑 8 / 招手 4 / 进食 5 / 蹲伏 8 / 思考 6 / 鼓掌 6 / 张望 6 / 沮丧 8 |
| `emotes/` | 2 | 512×512 立绘：叉腰、奶蛋 |
| `art/` | 1 | 栅栏与蓝天场景（888×1240） |

原始 sprite sheet 为 1536×2080 的 10 行图集，本库按动画行切分并保留透明通道。

### 本轮排除清单（附理由）

| 来源 | 许可 | 排除原因 |
|---|---|---|
| `chromoany/naiwa-icons` | CC BY-NC-SA 4.0 | 禁商用，与本库 MIT 再分发条款不兼容（71 枚 1024×1024 图标因此未收） |
| `hardworkingwhale/naiwa` | All rights reserved | LICENSE 明确禁止复制/再分发/单独转载，仅允许下载原版游玩 |
| `Jinxw03/Dounai-art-convertor-skill` | 自定义非商用 | LICENSE.md 禁止商用、广告、周边等一切变现用途 |
| `busgm666-cloud/naidan-slingshot` | 代码 MIT / 美术非 MIT | `NOTICE` 明确 `assets/*.png` 不在 MIT 范围，且立绘来自本库，无新增价值 |
| `2002yxy/dsh-nailong-desktop-pet` | MIT | 素材是 DeepSeek 鲸鱼形象，不是奶蛙 |
| `waverlose/NAIWA-cursors` | MIT | 仓库内仅 1 张预览图，无独立素材文件 |
| `xinxiangchen/nailong-mode` | MIT | 只有界面截图，无独立美术素材 |
| `Swordmynew/naiwa-petdex` | MIT | README 声明角色形象权利可能归第三方，仅 `qa/` 校验图，无成片素材 |
| `Trafalgar2000/naiwa-desktop-pet` | 代码 MIT / 素材另行声明 | `ASSETS-NOTICE.md` 明确 assets 不在 MIT 范围 |
| `naiwa.world`（奶蛙档案馆） | — | 站点已 404，无法访问 |
| Gitee / GitCode / npm | — | 检索无有效奶蛙素材仓库（Gitee 0 条；GitCode 需 token；npm 仅 3 个插件包，无可提取素材） |

## 去重与筛选

- **精确去重**：将每件候选文件计算 Git blob SHA1，与 wallpaper `main` 全量 215 件比对。
- **近似去重**：对候选图/GIF 首帧/视频首帧计算 dHash，与官网 215 张缩略图比对；近距离重复人工复核。
- 本批剔除 3 件重复：
  - `奶蛙捧腹大笑.gif` 与仓库既有 `emotes/奶蛙-表情-21.gif` 字节一致；
  - `奶蛙站立歪头杀.jpg` 与既有 `laugh-gallery/奶蛙-静站绿眼` 画面高度重复；
  - `奶蛙爆笑.mp4` 与既有 `videos/奶蛙-大笑.mp4` 画面高度重复。
- 所有入选图均人工检查形象：黄圆润身体、浅米色肚腹、绿眼、灰爪；排除官方奶龙、异色变体、带文字/水印或构图不符的素材。

## 调研但未收录的来源

| 来源 | 许可状态 | 排除原因 |
|---|---|---|
| [Trafalgar2000/naiwa-desktop-pet](https://github.com/Trafalgar2000/naiwa-desktop-pet) | 代码 MIT | `ASSETS-NOTICE.md` 明确 `assets/` 角色图片不在 MIT 范围 |
| [Swordmynew/naiwa-petdex](https://github.com/Swordmynew/naiwa-petdex) | 代码/文件 MIT | README 声明角色形象权利可能归第三方，未给出素材授权 |
| [mosterpath/pet-nailong](https://github.com/mosterpath/pet-nailong) | 代码 MIT | 素材多为收集的参考图，含“原版笑声”，来源与授权不明确 |
| [wangyiding645/nailong-assistant](https://github.com/wangyiding645/nailong-assistant) | 代码 MIT | README 注明动画/音效来自“奶蛙素材库”，未给出可再分发许可 |
| [Theorists258/naiwa-studio](https://github.com/Theorists258/naiwa-studio) | 代码 MIT | README 明确第三方 MP3 不包含在 MIT 授权内 |
| [CHARKJIL/milk-frog-desktop](https://github.com/CHARKJIL/milk-frog-desktop) | 代码 MIT | `ASSETS.md` 明确角色与 PNG/GIF/MP4 等美术素材不在 MIT 范围 |
| [AkaCMD/naifrog-desktop-pet](https://github.com/AkaCMD/naifrog-desktop-pet) | 代码 MIT | 精灵图来自上游 Zhengyici，音效来自 Tomorins 且被其许可限制 |
| [timerring/codex-pet-naiwa](https://github.com/timerring/codex-pet-naiwa) | 代码 MIT | Credits 指向的预览素材来自第三方，不在 MIT 授权内 |
| [busgm666-cloud/naidan-slingshot](https://github.com/busgm666-cloud/naidan-slingshot) | 代码 MIT | `NOTICE` 明确角色美术不在授权范围，且立绘来自其他仓库 |
| [wjc129/naiwa-desktop-pet](https://github.com/wjc129/naiwa-desktop-pet) | 代码 MIT | README 要求再分发 `奶娃.gif` 时自行取得使用权 |
| [LIN4RUN/naiwa-desktop-pet](https://github.com/LIN4RUN/naiwa-desktop-pet) | 代码 MIT | 含“原版笑声”音频，官方音源权利不明确 |
| [waverlose/NAIWA-cursors](https://github.com/waverlose/NAIWA-cursors) | MIT | 光标预览未通过内容核验，本批暂不收录 |
| [yugh6/Naiwa](https://github.com/yugh6/Naiwa) | 无许可证 | 无法确认再分发授权 |
| [CHENGONGSHUO/Naiwa](https://github.com/CHENGONGSHUO/Naiwa) | GPL-3.0 | 与本仓库 MIT 素材授权不兼容 |
| [SbongeBobybl/NaiWaChatPet](https://github.com/SbongeBobybl/NaiWaChatPet) | GPL-3.0 | 与本仓库 MIT 素材授权不兼容 |
| [22hewang/naiwa-ultimate](https://github.com/22hewang/naiwa-ultimate) | 无许可证 | 无法确认再分发授权 |
| [LynnShaw/naiwa-pet](https://github.com/LynnShaw/naiwa-pet) | 无许可证 | 无法确认再分发授权 |
| [DylanShek/naiwa-for-codex](https://github.com/DylanShek/naiwa-for-codex) | 无许可证 | 无法确认再分发授权 |
| [lyhkevin/Codex_pet_naiwa](https://github.com/lyhkevin/Codex_pet_naiwa) | 无许可证 | 无法确认再分发授权 |
| [GeorgeNaNN/nailoong-memes](https://github.com/GeorgeNaNN/nailoong-memes) | MIT | 内容为官方奶龙表情包，不符合“奶蛙”形象要求 |
| 官方奶龙素材 | 版权保留 | 按要求不收录官方素材 |

## 审核建议

- 本批按分类拆分 commit：`laugh-gallery` / `emotes` / `art` / `fan-videos` / `audio`，可逐类审阅。
- 每件素材的同名 `.txt` 末尾均有来源、许可与下架声明。
- `python3 scripts/build_assets.py --check` 可在本地复核 263 件素材、分类计数与缩略图完整性。
