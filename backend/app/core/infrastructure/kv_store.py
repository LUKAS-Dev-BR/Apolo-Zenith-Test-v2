import json
import time
from typing import Optional, Any
from pathlib import Path
from app.config import settings

class KVStore:
    def __init__(self):
        self.store_dir = settings.DATABASE_DIR / "kv_store"
        self.store_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_path(self, key: str) -> Path:
        safe_key = key.replace("/", "_").replace("\\", "_")
        return self.store_dir / f"{safe_key}.json"
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        path = self._get_path(key)
        
        data = {
            'value': value,
            'created_at': time.time(),
            'ttl': ttl
        }
        
        with open(path, 'w') as f:
            json.dump(data, f)
    
    def get(self, key: str) -> Optional[Any]:
        path = self._get_path(key)
        
        if not path.exists():
            return None
        
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            
            if data.get('ttl'):
                if time.time() - data['created_at'] > data['ttl']:
                    self.delete(key)
                    return None
            
            return data['value']
        except (json.JSONDecodeError, KeyError):
            return None
    
    def delete(self, key: str):
        path = self._get_path(key)
        if path.exists():
            path.unlink()
    
    def exists(self, key: str) -> bool:
        path = self._get_path(key)
        return path.exists()
    
    def list_keys(self, prefix: str = "") -> list:
        keys = []
        for path in self.store_dir.glob("*.json"):
            key = path.stem
            if prefix and not key.startswith(prefix):
                continue
            keys.append(key)
        return keys
    
    def increment(self, key: str, amount: int = 1) -> int:
        current = self.get(key)
        if current is None:
            current = 0
        
        new_value = current + amount
        self.set(key, new_value)
        return new_value
    
    def set_hash(self, key: str, field: str, value: Any):
        hash_key = f"{key}:{field}"
        self.set(hash_key, value)
    
    def get_hash(self, key: str, field: str) -> Optional[Any]:
        hash_key = f"{key}:{field}"
        return self.get(hash_key)
    
    def delete_hash(self, key: str, field: str):
        hash_key = f"{key}:{field}"
        self.delete(hash_key)
    
    def get_all_hash(self, key: str) -> dict:
        result = {}
        for path in self.store_dir.glob(f"{key}:*.json"):
            field = path.stem.split(":", 1)[1]
            value = self.get(f"{key}:{field}")
            if value is not None:
                result[field] = value
        return result
