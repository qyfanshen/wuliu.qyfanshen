# Architecture

## 概述

- **项目**：物流数字化管理平台
- **类型**：静态落地站 + Flask 后端演示
- **技术栈**：HTML5 · CSS3 · Vanilla JavaScript · Python 3 + Flask · Nginx

## 模块划分







- **Flask 演示后端**：`api_demo.py` 提供商会、车辆、线路、信用分等内存数据接口。

## 数据流

```
[Browser]
   │
   ├─── 静态资源（Nginx / CDN）
   │


   ├─── /api/* (Flask demo) ──► [in-memory mock data]
   │
   └─── /admin/*（如适用）
```

## 安全设计

- HTTPS 强制（301 跳转）
- 安全响应头：CSP / X-Frame-Options / Referrer-Policy / Permissions-Policy
- 敏感文件（`.env`、`*.bak.*`、`storage/`、`.user.ini`）通过 `.gitignore` + Nginx deny 双重保护
- 接口限流（PHP 站 `api/rate_limit.php`）
- CSRF token 校验（PHP 站 `includes/csrf.php`）
