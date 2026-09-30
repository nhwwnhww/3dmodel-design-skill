# Validation report — v0.1

执行日期：2026-09-30（Australia/Brisbane）。环境：Windows / Python 3.12.7。

## 已执行
- `python -m unittest discover -s tests -v`：26 项通过。覆盖缺失 gate、源文件/配置变更、旧 revision、缺失截面/视角、原型未知、切片器不符、hash 错误、路径越界、行为缺少专属实测、证据角色缺失、切片范围检查、数值不满足/NaN/空集合以及 AABB 三类结果。
- Skill creator `quick_validate.py`：`Skill is valid!`（结构/frontmatter 检查，不代表模型能力）。
- 18 项 CLI 冒烟检查：7 个 Python 工具的 `--help`；3 个 scaffold 默认退出 2；4 个空项目模板按约定失败；4 个不存在输入文件返回 2。
- 全部 Python 文件语法解析通过。用户要求的 21 个入口/专题/模块/脚本文件存在。
- Markdown 本地链接与最终 ZIP 的文件/hash 一致性由打包步骤核查。

## 行为试用
独立 agent 在不加载 Skill 时已拒绝无证据的 ready-to-print / snap-works 声明；未观察到该项基线失败，不能声称本 Skill 使这项行为从失败变成功。
加载 Skill 后的两种模拟场景正确识别：缺 Bambu 和实测只能交付待验证草稿；磁铁属于 TBC；r1 卡扣在 r2 几何和材料变化后不可直接沿用旧结论。独立审阅发现旧 physical gate 继承和发布授权的表述歧义，已修订为明确的 v0.1 规则，独立复核确认两处歧义均已消除。
这是有限场景试用，不是大量样本成功率或真实打印验证。

## 未执行 / 不保证
- 未安装或运行 build123d、CadQuery、trimesh、Playwright/Chromium；未运行 Blender、Plasticity 或 Bambu Studio。
- 无真实模型 build、mesh QA、七视图/截面渲染、真实壁厚、精确碰撞、真实切片、物理打印或 MakerWorld 上传测试。
- HTML 文件是明确的 scaffold 状态页，未测试模型显示功能，因为没有该实现。
- 未测试 ChatGPT 原生 ZIP 安装、Codex 安装后的自动发现、macOS/Linux 运行。
- MakerWorld 全部当前规则未核实；发布时仍需核对。
- 通过测试仅说明有限脚本行为和指令结构符合本包契约；不表示某件作品已 ready to print 或 works。

## 测试证据边界
回归测试使用临时合成文本文件及标注为 fixture 的字段，目的是验证文件/记录一致性。它们不是 3MF、照片或物理成功证据，也不能交给真实作品复用。校验器不解析文件内容，必须配合人工/代理审阅。包内项目模板全部保持 unknown 或空，正常情况下应被阻止通过。

运行时脚本不写模型、证据或配置，不自动联网/安装/发布。额外依赖安装和未来 adapter 的行为不在本次验证范围内。
