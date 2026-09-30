# MakerWorld Design Studio v0.1

面向原创 MakerWorld 创意作品的 ChatGPT/Codex Skill；默认 P1S、0.4 mm、PETG，支持替换项目配置。此包是工作流、参考文档、证据校验器与明确标记的自动化骨架，**不是已经打通的自动建模/渲染/切片软件**。

**Hard rule：没有真实 build + 多视角/section 检查 + Bambu Studio slicer verification，不得声称 “ready to print”；涉及 fit/snap/press/mechanism，没有对应 physical test 不得声称 “works”。**

## 从 GitHub 安装到 Codex

```text
git clone https://github.com/nhwwnhww/3dmodel-design-skill.git makerworld-design-studio
```

将仓库文件夹放入 `~/.codex/skills/makerworld-design-studio`（不要覆盖已有版本），然后在新会话中调用 `$makerworld-design-studio`。无需安装可选 CAD/渲染依赖即可阅读流程与运行证据检查器。

## 使用
- Codex：将整个 `makerworld-design-studio` 文件夹复制到本机技能目录（通常为 `~/.codex/skills/`），避免覆盖同名现有版本；在能发现该技能的新会话中调用 `$makerworld-design-studio`。本交付未替你安装。
- ChatGPT：此 ZIP 提供可移植指令与资源，不保证每个 ChatGPT 界面支持原生 Skill ZIP 安装。可上传 ZIP/解压文件并要求读取 SKILL.md；执行脚本依赖当前会话是否具备文件和 Python 工具。未验证原生安装兼容性。
- 项目中复制 `assets/project-template/`，按 [项目契约](references/project-contract.md) 填写 spec、manifest 和证据；不要把示例状态改为 passed 来绕过验证。
- 当前可执行工具只用 Python 标准库，建议 Python 3.10+，本机测试版本见 VALIDATION。运行位置为本 Skill 根目录：

```text
python -m unittest discover -s tests -v
python scripts/release_check.py /absolute/project/manifest.json
python scripts/slice_check.py /absolute/project/manifest.json
python scripts/assembly_check.py /absolute/project/bounds.json
python scripts/checks_template.py /absolute/project/measurements.json
```

退出码 0 只表示该脚本明确限定的检查通过；1 表示记录/检查失败；2 表示 scaffold、依赖缺失或输入错误。release 检查器成功也不能自动授予可打印/可用结论。

## 文件地图
- `SKILL.md`：入口、流程、证据与声明边界。
- `references/`：10 个指定专题，另有项目契约与来源/复用说明。
- `modules/tbc/bought-components.md`：外购件未来契约，无 v0.1 实现。
- `scripts/`：9 个指定文件、工具说明及 Python 依赖说明。
- `assets/project-template/`：spec、manifest 和数值/包围盒输入模板。
- `tests/`：证据失效、缺失、越界路径与包围盒分类回归测试。
- `VALIDATION.md`：实际执行的测试、未验证的外部集成和兼容性边界。

## 依赖与影响
本包不会安装依赖、联网发布、启动打印机或改动配置。可执行脚本只读项目文件、向终端输出 JSON；写入报告须由调用者自行重定向。Windows 使用 `python`，macOS/Linux 可能需 `python3`，路径须按本机调整。没有在 macOS/Linux 上执行过测试。

可选环境应在独立 venv 中按所选路径安装，先核对官方版本支持，再锁定项目版本；不要把未经测试的最新版组合称为兼容矩阵：

```text
python -m venv .venv
.venv\Scripts\python -m pip install build123d
```

上述为 Windows 的可选示例，不是必须执行的安装。CadQuery 路径用 `cadquery` 替代；mesh QA 可选 `trimesh`，精确布尔还可能需 `manifold3d`；浏览器方案需 `playwright` 和 `python -m playwright install chromium`。Blender、Plasticity、Bambu Studio 按官方应用安装流程安装。**安装这些软件不会使本包 scaffold 自动变为实现。** Linux/macOS venv 解释器位于 `.venv/bin/python`。CAD 二进制依赖与 Python/平台匹配必须实测。

回滚：保留旧版目录，以独立副本试用；不使用时移走本 Skill 副本。项目历史与证据应保留，不通过清理旧证据伪装验证状态。

## 开源与贡献

本项目采用 [MIT License](LICENSE)。上游概念来源与原始声明见 [UPSTREAM-NOTICE.txt](UPSTREAM-NOTICE.txt) 和 [复用说明](references/sources-and-reuse.md)。贡献前请读 [CONTRIBUTING.md](CONTRIBUTING.md)。

本项目由社区维护，与 Bambu Lab 或 MakerWorld 无官方隶属或背书关系。许可证适用于本仓库内容，不会自动改变用户模型、第三方素材或品牌的权利。
