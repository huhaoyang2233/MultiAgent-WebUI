import json
import os
from typing import Any, Dict, List

DATA_DIR = os.path.join(os.path.dirname(__file__), 'files')

os.makedirs(DATA_DIR, exist_ok=True)

class JSONDatabase:
    def __init__(self, filename: str):
        self.filepath = os.path.join(DATA_DIR, f"{filename}.json")

    def _load_data(self) -> Dict[str, Any]:
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_data(self, data: Dict[str, Any]):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        data = self._load_data()
        return data.get(key, default)

    def set(self, key: str, value: Any):
        data = self._load_data()
        data[key] = value
        self._save_data(data)

    def delete(self, key: str):
        data = self._load_data()
        if key in data:
            del data[key]
            self._save_data(data)

    def get_all(self) -> Dict[str, Any]:
        return self._load_data()

    def append(self, key: str, value: Any):
        data = self._load_data()
        if key not in data:
            data[key] = []
        data[key].append(value)
        self._save_data(data)

    def update(self, key: str, index: int, value: Any):
        data = self._load_data()
        if key in data and isinstance(data[key], list):
            if 0 <= index < len(data[key]):
                data[key][index] = value
                self._save_data(data)

    def remove(self, key: str, index: int):
        data = self._load_data()
        if key in data and isinstance(data[key], list):
            if 0 <= index < len(data[key]):
                del data[key][index]
                self._save_data(data)

    def find_by_id(self, key: str, item_id: str) -> Any:
        data = self._load_data()
        if key in data and isinstance(data[key], list):
            for item in data[key]:
                if item.get('id') == item_id:
                    return item
        return None

    def find_index_by_id(self, key: str, item_id: str) -> int:
        data = self._load_data()
        if key in data and isinstance(data[key], list):
            for index, item in enumerate(data[key]):
                if item.get('id') == item_id:
                    return index
        return -1

    def delete_by_id(self, key: str, item_id: str):
        index = self.find_index_by_id(key, item_id)
        if index != -1:
            self.remove(key, index)