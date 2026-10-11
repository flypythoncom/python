# 任务契约：堵上一个笔记服务里的五个安全漏洞

只修改 `starter/notes_app.py`。仅用标准库。绝不修改 `tests/`、
`solution/`、`scenario/` 或 `attack_replay.py`（提供的测试工具，在
`starter/` 与 `solution/` 中完全相同）。`init_db` 已经提供且正确。除非
特别说明，下面每个参数都由攻击者控制。拒绝一律抛出 `SecurityError`。

- `find_notes(conn, owner, query) -> list[dict]`：
  - 返回 *owner* 的、标题包含 *query*（不区分大小写）的笔记
    `{"id", "title", "body"}`，按 id 排序。
  - *owner* 和 *query* 只能以绑定参数（`?`）进入 SQLite，绝不经过字符串
    格式化。任何输入都不能返回别的 owner 的笔记。
  - *query* 是字面子串：`%` 和 `_` 只匹配它们自己。
- `read_attachment(base_dir, name) -> bytes`：
  - *base_dir* 可信；*name* 不可信。拒绝空的或绝对路径的 *name*，并拒绝
    任何解析后路径（处理 `..` 和符号链接之后）不在解析后的 *base_dir*
    之内的 *name*。
  - 被拒绝的名字绝不读取任何文件。位于 *base_dir* 之内但不存在的名字抛出
    `FileNotFoundError`。
- `load_secret_key(env=None) -> bytes`：
  - 从 *env*（缺省为 `os.environ`）读取 `NOTES_SECRET_KEY`。缺失或少于
    32 个字符时抛出点名 `NOTES_SECRET_KEY` 的 `SecurityError`。没有缺省
    密钥。
- `hash_password(password, *, salt=None, iterations=600_000) -> str`：
  - 用 `hashlib.pbkdf2_hmac("sha256", …)` 返回
    `pbkdf2_sha256$<iterations>$<salt hex>$<digest hex>`；*salt* 为 `None`
    时用 `secrets` 生成新的 16 字节盐。同一个密码哈希两次得到不同字符串。
    这里接受任何 *iterations* 值；最低次数由 `verify_password` 把关。
- `verify_password(password, stored) -> bool`：
  - 只有迭代次数不少于 600 000、摘要匹配（用 `hmac.compare_digest` 比较）
    的 `pbkdf2_sha256` 字符串才返回 True。其他任何格式——包括裸 MD5 十六
    进制摘要——都返回 False。
- `dump_session(data, key) -> str` / `load_session(token, key) -> dict`：
  - token 是 base64url 编码的 JSON、一个字面的 `.`，再接用 *key* 对
    base64url 部分算出的十六进制 HMAC-SHA256；可以去掉填充。绝不使用
    `pickle`。
  - `load_session` 在解码任何东西**之前**先用 `hmac.compare_digest` 校验
    签名。格式错误的 token、签名不对、用别的密钥签的 token、含非 ASCII
    字符的 token、不是 JSON 的 payload、不是对象的 JSON，都抛出
    `SecurityError`——绝不抛别的异常类型。

`python starter/attack_replay.py <scenario-dir>` 重放场景的 `attacks.json`
并打印 `blocked=X/Y`；只有每个攻击都被挡住时才以 0 退出。

针对原样的 starter 运行套件时，会故意反序列化一个无害的 gadget，它在临时
文件夹里创建一个目录——这正是 starter 会执行攻击者提供数据的证据。

完成的标准是 `python verify.py starter` 以 0 退出且全部十六个测试通过
（在无法创建符号链接、符号链接测试被跳过的平台上为十五个）。
