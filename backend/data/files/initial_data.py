import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__))

initial_users = {
    "users": [
        {
            "id": "user-1",
            "username": "admin",
            "password": "admin123",
            "email": "admin@example.com",
            "avatar": "https://i.pravatar.cc/40?img=1",
            "role": "admin",
            "created_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": "user-2",
            "username": "user",
            "password": "user123",
            "email": "user@example.com",
            "avatar": "https://i.pravatar.cc/40?img=2",
            "role": "user",
            "created_at": "2024-01-02T00:00:00Z"
        }
    ]
}

initial_ai_roles = {
    "ai_roles": [
        {
            "id": "role-1",
            "name": "市场观察员",
            "avatar": "📊",
            "color": "#409EFF",
            "description": "擅长大盘及板块分析，掌握资金流向、行业热度及分化情况，能够发现潜在龙头股。主要负责整体市场板块观察，为个股和板块提供趋势参考。",
            "ability": "实时市场数据查询、趋势分析、投资建议",
            "personality": "专业、严谨、数据驱动",
            "created_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": "role-2",
            "name": "趋势分析师",
            "avatar": "📈",
            "color": "#67C23A",
            "description": "擅长对指定的股票专注长短期的趋势分析与股票预测，擅长识别金叉/死叉、极值点和趋势延续/反转信号。能量化支撑位、压力位及潜在价格区间，为操作提供参考。",
            "ability": "趋势预测、数据分析、决策支持",
            "personality": "敏锐、洞察、前瞻",
            "created_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": "role-3",
            "name": "技术分析师",
            "avatar": "🤖",
            "color": "#E6A23C",
            "description": "擅长对指定的股票做K线形态识别与波动分析，能够判断头肩顶、W底、M顶等典型技术形态，结合RSI、MACD、布林带等指标分析市场波动。主要负责发现形态信号、预测潜在反转和支撑压力区域。",
            "ability": "技术指标分析、图表解读、信号识别",
            "personality": "理性、细致、专业",
            "created_at": "2024-01-01T00:00:00Z"
        }
    ]
}

initial_friends = {
    "user-1": [
        {
            "id": "friend-1",
            "name": "市场观察员",
            "avatar": "📊",
            "type": "ai",
            "role_id": "role-1",
            "status": "online",
            "created_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": "friend-2",
            "name": "趋势分析师",
            "avatar": "📈",
            "type": "ai",
            "role_id": "role-2",
            "status": "online",
            "created_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": "friend-3",
            "name": "技术分析师",
            "avatar": "🤖",
            "type": "ai",
            "role_id": "role-3",
            "status": "online",
            "created_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": "friend-4",
            "name": "小明",
            "avatar": "👤",
            "type": "user",
            "status": "online",
            "created_at": "2024-01-02T00:00:00Z"
        },
        {
            "id": "friend-5",
            "name": "小红",
            "avatar": "👤",
            "type": "user",
            "status": "offline",
            "created_at": "2024-01-03T00:00:00Z"
        }
    ],
    "user-2": [
        {
            "id": "friend-6",
            "name": "市场观察员",
            "avatar": "📊",
            "type": "ai",
            "role_id": "role-1",
            "status": "online",
            "created_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": "friend-7",
            "name": "趋势分析师",
            "avatar": "📈",
            "type": "ai",
            "role_id": "role-2",
            "status": "online",
            "created_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": "friend-8",
            "name": "王五",
            "avatar": "👤",
            "type": "user",
            "status": "online",
            "created_at": "2024-01-04T00:00:00Z"
        }
    ]
}

initial_groups = {
    "user-1": [
        {
            "id": "group-1",
            "name": "股票讨论群",
            "avatar": "👥",
            "member_count": 4,
            "unread": 3,
            "members": ["friend-1", "friend-2", "friend-3", "friend-4"],
            "created_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": "group-2",
            "name": "AI助手群",
            "avatar": "🤖",
            "member_count": 3,
            "unread": 0,
            "members": ["friend-1", "friend-2", "friend-3"],
            "created_at": "2024-01-02T00:00:00Z"
        }
    ],
    "user-2": [
        {
            "id": "group-3",
            "name": "新手交流群",
            "avatar": "🌱",
            "member_count": 3,
            "unread": 2,
            "members": ["friend-6", "friend-7", "friend-8"],
            "created_at": "2024-01-05T00:00:00Z"
        }
    ]
}

initial_custom_agents = {
    "custom_agents": [
        {
            "id": "agent-1",
            "name": "股票分析师",
            "avatar": "📊",
            "ability": "擅长股票分析、趋势预测、投资建议",
            "personality": "专业、严谨、耐心",
            "description": "帮助用户分析股票走势，提供投资建议",
            "subscribed": True,
            "created_at": "2024-01-15T00:00:00Z"
        },
        {
            "id": "agent-2",
            "name": "生活助手",
            "avatar": "🤖",
            "ability": "日程管理、天气查询、新闻资讯",
            "personality": "友好、热情、乐于助人",
            "description": "您的智能生活助手，帮您管理日常事务",
            "subscribed": False,
            "created_at": "2024-01-16T00:00:00Z"
        }
    ]
}

initial_chat_history = {
    "chat_history": []
}

initial_sessions = {
    "user-1": [
        "user-1_agent_friend-1",
        "user-1_agent_friend-2",
        "user-1_group_group-1",
        "user-1_friend_friend-4"
    ],
    "user-2": [
        "user-2_agent_friend-6",
        "user-2_group_group-3",
        "user-2_friend_friend-8"
    ]
}

def init_data():
    files = [
        ("users.json", initial_users),
        ("ai_roles.json", initial_ai_roles),
        ("friends.json", initial_friends),
        ("groups.json", initial_groups),
        ("custom_agents.json", initial_custom_agents),
        ("chat_history.json", initial_chat_history),
        ("sessions.json", initial_sessions)
    ]
    
    for filename, data in files:
        filepath = os.path.join(DATA_DIR, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Created {filename}")
        else:
            print(f"{filename} already exists")

def reset_data():
    files = [
        ("users.json", initial_users),
        ("ai_roles.json", initial_ai_roles),
        ("friends.json", initial_friends),
        ("groups.json", initial_groups),
        ("custom_agents.json", initial_custom_agents),
        ("chat_history.json", initial_chat_history),
        ("sessions.json", initial_sessions)
    ]
    for filename, data in files:
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Reset {filename}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_data()
    else:
        init_data()