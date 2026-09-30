# Backend routing 与 source of truth
| 设计特征 | 优先路径 | 保留什么 | 不证明什么 |
|---|---|---|---|
| 尺寸驱动实体、配合面、圆角/倒角 | build123d 或 CadQuery | build.py、PARAMETERS、版本、STEP（适用时）、导出日志 | CAD 成功不等于 FDM 成功 |
| 有机雕塑、纹理、角色造型 | Blender | .blend、单位/尺寸、modifier 顺序、导出配置及可重复操作 | render surface 不等于封闭实体 |
| 交互式曲面探索 | Plasticity | 原生项目、尺寸表、导出步骤、可用中间实体格式 | 不假定有可调用 CLI/API |
| 混合创意外壳 + 精密接口 | 有机外观 + CAD 接口 | 两边源工程、变换矩阵、接口 datum、组合步骤 | 布尔成功不等于最薄处足够 |
| 网格检测/有限修复 | trimesh；必要时 manifold3d | 原网格、修复方法、前后报告 | repair 不能替代设计决策 |

先选择一个主 backend；不能因为库容易安装而将所有作品强行 mesh-first。v0.1 未集成这些 backend 的执行器。

项目明确毫米、原点、Z-up 和建造板坐标。STL 不携带可靠单位语义，导入 Bambu Studio 后对照一个已知尺寸；GLB 的单位/坐标转换也要记录，不能直接混用数值。原生 CAD 导出记录线性/角度离散精度，检查细节丢失、面翻转和零件丢失。

PARAMETERS 按“外观/尺寸/接口/制造”组织，每项记录单位、范围、意图与来源；派生量用表达式计算，避免多个重复常量。参数和源工程一起进入 revision 的 inputs。

真实 build 指重新运行生成脚本或从已保存原生工程执行已记录的导出。保存命令/操作、工具版本、输出 hash。运行项目自身 invariant，例如件数、整体尺寸、公称接口、孔是否贯通、预期腔体；不能将 `assert True` 算验证。

离线人工路径：用户在原生应用生成导出并提供日志/截图，代理标记为 user-supplied evidence，核对 revision 与尺寸，不能伪称自己运行了 CAD。
