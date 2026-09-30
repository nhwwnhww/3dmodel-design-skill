# MakerWorld release candidate
本模块生成候选材料，不自动上传或发布。发布前实时核查平台规则，平台审核/流量/原创认定不由本 Skill 保证。

候选包包括：对应 revision 的模型文件、实际 Bambu Studio 3MF、打印配置说明、所需纯打印零件、装配/后处理说明、真实照片、必要渲染（明确标注）、验证范围与局限、许可与素材/灵感来源、标题/简介/标签草稿。保留可编辑源供用户留档，不默认公开用户全部源文件。

文案回答：作品的创意和使用场景是什么；怎么打印和装配；用户可改哪些参数；哪些配置已实际测试；哪些没有。打印时间与质量注明来自 slicer estimate 还是实际观察。

证据 gate：build、visual+sections、DfAM、Bambu slice、整件 physical prototype、release 文档；多件/行为类加 assembly。涉及实际行为还需逐项对应的物理验收记录，不以一般“打印完成”替代。

originality review 是来源与过程审阅，不是法律鉴定。素材许可、remix 署名及平台资格需要按作品实情确认；不能用未知许可证的第三方模型宣称原创。平台规则可能变化，无法读取时说明未核实，不声称已满足全部平台要求。

推荐声明层次：concept / geometry built / visually reviewed / Bambu slice verified / prototype tested / release candidate。`release_check.py` 只验证记录一致性，成功意味着 evidence_records_complete；人工审阅之后才给出相应状态。

[MakerWorld](https://makerworld.com/) 为发布入口；本包没有验证当前上传界面、表单字段或账户资格。发布需用户授权最终模型、描述和许可证，不能因本 Skill 被调用就自动发布。已有明确且覆盖当前产物的发布授权继续有效，不重复索取；仅在授权范围不清或最终产物/许可超出授权时澄清。缺少技术验证与缺少发布授权是两类不同阻塞。
