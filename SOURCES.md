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
| [GeorgeNaNN/nailong-memes](https://github.com/GeorgeNaNN/nailong-memes) | MIT | 内容为官方奶龙表情包，不符合“奶蛙”形象要求 |
| 官方奶龙素材 | 版权保留 | 按要求不收录官方素材 |

## 审核建议

- 本批按分类拆分 commit：`laugh-gallery` / `emotes` / `art` / `fan-videos` / `audio`，可逐类审阅。
- 每件素材的同名 `.txt` 末尾均有来源、许可与下架声明。
- `python3 scripts/build_assets.py --check` 可在本地复核 263 件素材、分类计数与缩略图完整性。
