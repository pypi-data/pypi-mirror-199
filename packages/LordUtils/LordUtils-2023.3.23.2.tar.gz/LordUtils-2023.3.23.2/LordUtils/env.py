
from pathlib import Path


def env_to_bool(key, default) -> bool:
    v = environ.get(key, default)
    if isinstance(v, bool):
        return v
    v = v.lower()
    if v == 'none':
        return default
    r = v in ['true', '1', 'on', 'yes', 'active']
    return r


def env_to_list(key, default) -> list:
    v = environ.get(key, default)
    if isinstance(v, list):
        return v
    if v is None:
        return default
    v = regex.split('; *', v)
    return v


def env_to_path(key, default, create=False) -> Path:
    v = environ.get(key, default)
    if v is None:
        return default
    v = Path(v)
    if create and not v.exists():
        v.mkdir(parents=True, exist_ok=True)
    return v
