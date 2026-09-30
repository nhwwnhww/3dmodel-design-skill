# Bought components — TBC / future expansion
状态：**TBC，v0.1 不实现、不默认启用、不生成硬件接口几何。** 包括 magnets、motors、bearings、electronics、metal fasteners、hybrid printed/non-printed assemblies。

设计意图：未来让可核查外购件融入原创作品，兼顾装配、维护与低 BOM。不要现在创建空的可调用硬件 adapter；本文件仅定义未来数据契约。

未来输入：component ID、厂商/型号/版本、datasheet/STEP 或实测来源、测量日期、单位、datum、外形/安装/运动包络、尺寸及公差可信度、数量、载荷/热/电约束。
未来输出：经核验尺寸记录、硬件接口参数、装配/拆卸路径、紧固与防脱策略、附加 BOM、需要的测试与未知项。
扩展点：model-routing 的接口实体；assembly 的外购件包络与访问路径；prototype 的保持力/热/电相关测试；release 的外购 BOM、来源与装配说明。

启用前需明确的新范围：选定部件证据、设计约束、验证方式，以及用户接受增加 BOM。不能凭“常见磁铁尺寸”猜孔，也不能为未选硬件做看似准确的占位模型。v0.1 遇到需求时记录在 spec future_requests，先继续不依赖硬件的工作。
