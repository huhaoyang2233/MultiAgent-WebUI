import json
import os
from typing import Any, Dict, List

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), 'sessions')

os.makedirs(SESSIONS_DIR, exist_ok=True)

class SessionDatabase:
    @staticmethod
    def get_session_filepath(session_id: str) -> str:
        return os.path.join(SESSIONS_DIR, f"{session_id}.json")

    @staticmethod
    def session_exists(session_id: str) -> bool:
        return os.path.exists(SessionDatabase.get_session_filepath(session_id))

    @staticmethod
    def create_session(session_id: str, chat_type: str = "", target_info: dict = None):
        if not SessionDatabase.session_exists(session_id):
            from datetime import datetime
            data = {
                "session_id": session_id,
                "messages": [],
                "created_at": datetime.utcnow().isoformat() + "Z",
                "updated_at": datetime.utcnow().isoformat() + "Z",
                "chat_type": chat_type,
            }

            if target_info:
                data["target_info"] = target_info

            SessionDatabase.save_session(session_id, data)

    @staticmethod
    def load_session(session_id: str) -> Dict[str, Any]:
        filepath = SessionDatabase.get_session_filepath(session_id)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "session_id": session_id,
            "messages": [],
            "created_at": "",
            "updated_at": ""
        }

    @staticmethod
    def save_session(session_id: str, data: Dict[str, Any]):
        filepath = SessionDatabase.get_session_filepath(session_id)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def delete_session(session_id: str):
        filepath = SessionDatabase.get_session_filepath(session_id)
        if os.path.exists(filepath):
            os.remove(filepath)

    @staticmethod
    def list_sessions() -> List[str]:
        sessions = []
        for filename in os.listdir(SESSIONS_DIR):
            if filename.endswith('.json'):
                session_id = filename[:-5]
                sessions.append(session_id)
        return sessions

    @staticmethod
    def get_all_sessions_data() -> List[Dict[str, Any]]:
        sessions_data = []
        for session_id in SessionDatabase.list_sessions():
            data = SessionDatabase.load_session(session_id)
            sessions_data.append(data)
        return sessions_data

    @staticmethod
    def get_user_sessions(user_id: str) -> List[Dict[str, Any]]:
        sessions_data = []
        for session_id in SessionDatabase.list_sessions():
            if session_id.startswith(f"{user_id}_"):
                data = SessionDatabase.load_session(session_id)
                sessions_data.append(data)
        return sessions_data

    @staticmethod
    def add_message(session_id: str, message: Dict[str, Any]):
        data = SessionDatabase.load_session(session_id)
        data["messages"].append(message)
        from datetime import datetime
        data["updated_at"] = datetime.utcnow().isoformat() + "Z"
        if not data["created_at"]:
            data["created_at"] = data["updated_at"]
        SessionDatabase.save_session(session_id, data)

    @staticmethod
    def get_messages(session_id: str) -> List[Dict[str, Any]]:
        data = SessionDatabase.load_session(session_id)
        return data.get("messages", [])

    @staticmethod
    def clear_messages(session_id: str):
        data = SessionDatabase.load_session(session_id)
        data["messages"] = []
        from datetime import datetime
        data["updated_at"] = datetime.utcnow().isoformat() + "Z"
        SessionDatabase.save_session(session_id, data)

    @staticmethod
    def delete_message(session_id: str, message_id: str) -> bool:
        data = SessionDatabase.load_session(session_id)
        messages = data.get("messages", [])
        for i, msg in enumerate(messages):
            if msg.get("id") == message_id:
                del messages[i]
                from datetime import datetime
                data["updated_at"] = datetime.utcnow().isoformat() + "Z"
                SessionDatabase.save_session(session_id, data)
                return True
        return False