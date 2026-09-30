# v0.1 工具状态和实现边界

“可直接借鉴”描述上游思路的复用决策；不代表复制的代码已在此环境运行。此版本没有直接拷贝上游执行代码，以下 Python/HTML 均为新写的有限实现或显式 scaffold。

| 文件 | 复用类别 | 本包实际状态 | 依赖 / 未提供能力 |
|---|---|---|---|
| checks_template.py | 可直接借鉴 invariant 思路 | 已实现：检查外部测量值是否在范围内 | 标准库；不提取 CAD/mesh 数值 |
| shoot.py | 改造后实现 | 仅 scaffold，退出 2 | 未来 Playwright+Chromium/Blender；无截图功能 |
| viewer_glb.html | 改造后实现 | 仅 scaffold 状态页 | 未来 Three.js/GLTF loader；无模型查看功能 |
| viewer_stl.html | 改造后实现 | 仅 scaffold 状态页 | 未来 Three.js/STL loader；无模型查看功能 |
| wallcheck.py | 改造后实现 | 仅 scaffold，退出 2 | 未来 CAD/trimesh/ray 依赖；不测壁厚 |
| assembly_check.py | 改造后实现 | 已实现有限 AABB broad phase | 标准库；无实体碰撞/间隙/运动求解 |
| slice_check.py | 我们新增 | 已实现切片证据记录校验 | 标准库；不执行 Bambu Studio 或读取切片语义 |
| render_beauty.py | 我们新增 | 仅 scaffold，退出 2 | 未来 Blender；无渲染功能 |
| release_check.py | 我们新增 | 已实现发布证据完整性/一致性检查 | 标准库；不能判断证据内容真伪或证明作品有效 |

## 调用与输入
在 Skill 根目录运行；项目输入可给绝对路径。示例文件故意保持 unknown，不包含真实成功证据。

```text
python scripts/checks_template.py assets/project-template/measurements.json
python scripts/assembly_check.py assets/project-template/bounds.json
python scripts/release_check.py assets/project-template/manifest.json
python scripts/slice_check.py assets/project-template/manifest.json
python scripts/shoot.py --contract
python scripts/wallcheck.py --contract
python scripts/render_beauty.py --contract
```

`checks_template`：从实测/CAD 测量填 `actual,min,max,unit,method,source_revision`。预期范围来自 spec，不能看测量结果后任意放宽。退出 0 仅表示输入的数值范围满足要求。
`assembly_check`：输入毫米、同一坐标系中每件的 min/max AABB；输出 disjoint / possible_contact / possible_overlap。退出 0 表示筛查执行成功，即使出现 possible_overlap；不写 assembly passed。
`release_check --digest`：只打印对声明 inputs/profile/behavior requirements 计算的摘要；不是检查成功，也不修改 manifest。输入文件 SHA256 可用 PowerShell `Get-FileHash -Algorithm SHA256 <path>`，填入小写十六进制。

证据校验器防意外串版、缺件和被修改的文件，不防主动伪造。它不解析 PNG、3MF、STL，role 是记录标签，不能仅因为一份任意文本标了 photo 就认为实拍通过。代理/人工必须打开实际产物、审阅内容，按项目契约补全真实证据后签署。

## 后续实现验收
- render：固定测试几何（含孔、内腔、错位件）、验证七视角与两切面内容、失败/空白截图检测、模型 hash 绑定。
- wall：已知厚度/薄壁/空腔/退化几何 fixture；报告采样覆盖与误差，不把抽样最小值当全局证明。
- assembly：实际碰撞、允许接触、插入路径与运动姿态 fixture；不得用 AABB 代替 narrow phase。
- slicer：在目标 OS 和具体 Bambu Studio 版本验证帮助/参数，真实切片并重开 3MF 审阅；成功和失败 fixture 均需覆盖。
任何实现前保留当前 scaffold 非成功行为；没有外部集成测试不能把状态改为 validated。
