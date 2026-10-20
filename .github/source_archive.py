"""领域原始资料读取：JSON载荷是事实源，当前程序位置及迁移绑定单独校验。"""
import base64
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re

FORMAT = 'vibe-coding-cn/source-archive@1'
MAX_BYTES = 64 * 1024 * 1024


class ArchiveError(ValueError):
    """可安全报告的固定档案契约错误，不携带原始输入值。"""


def require(condition, message):
    if not condition:
        raise ArchiveError(message)


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, '原始数据JSON含重复键')
            result[key] = value
        return result
    def constant(_value):
        raise ArchiveError('原始数据JSON含非有限数')
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)


def normal(value):
    require(isinstance(value, str), '来源定位必须是文本')
    path = PurePosixPath(value)
    require(value == path.as_posix() and path.parts and not path.is_absolute()
            and not any(part in {'.', '..', '.git', '.history', '.venv', 'logs'} or part.startswith('.env')
                        or part.lower() in {'auth.json', 'credentials.json', 'credentials.toml'}
                        or part.lower().endswith(('.pem', '.key', '.db', '.sqlite', '.sqlite3')) for part in path.parts)
            and '\\' not in value and ':' not in value, '来源路径越界或属于敏感数据')
    return value


def checked_path(root, relative):
    path = root / normal(relative)
    current = path
    while current != root:
        require(not current.is_symlink(), '来源或输出父目录含软链接')
        current = current.parent
    require(path.resolve().is_relative_to(root.resolve()), '来源越过仓库边界')
    return path


def root_and_key(path):
    path = Path(path).absolute()
    if '.github' in path.parts:
        index = path.parts.index('.github')
        root = Path(*path.parts[:index])
        return root, path.relative_to(root).as_posix()
    if path.name == '.gitmodules':
        return path.parent, '.gitmodules'
    return None, None


def raw_read(path, limit=MAX_BYTES):
    with path.open('rb') as stream:
        raw = stream.read(limit + 1)
    require(len(raw) <= limit, '来源超过读取预算')
    return raw


@lru_cache(maxsize=32)
def bundles(root):
    root = Path(root)
    result = {}
    identities = set()
    for kind in ('gongfa', 'faqi'):
        path = checked_path(root, f'.github/context/{kind}/data.json')
        if not path.exists():
            continue
        raw = raw_read(path)
        data = strict_json(raw)
        archive_fields = {'format', 'kind', 'source_revision', 'documents', 'locations', 'live_sources', 'projections'}
        require(frozenset(data) in {frozenset(archive_fields), frozenset(archive_fields | {'explanations_v1'})}
                and data['format'] == FORMAT and data['kind'] == kind
                and re.fullmatch('[a-f0-9]{40}', data['source_revision']), '原始数据格式不符')
        if 'explanations_v1' in data:
            explanations = data['explanations_v1']
            require(isinstance(explanations, dict) and set(explanations) == {'template_sha256', 'items'}
                    and isinstance(explanations['template_sha256'], str)
                    and re.fullmatch('[a-f0-9]{64}', explanations['template_sha256'])
                    and isinstance(explanations['items'], list) and len(explanations['items']) <= 1024,
                    'v1说明载荷格式不符')
        require(isinstance(data['documents'], dict) and len(data['documents']) <= 4096, '来源文档数量超限')
        decoded, total = {}, 0
        for key, item in data['documents'].items():
            normal(key)
            require(key not in identities, '同一来源文档被两个工具重复维护')
            identities.add(key)
            require(set(item) == {'mode', 'encoding', 'data', 'sha256'} and item['mode'] in {'100644', '100755', '120000'}
                    and item['encoding'] in {'utf-8', 'base64'} and isinstance(item['data'], str), '原始载荷字段不符')
            value = item['data'].encode('utf-8') if item['encoding'] == 'utf-8' else base64.b64decode(item['data'], validate=True)
            require(hashlib.sha256(value).hexdigest() == item['sha256'], '原始载荷SHA不符')
            total += len(value)
            require(total <= MAX_BYTES, '原始载荷总量超过64MiB')
            decoded[key] = value
        for key, target in data['locations'].items():
            normal(key); checked_path(root, target)
        for key, binding in data['live_sources'].items():
            normal(key)
            require(set(binding) == {'path', 'sha256'} and re.fullmatch('[a-f0-9]{64}', binding['sha256']), '当前来源绑定格式不符')
            checked_path(root, binding['path'])
        require(isinstance(data['projections'], list), '来源引用集合不符')
        for ref in data['projections']:
            normal(ref['path'])
            require(not Path(ref['target']).is_absolute() and '\\' not in ref['target'], '引用目标必须为相对路径')
            require((root / ref['path']).parent.joinpath(ref['target']).resolve().is_relative_to(root.resolve()), '引用目标越界')
        result[kind] = {'data': data, 'bytes': decoded, 'path': path, 'sha256': hashlib.sha256(raw).hexdigest()}
    return result


def clear_cache():
    bundles.cache_clear()


def source_document(path):
    root, key = root_and_key(path)
    if root is not None:
        normal(key)
        for bundle in bundles(root).values():
            if key in bundle['bytes']:
                return bundle, key
    return None, key


def physical_path(path):
    root, key = root_and_key(path)
    if root is None:
        return Path(path)
    choices = [(old, current) for bundle in bundles(root).values() for old, current in bundle['data']['locations'].items()
               if key == old or key.startswith(old + '/')]
    if choices:
        old, current = max(choices, key=lambda item: len(item[0]))
        return checked_path(root, current + key[len(old):])
    return Path(path)


def read_bytes(path, limit=MAX_BYTES):
    bundle, key = source_document(path)
    if bundle:
        raw = bundle['bytes'][key]
        require(len(raw) <= limit, '原始载荷超过读取预算')
        return raw
    target = physical_path(path)
    root, _key = root_and_key(target)
    if root is not None:
        checked_path(root, _key)
    return raw_read(target, limit)


def read_text(path):
    return read_bytes(path).decode('utf-8')


def source_is_file(path):
    bundle, _key = source_document(path)
    return bool(bundle) or physical_path(path).is_file()


def source_is_directory(path):
    root, key = root_and_key(path)
    if root is not None and any(any(name.startswith(key + '/') for name in bundle['bytes']) for bundle in bundles(root).values()):
        return True  # 历史来源容器，不声称旧目录在当前工作树仍存在。
    return physical_path(path).is_dir()


def source_is_symlink(path):
    bundle, key = source_document(path)
    return bundle['data']['documents'][key]['mode'] == '120000' if bundle else Path(path).is_symlink()


def source_readlink(path):
    bundle, key = source_document(path)
    if bundle:
        require(bundle['data']['documents'][key]['mode'] == '120000', '不是来源软引用')
        return bundle['bytes'][key].decode('utf-8')
    return os.readlink(path)


def bundle_bindings(root):
    return {item['path']: item['sha256'] for item in bundles(Path(root)).values()}


def check_unchanged(root):
    for path, digest in bundle_bindings(root).items():
        checked_path(Path(root), path.relative_to(root).as_posix())
        require(hashlib.sha256(raw_read(path)).hexdigest() == digest, '原始数据在读取期间变化')


def check_live(root):
    root = Path(root)
    check_unchanged(root)
    for bundle in bundles(root).values():
        for binding in bundle['data']['live_sources'].values():
            path = checked_path(root, binding['path'])
            require(hashlib.sha256(raw_read(path)).hexdigest() == binding['sha256'], '当前实现已变化；迁移绑定不再适用')
        for ref in bundle['data']['projections']:
            path = root / ref['path']
            require(path.is_symlink() and os.readlink(path) == ref['target'] and path.resolve().exists(), '平铺引用缺失或目标漂移')


def export_documents(root, kind, destination):
    """显式还原原始资料，供可重复核对/隔离CLI夹具使用；不是运行时旧目录。"""
    bundle = bundles(Path(root))[kind]
    destination = Path(destination)
    require(not destination.exists(), '还原目标必须是新目录')
    destination.mkdir(parents=True)
    for key, raw in bundle['bytes'].items():
        path = checked_path(destination, key)
        path.parent.mkdir(parents=True, exist_ok=True)
        mode = bundle['data']['documents'][key]['mode']
        if mode == '120000':
            target = raw.decode('utf-8')
            require(not Path(target).is_absolute() and (path.parent / target).resolve().is_relative_to(destination.resolve()), '原始引用还原越界')
            path.symlink_to(target)
        else:
            with path.open('xb') as stream:
                stream.write(raw)
            path.chmod(0o755 if mode == '100755' else 0o644)
