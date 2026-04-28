import json
import os
from typing import Any, Dict, List

DATA_DIR = os.path.join(os.path.dirname(__file__), 'files')

os.makedirs(DATA_DIR, exist_ok=True)

class JSONDatabase:
    def __init__(self, filename: str):
        self.filepath = os.path.join(DATA_DIR, f"{filename}.json")
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_data(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any):
        self.data[key] = value
        self._save_data()

    def delete(self, key: str):
        if key in self.data:
            del self.data[key]
            self._save_data()

    def get_all(self) -> Dict[str, Any]:
        return self.data

    def append(self, key: str, value: Any):
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(value)
        self._save_data()

    def update(self, key: str, index: int, value: Any):
        if key in self.data and isinstance(self.data[key], list):
            if 0 <= index < len(self.data[key]):
                self.data[key][index] = value
                self._save_data()

    def remove(self, key: str, index: int):
        if key in self.data and isinstance(self.data[key], list):
            if 0 <= index < len(self.data[key]):
                del self.data[key][index]
                self._save_data()

    def find_by_id(self, key: str, item_id: str) -> Any:
        if key in self.data and isinstance(self.data[key], list):
            for item in self.data[key]:
                if item.get('id') == item_id:
                    return item
        return None

    def find_index_by_id(self, key: str, item_id: str) -> int:
        if key in self.data and isinstance(self.data[key], list):
            for index, item in enumerate(self.data[key]):
                if item.get('id') == item_id:
                    return index
        return -1

    def delete_by_id(self, key: str, item_id: str):
        index = self.find_index_by_id(key, item_id)
        if index != -1:
            self.remove(key, index)
