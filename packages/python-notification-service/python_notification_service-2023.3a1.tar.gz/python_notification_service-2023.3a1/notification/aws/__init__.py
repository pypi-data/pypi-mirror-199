import hashlib
from typing import Any


def generate_resource_id(topic: Any) -> str:
    if isinstance(topic, str):
        return hashlib.new('sha256', topic.encode()).hexdigest()[:12].upper()
    elif isinstance(topic, bytes):
        return hashlib.new('sha256', topic).hexdigest()[:12].upper()
    else:
        return hashlib.new('sha256', str(topic).encode()).hexdigest()[:12].upper()
