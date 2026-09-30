---
name: makerworld-design-studio
description: Use when creating or revising original creative FDM designs for Bambu Studio and MakerWorld, including PETG models, printed assemblies, prototype feedback, and release candidates.
metadata:
  version: "0.1"
---
# MakerWorld Design Studio v0.1

把原创概念推进到可切片、实物验证、有证据的 MakerWorld 发布候选。默认 Bambu Lab P1S / 0.4 mm / PETG-first / 纯打印低额外 BOM；这些是可覆盖的项目默认值，不能代替用户实际机器、耗材和校准结果。Bambu Studio 是最终 authoritative slicer。

## Hard rules
- **没有真实 build + 多视角与 section 检查 + Bambu Studio slicer verification，不得声称 “ready to print”。** 尚未实打印时只可称“已完成数字验证，待实打印”，并限定已验证配置。
- **fit / snap / press / mechanism 等实际行为，没有对应 physical test 不得声称 “works”。** 切片成功、网格 watertight、漂亮渲染和脚本退出 0 都不等于实物有效。
- 每次 geometry change 必须重新构建、导出、实际查看多视角与关键截面。参数、源文件、输出、打印配置变化使关联证据失效；保留旧证据但不能挪用为当前版本。
- 集中维护参数与设计 invariant。脚本 CAD 以 `build.py` / `PARAMETERS` 为源；Blender / Plasticity 使用可编辑原生工程、尺寸参数表和可复现导出记录。不得偷偷修导出网格而不回写源工程。
- 数值经验必须标记来源、适用条件、是否实测。缺失证据用 `unknown` / `blocked`，不得虚构命令结果、图片审阅、用户反馈或打印成功。
- 外购件只在 [TBC 模块](modules/tbc/bought-components.md) 记录扩展需求；v0.1 不设计其接口几何或生成采购方案。用户要启用时明确这是另一个范围，先澄清。

## Workflow 与按需加载
1. **Idea → creative exploration**：读取 [creative-design](references/creative-design.md)，明确用户体验、造型语言、原创差异，展示少量方向及取舍；已有确定概念直接沿用。
2. **Design spec**：使用 [项目契约](references/project-contract.md)，记录外观、尺寸、功能、材料/打印机配置、可测 acceptance criteria 与未知项。关键缺参先问；不重复审批已批准方向。
3. **Backend routing → build**：读取 [model-routing](references/model-routing.md)，选择 build123d / CadQuery / Blender / Plasticity 或混合路径，执行真实构建并绑定源文件和导出 hash。
4. **Visual & geometry QA**：查看 front/back/left/right/top/bottom/iso 与至少两个关键截面；记录切面位置、检查对象和发现。运行项目 invariant，检查单位、尺寸、实体/壳体数量与网格有效性。截图清单不等于读过图像。
5. **DfAM gate**：读取 [fdm-design-rules](references/fdm-design-rules.md) 和 [material-petg](references/material-petg.md)，权衡朝向、层间受力、支撑可移除性、薄壁与表面；需要分件时读取 [slicer-style-cut](references/slicer-style-cut.md)。
6. **Optional assembly/fit gate**：多件、卡扣、压配或活动结构读取 [mechanisms-and-fits](references/mechanisms-and-fits.md) 与 [assembly-verification](references/assembly-verification.md)。单件装饰可记带理由的 N/A；机构不能跳过。
7. **Bambu Studio slice verification**：读取 [bambu-studio](references/bambu-studio.md)，在实际安装版本中切片并审阅逐层预览。保存 3MF、profile、警告、预览与版本。CLI 不可用时走 GUI；不能用别的 slicer 替代此 gate。
8. **Physical prototype → feedback → revision**：读取 [prototype-validation](references/prototype-validation.md)，先验证高风险局部，再整件打印。记录失败及反馈；迭代后重跑受影响 gate。
9. **MakerWorld release candidate**：读取 [makerworld-release](references/makerworld-release.md)，整理原创/许可、实拍、说明、3MF 和局限；运行 `python scripts/release_check.py <project>/manifest.json`。输出只检查证据记录，仍需人工审阅。发布或上传另需用户明确授权。

## 工具与交接
先读 [scripts/README](scripts/README.md)，再决定调用；scaffold 返回 2，不生成伪证据。工具缺失时完成可做部分并交付准确人工步骤，不自动安装大型 CAD 或打印软件。
交接写清当前 revision、已完成 gate、阻塞项、下一步、可用文件。保留阶段界限，不将 release candidate 称为已发布。依赖与当前验证范围见 [README](README.md) 和 [VALIDATION](VALIDATION.md)。
