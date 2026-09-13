# 任务契约：场景报表工具（实战课程核心）

只修改 `starter/report_tool.py`。仅用标准库；不新增依赖。

- `load_records(path) -> list[dict]`：
  - `.csv` 文件经 `csv.DictReader` 加载。
  - `.json` 文件按对象列表加载；不是列表或元素不是对象时抛出
    `ValueError`。
  - 其他后缀抛出 `ValueError`，并指明不支持的文件名。
- `build_report(records, *, required_fields, numeric_field, group_field) -> dict`：
  - 返回 `{"total", "valid", "invalid", "groups", "errors"}`。
  - 无效行绝不中止运行：每行以 `{"index": <行位置>, "reason": <简短
    说明>}` 收集进 `errors`。无效指：不是字典、必填字段缺失或为空、
    `numeric_field` 不是数字（布尔值不算数字）。
  - 有效行聚合为 `groups[分组值] = {"count": int, "total": float}`；每个
    分组总计保留两位小数。
  - 任何输入下都必须满足 `total = valid + invalid`。
- `write_report(report, destination)`：
  - 原子地写入 JSON（UTF-8、缩进 2、末尾换行）：先写同名临时文件，再
    `os.replace`。
  - 自动创建缺失的父目录。
  - 成功后不留任何 `.tmp` 文件。
- `run_scenario(scenario_dir) -> dict`：
  - 读取 `scenario.json`（`data_file`、`required_fields`、
    `numeric_field`、`group_field`、`report_file`），处理数据文件，把
    报告写进场景目录，并返回报告。
- `main(argv=None) -> int`：
  - 恰好一个参数（场景目录）。否则向 stderr 打印用法并返回 2。
  - 成功时向 stdout 打印 `total=... valid=... invalid=...` 并返回 0。
  - 输入失败时向 stderr 打印 `error: ...` 并返回 1。

完成的标准是 `python verify.py starter` 以 0 退出且九个测试全部通过，
同时 `python verify.py starter --expect-failure` 非零退出——因为
starter 已不再复现未完成状态。
