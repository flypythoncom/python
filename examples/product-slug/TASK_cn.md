# 任务契约：规范化产品 slug

只修改 `starter/product_slug.py`。

- `normalize_product_slug(name)` 返回小写 ASCII slug；
- 连续空白、`_` 或 `-` 变成一个 `-`；
- 其他标点被移除，不能产生重复分隔符；
- 去掉开头和结尾的分隔符；
- 结果为空时抛出 `ValueError`；
- 不增加依赖，不修改测试。

完成标准：`python examples/product-slug/verify.py starter` 成功退出。
