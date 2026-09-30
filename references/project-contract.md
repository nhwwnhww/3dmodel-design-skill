# 项目契约与证据格式

复制 `assets/project-template` 为单独项目。建议布局：`spec.md`、`src/` 或原生工程、`exports/`、`evidence/<revision>/`、`release/`、`manifest.json`。项目以 mm 为统一制造单位。Skill 本身不包含模型成品。

## spec 最小字段
创意、目标用户/场景、外观语言、尺寸/预算、功能、接受标准、主 backend/单位/源文件、打印机/喷嘴/材料/板材/profile、支撑/朝向、纯打印 BOM、关键风险、未知项、未来请求、阶段状态。

## manifest v1
- `schema_version: 1`；`revision` 为非空版本标识。
- `profile` 至少包含 printer、nozzle_mm、material、plate、layer_height_mm；补全材料系列、profile 版本和影响输出的设置。
- `inputs` 是项目相对路径 → 小写 SHA256。**必须列出所有影响当前模型/工艺的源文件、参数、当前导出与打印配置快照**；校验器无法自动知道漏报的文件。
- `assembly_required` 是 boolean；多件需 true。
- `behavioral_claims` 是拟宣称的实际行为列表（如 snap、press、rotation）。没有则空列表，不能为省略测试而漏报。
- `gates` 为 build / visual / dfam / slice / prototype / release，适用时加 assembly。

每个 gate：`status`（unknown/blocked/failed/passed）、`reviewer`（实际检查者）、`revision`、`input_digest`、`details`、`artifacts`。
每个 artifact：`path`（相对 manifest 所在项目目录，不准越界）、`sha256`、`role`。
任何缺失、未知、失败或 hash 不匹配均不能满足 release gate。

| Gate | details 必填 | artifacts role 必填 | 人工内容审阅 |
|---|---|---|---|
| build | command, tool_versions | build_log, model | 真实执行/导出、对应源、实体/尺寸/invariant |
| visual | views, sections, findings | views, sections | 七视图均实际查看；至少两关键截面坐标/问题与结论 |
| dfam | orientation, supports, walls, material_basis | report | 配置相关规则、薄壁、支撑移除与朝向 |
| slice | slicer="Bambu Studio", version, profile, warnings, layer_review | project_3mf, preview | 当前版本实际切片、关键层与警告 |
| assembly | fit_table, motion_path | report | 适用的配合、穿透、插入路径及运动范围 |
| prototype | printer, material, observations, feedback | report, photo | 当前整件实物、设置、过程与用户反馈 |
| release | license, originality, limitations | listing, instructions | 原创/许可、实际限制与打印装配说明 |

visual.views 使用 front/back/left/right/top/bottom/iso；sections 是至少两个带平面/位置/检查对象的描述。用多份 artifact 对应各视图/切面，或一个包含完整视图与逐项审阅的报告，不能用一张图充数。details findings 必须如实记载发现和处理。
prototype 若含 behavioral_claims，还需 `behavior_tests` 对象逐条说明对应物理试验方法、验收值/现象、结果和报告位置。一个正常打印照片不足以证明卡扣循环或转动成功。

## 更新操作顺序
1. 修改源/配置并分配 revision，真实构建/导出。
2. 将源、参数、输出、配置填入 inputs，记录真实文件 hash。
3. `python scripts/release_check.py <project>/manifest.json --digest` 计算摘要。
4. 重做各阶段验证，保存当前证据，填 hash、摘要与 revision，实际审阅后再填 passed。
5. 运行 release_check 并人工复核。若某阶段修改了 inputs（例如切片时改 profile），重算摘要并重新审阅受影响阶段；不要机械复制摘要以消除报错。

inputs 建议采用切片前已保存的配置快照，slice 的最终 3MF 作为 evidence，避免将审阅报告本身纳入 inputs 形成循环。文件清单完整性与证据语义依靠人工；校验器只查声明的文件。
