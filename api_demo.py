"""
物流商会数字化管理平台 - 后端 API 演示
==========================================

这是一个 Flask 后端 API 演示文件，展示如何为前端提供数据接口。

使用方法：
1. 安装依赖: pip install flask flask-cors
2. 运行服务: python api_demo.py
3. 访问: http://localhost:5000
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 模拟数据库
members_db = [
    {
        "id": 1,
        "name": "XX物流有限公司",
        "type": "enterprise",
        "level": "core",
        "credit_score": 98,
        "routes": ["上海-北京", "广州-深圳"],
        "vehicles": 45,
        "join_date": "2025-01-15",
        "status": "active"
    },
    {
        "id": 2,
        "name": "YY运输公司",
        "type": "enterprise",
        "level": "quality",
        "credit_score": 92,
        "routes": ["成都-重庆", "武汉-上海"],
        "vehicles": 32,
        "join_date": "2025-03-20",
        "status": "active"
    }
]

routes_db = [
    {
        "id": 1,
        "name": "上海 → 北京",
        "publish_count": 156,
        "trade_count": 128,
        "conversion_rate": 0.821
    },
    {
        "id": 2,
        "name": "广州 → 深圳",
        "publish_count": 142,
        "trade_count": 115,
        "conversion_rate": 0.810
    }
]

# ==================== 首页数据 ====================

@app.route('/api/stats/overview', methods=['GET'])
def get_stats_overview():
    """获取首页统计概览数据"""
    return jsonify({
        "success": True,
        "data": {
            "memberCount": 1258,
            "routeCount": 346,
            "tradeCount": 892,
            "creditScore": 95.6,
            "trends": {
                "memberGrowth": 12.5,
                "routeGrowth": 8.3,
                "tradeGrowth": 23.7,
                "creditGrowth": 2.1
            }
        }
    })


# ==================== 会员管理 ====================

@app.route('/api/members', methods=['GET'])
def get_members():
    """获取会员列表"""
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))
    level = request.args.get('level', None)
    
    # 过滤
    filtered = members_db
    if level:
        filtered = [m for m in members_db if m['level'] == level]
    
    # 分页
    total = len(filtered)
    start = (page - 1) * size
    end = start + size
    items = filtered[start:end]
    
    return jsonify({
        "success": True,
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "size": size
        }
    })


@app.route('/api/members/<int:member_id>', methods=['GET'])
def get_member_detail(member_id):
    """获取会员详情"""
    member = next((m for m in members_db if m['id'] == member_id), None)
    
    if not member:
        return jsonify({
            "success": False,
            "message": "会员不存在"
        }), 404
    
    return jsonify({
        "success": True,
        "data": member
    })


@app.route('/api/members/stats', methods=['GET'])
def get_member_stats():
    """获取会员统计数据"""
    return jsonify({
        "success": True,
        "data": {
            "total": 1258,
            "by_level": {
                "core": {"count": 126, "percent": 10.0},
                "quality": {"count": 258, "percent": 20.5},
                "normal": {"count": 687, "percent": 54.6},
                "warning": {"count": 187, "percent": 14.9}
            },
            "new_this_month": 45,
            "active_rate": 0.78
        }
    })


# ==================== 线路管理 ====================

@app.route('/api/routes', methods=['GET'])
def get_routes():
    """获取线路列表"""
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))
    
    total = len(routes_db)
    start = (page - 1) * size
    end = start + size
    items = routes_db[start:end]
    
    return jsonify({
        "success": True,
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "size": size
        }
    })


@app.route('/api/routes/hot', methods=['GET'])
def get_hot_routes():
    """获取热门线路 TOP10"""
    sorted_routes = sorted(routes_db, key=lambda x: x['trade_count'], reverse=True)[:10]
    
    return jsonify({
        "success": True,
        "data": sorted_routes
    })


# ==================== 供需撮合 ====================

@app.route('/api/trades/publish', methods=['POST'])
def publish_trade():
    """发布供需信息"""
    data = request.json
    
    # 验证必填字段
    required_fields = ['type', 'from_city', 'to_city', 'quantity']
    for field in required_fields:
        if field not in data:
            return jsonify({
                "success": False,
                "message": f"缺少必填字段: {field}"
            }), 400
    
    # 模拟保存到数据库
    trade_id = random.randint(1000, 9999)
    
    return jsonify({
        "success": True,
        "data": {
            "id": trade_id,
            "message": "发布成功"
        }
    })


@app.route('/api/trades/trend', methods=['GET'])
def get_trade_trend():
    """获取交易趋势数据"""
    days = int(request.args.get('days', 7))
    
    # 生成模拟数据
    data = []
    for i in range(days):
        data.append({
            "date": f"2026-07-{23+i:02d}",
            "supply_count": random.randint(80, 150),
            "demand_count": random.randint(60, 120),
            "trade_count": random.randint(40, 80)
        })
    
    return jsonify({
        "success": True,
        "data": data
    })


# ==================== 风控管理 ====================

@app.route('/api/risk/alerts', methods=['GET'])
def get_risk_alerts():
    """获取风险预警信息"""
    return jsonify({
        "success": True,
        "data": [
            {
                "id": 1,
                "type": "critical",
                "title": "资质逾期提醒",
                "description": "12家企业资质即将到期，请及时提醒续期",
                "time": "2小时前"
            },
            {
                "id": 2,
                "type": "warning",
                "title": "纠纷待处理",
                "description": "新增3起运费纠纷，等待调解处理",
                "time": "5小时前"
            },
            {
                "id": 3,
                "type": "info",
                "title": "会费催缴",
                "description": "25家企业会费已逾期，需要进行催缴",
                "time": "1天前"
            }
        ]
    })


# ==================== 数据大屏 ====================

@app.route('/api/dashboard/realtime', methods=['GET'])
def get_realtime_data():
    """获取实时数据（用于大屏展示）"""
    return jsonify({
        "success": True,
        "data": {
            "timestamp": datetime.now().isoformat(),
            "online_members": random.randint(200, 400),
            "today_trades": random.randint(50, 100),
            "capacity_usage": random.uniform(0.6, 0.9),
            "hot_routes": [
                {"name": "上海→北京", "count": random.randint(10, 30)},
                {"name": "广州→深圳", "count": random.randint(8, 25)},
                {"name": "成都→重庆", "count": random.randint(6, 20)}
            ]
        }
    })


# ==================== 认证接口 ====================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # 模拟验证（实际应查询数据库）
    if username == 'admin' and password == '123456':
        return jsonify({
            "success": True,
            "data": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "user": {
                    "id": 1,
                    "username": username,
                    "role": "admin",
                    "name": "管理员"
                }
            }
        })
    else:
        return jsonify({
            "success": False,
            "message": "用户名或密码错误"
        }), 401


@app.route('/api/auth/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.json
    
    # 验证必填字段
    required_fields = ['name', 'phone', 'username', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({
                "success": False,
                "message": f"缺少必填字段: {field}"
            }), 400
    
    # 模拟保存到数据库
    user_id = random.randint(1000, 9999)
    
    return jsonify({
        "success": True,
        "data": {
            "id": user_id,
            "message": "注册成功"
        }
    })


# ==================== 运行服务 ====================

if __name__ == '__main__':
    print("=" * 60)
    print("物流商会数字化管理平台 - API 服务已启动")
    print("=" * 60)
    print(f"访问地址: http://localhost:5000")
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("\n可用接口:")
    print("  GET  /api/stats/overview      - 获取统计概览")
    print("  GET  /api/members             - 获取会员列表")
    print("  GET  /api/members/<id>        - 获取会员详情")
    print("  GET  /api/routes              - 获取线路列表")
    print("  POST /api/trades/publish      - 发布供需信息")
    print("  GET  /api/risk/alerts         - 获取风险预警")
    print("  GET  /api/dashboard/realtime  - 获取实时数据")
    print("  POST /api/auth/login          - 用户登录")
    print("  POST /api/auth/register       - 用户注册")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
