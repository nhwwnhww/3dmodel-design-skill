# Bambu Studio authoritative slicing
v0.1 支持人工 GUI 流程与证据记录检查；**未实现 Bambu CLI 调用或 3MF/G-code 语义分析**。slice_check.py 不启动 slicer，不从文件存在推断切片成功。

## GUI 验证流程
1. 核实应用版本、实际打印机、喷嘴、板材、材料/profile。导入当前导出，核对一个已知尺寸、零件数和朝向。
2. 保存 Bambu Studio project 3MF；核对支撑、层高、壁/填充与缝线设置的设计意图；保留 profile 名称和自定义差异。
3. 执行切片，逐项解释警告并记录；无警告不等于无问题。
4. 审阅首层、薄壁、小细节、桥接、顶部封口、关键配合/活动间隙、内腔与支撑拆除路径；对关键层保存带层号的截图。
5. 保存切片后的项目与预览、估算时间/材料量、警告处理报告。确认重新打开同一项目仍对应当前模型和设置；必要时重新切片。
6. 记录输入几何 hash、项目 3MF hash、软件版本、profile、审阅者。只对这个 revision 和配置给出结论。

## CLI 的未来接入契约
先读取 [官方 Command Line Usage](https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage) 并核对本机该版本帮助输出、可执行路径与平台限制，不复制未验证 flags。Windows/macOS/Linux 路径与封装不同；GUI 存在不能证明所有 CLI 功能可用。
将来的 adapter 需接受 executable、输入、profile、输出目录与超时，捕获实际参数、退出码、stdout/stderr、产物 hash，并保留失败证据。不得通过 shell 拼接任意字符串，也不能把 exit 0 作为完整 slice gate。
CLI 缺失/失败时转人工 GUI；GUI 也不可用则 gate=blocked，交接用户需要提供的版本、3MF、关键层预览、警告与设置，不假造已切片。
