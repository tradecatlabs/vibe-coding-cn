"""校验 v1 结构化说明载荷并生成逐对象 Markdown 表格。"""
from hashlib import sha256
import html
from pathlib import Path
import re
import source_archive

TEMPLATE_PATH = ".github/context/assets/templates/tool-explanation-template-v1.md"
FIELD_NAMES = (
    "工具的名称",
    "是什么",
    "为什么",
    "怎么做",
    "扩展",
    "关联信息",
    "出处",
    "相关图书",
    "它要解决什么问题？",
    "为什么这样设计？",
    "内部如何实现？",
    "付出了什么代价？",
    "比较不同技术与方法。",
    "提炼共同规律。",
    "明确这些规律成立的前提与适用条件。",
    "结论",
    "连接规则",
    "依据",
)
MAX_ITEMS = 1024
MAX_FIELD_BYTES = 64 * 1024
MAX_PAYLOAD_BYTES = 16 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def template_bytes(root):
    path = source_archive.checked_path(Path(root), TEMPLATE_PATH)
    require(path.is_file(), "v1模板缺失或不是普通文件")
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    marker = "## 单对象 Markdown 表格模板"
    require(text.count(marker) == 1, "v1模板表格入口不唯一")
    table_lines = text.split(marker, 1)[1].splitlines()
    require(table_lines.count("| 序号 | 说明项 | 内容 |") == 1 and
            table_lines.count("|:---:|:---|:---|") == 1, "v1模板表头或三列表格分隔符漂移")
    rows = []
    for line in table_lines:
        parts = line.split("|")
        if len(parts) != 5 or not parts[1].strip().isdigit():
            continue
        rows.append((int(parts[1].strip()), parts[2].strip()))
    require([number for number, _ in rows] == list(range(1, 19)), "v1模板序号缺失或重排")
    names = tuple(name for _, name in rows)
    require(names == FIELD_NAMES, "v1模板名称或顺序漂移")
    return raw


def template_sha256(root):
    return sha256(template_bytes(root)).hexdigest()


def validate_payload(root, payload, expected_objects):
    """返回 object_key 到18项字段的映射，并绑定模板和全部当前对象。"""
    raw_template = template_bytes(root)
    require(isinstance(payload, dict) and set(payload) == {"template_sha256", "items"},
            "v1说明载荷字段不符")
    require(payload["template_sha256"] == sha256(raw_template).hexdigest(), "v1说明与已登记模板版本不匹配")
    items = payload["items"]
    require(isinstance(items, list) and len(items) <= MAX_ITEMS, "v1说明对象数量超限")
    require(isinstance(expected_objects, dict) and len(expected_objects) <= MAX_ITEMS and
            all(isinstance(key, str) and key and isinstance(name, str) and name.strip()
                for key, name in expected_objects.items()), "当前对象集合无效或超限")
    result = {}
    size = 0
    for item in items:
        require(isinstance(item, dict) and set(item) == {"object_key", "fields"}, "v1说明对象结构不符")
        key = item["object_key"]
        require(isinstance(key, str) and key and key not in result, "v1说明对象身份为空或重复")
        fields = item["fields"]
        require(isinstance(fields, list) and len(fields) == len(FIELD_NAMES), "每个对象必须完整包含18项")
        for expected_name, field in zip(FIELD_NAMES, fields):
            require(isinstance(field, dict) and set(field) == {"name", "content"}, "v1说明项结构不符")
            require(field["name"] == expected_name, "v1说明项名称或顺序与模板不符")
            content = field["content"]
            require(isinstance(content, str) and content.strip(), "v1说明项不得留空")
            encoded = content.encode("utf-8")
            require(len(encoded) <= MAX_FIELD_BYTES, "单个v1说明项超过64KiB")
            require(not re.search(r"[\x00-\x08\x0b-\x0c\x0e-\x1f\ufffe\uffff]", content),
                    "v1说明项含不支持的控制字符")
            size += len(encoded)
            require(size <= MAX_PAYLOAD_BYTES, "v1说明总量超过16MiB")
        result[key] = fields
    require(set(result) == set(expected_objects), "v1说明对象与当前登记范围不一致")
    for key, name in expected_objects.items():
        require(result[key][0]["content"] == name, "v0名称项与对象身份名称不一致")
    return result


def _cell(value):
    value = html.escape(value, quote=False)
    for char, entity in (("\\", "&#92;"), ("`", "&#96;"), ("*", "&#42;"),
                         ("_", "&#95;"), ("~", "&#126;"), ("[", "&#91;"),
                         ("]", "&#93;"), ("|", "&#124;")):
        value = value.replace(char, entity)
    return value.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>").replace("\t", "&#9;")


def anchor_for(object_key):
    slug = re.sub(r"[^a-z0-9-]+", "-", object_key.lower()).strip("-") or "item"
    suffix = sha256(object_key.encode("utf-8")).hexdigest()[:8]
    # 已发布的v0锚点继续使用，避免模板迁移破坏现有阅读链接。
    return f"v0-{slug}-{suffix}"


def render_table(fields):
    require(isinstance(fields, list) and len(fields) == 18, "每张v1表格必须有18项")
    require(all(isinstance(field, dict) and set(field) == {"name", "content"} and
                isinstance(field["name"], str) and isinstance(field["content"], str) for field in fields),
            "表格字段结构不符")
    require([field["name"] for field in fields] == list(FIELD_NAMES), "表格字段与v1模板不符")
    for field in fields:
        require(field["content"].strip() and len(field["content"].encode("utf-8")) <= MAX_FIELD_BYTES,
                "表格内容为空或超过64KiB")
        require(not re.search(r"[\x00-\x08\x0b-\x0c\x0e-\x1f\ufffe\uffff]", field["content"]),
                "表格内容含不支持的控制字符")
    lines = ["| 序号 | 说明项 | 内容 |", "|:---:|:---|:---|"]
    for number, field in enumerate(fields, 1):
        lines.append(f"| {number} | {_cell(field['name'])} | {_cell(field['content'])} |")
    return "\n".join(lines)


def render_object(object_key, title, fields):
    anchor = anchor_for(object_key)
    return "\n".join((f'<a id="{anchor}"></a>', "### " + _cell(title) + "", "",
                       render_table(fields), ""))


def render_index_link(object_key, title):
    return f"- [{_cell(title)}](#{anchor_for(object_key)})"


def render_file_link(object_key, title, filename):
    require(isinstance(filename, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", filename),
            "对象导航目标文件名不规范")
    return f"- [{_cell(title)}]({filename}#{anchor_for(object_key)})"
