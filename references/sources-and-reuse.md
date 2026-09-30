# 来源、复用判断与边界
查阅日期：2026-09-30。上游固定快照：[`m-esm/3d-print-modeling`](https://github.com/m-esm/3d-print-modeling/tree/0bd303f67552534c2a3d42650932a85251a7d3a3)。
当前快照含 1 个 SKILL.md、9 个 references、12 个 scripts。目录清单及相关主入口/脚本已核对；没有将上游项目案例、兼容性或测试结论移植为本包证据。

| 来源模块 | 判断 | 本包处理 |
|---|---|---|
| SKILL.md | 修改后复用思想 | 创意→验证→发布流程重写，去掉机械项目默认与自动 commit |
| design-rules-checklist / fdm-design-rules | 修改后复用 | 融入 printer/material-aware DfAM |
| numeric-verify | 直接借鉴思路 | invariant 与可追溯输入；不复制脚本实现 |
| mechanisms-and-fits / assembly-verification | 修改后复用 | 聚焦纯打印配合，去除硬件特化 |
| slicer-style-cut | 修改后复用 | 分件、观察切面与制造源区别 |
| csg-robustness | 按需原则 | backend 中保留几何有效性，不新增复杂布尔库 |
| components-verified | v0.1 不需要 | 外购件纳入 TBC，不带作者硬件尺寸表 |
| hard-won-patterns | 不直接复用 | 作者机械案例不作为本用户普适规则 |
| shoot / GLB/STL viewers / wallcheck | 需改造 | 本包显式 scaffold，未来本地/跨平台验证 |
| checks_template | 直接借鉴思想 | 新写外部测量范围检查器 |
| assembly_check | 修改后实现 | 仅新写 AABB 筛查，不移植完整引擎 |
| fitmap / parts_viewer / stlpaths / serve / Makefile / requirements | 不直接复用 | v0.1 无此运行链，避免隐式依赖 |
| Creative / PETG / Bambu / prototype / MakerWorld | 我们新增 | 当前目标专用参考与 gate |
| slice_check / render_beauty / release_check | 我们新增 | 有限证据检查与 beauty scaffold |

没有直接复制上游代码或大段正文；随包保留上游 MIT notice 以清楚标识来源，不能据此推断上游为本包背书。

## 外部事实与未来接入时应复核的官方来源
- [Bambu Studio CLI](https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage)：CLI 入口参考；本包不承诺某版参数。
- [Bambu filament guide](https://cdn1.bambulab.com/filament/filament-guide/wksdyyzd8n9/filament-guide-en.pdf) 与 [PETG HF](https://bambulab.cn/zh-cn/filament/petg-hf)：具体耗材参考，不能泛化到全部 PETG。
- [trimesh quick start](https://trimesh.org/quick_start.html)：未来网格加载/检查参考；本包不运行 trimesh。
- [build123d docs](https://build123d.readthedocs.io/)、[CadQuery docs](https://cadquery.readthedocs.io/)、[Blender manual](https://docs.blender.org/manual/en/latest/)、[Playwright Python](https://playwright.dev/python/docs/intro)、[Plasticity](https://www.plasticity.xyz/)：未来接入时核查版本/安装/API；此次未验证集成。
- [MakerWorld](https://makerworld.com/)：发布时核查当前规则和表单；本次直接读取 community-guidelines 页面失败，**没有核实全部当前发布规范**。本包 release checklist 为内部标准，不假装是平台强制清单。
