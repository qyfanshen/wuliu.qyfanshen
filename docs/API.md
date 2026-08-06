# API Reference

> 物流数字化管理平台 的接口文档。模块：flask_demo

## 通用约定

- 基础路径：`/api/`
- 请求/响应：JSON
- 鉴权：除登录接口外，所有接口需要带 `Authorization: Bearer <token>` 或 Cookie 会话
- 限流：默认每 IP 每分钟 60 次（可由 `api/rate_limit.php` 或中间件调整）
- 错误格式：
  ```json
  { "code": 400, "message": "Invalid parameter", "data": null }
  ```


## Flask 演示后端（`api_demo.py`）

```bash
pip install flask flask-cors
python api_demo.py
# → http://localhost:5000
```

接口示例：
- `GET  /api/members` — 商会会员列表
- `GET  /api/vehicles` — 车辆列表
- `GET  /api/routes` — 物流线路列表
- `GET  /api/credit/<member_id>` — 会员信用分
