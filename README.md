# Tuna Python 前后端分离项目

这是Tuna项目的Python版本，使用Flask框架实现，功能与Go版本完全一致。

## 项目结构

```
tuna-python/
├── backend/              # 后端代码
│   ├── api/             # 用户端API模块
│   │   └── main.py
│   ├── admin/           # 管理端API模块
│   │   └── main.py
│   ├── config/          # 配置模块
│   │   └── config.py
│   ├── database/        # 数据库连接模块
│   │   └── database.py
│   ├── models/          # 数据模型和仓库
│   │   ├── user.py
│   │   └── user_repository.py
│   ├── config.yaml      # 配置文件
│   └── requirements.txt # Python依赖
├── frontend/            # 前端页面
│   ├── user/           # 用户端页面
│   │   └── index.html
│   └── admin/          # 管理端页面
│       └── index.html
└── README.md
```

## 数据库配置

- Host: 127.0.0.1
- Port: 6666
- User: agile
- Password: agile
- Database: tuna
- Table: user_info_tab

## 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

## 运行后端

### 启动API服务（用户端，端口8712）

```bash
cd backend
python api/main.py
```

### 启动Admin服务（管理端，端口8713）

```bash
cd backend
python admin/main.py
```

或者使用两个终端分别运行：

```bash
# 终端1
cd backend
python api/main.py

# 终端2
cd backend
python admin/main.py
```

后端将启动两个服务：
- API服务（用户端）: http://localhost:8712
- Admin服务（管理端）: http://localhost:8713

## 访问前端

- 用户端: 在浏览器中打开 `frontend/user/index.html`
- 管理端: 在浏览器中打开 `frontend/admin/index.html`

或者使用本地服务器（推荐）：

```bash
# 用户端
cd frontend/user
python3 -m http.server 3000
# 然后访问 http://localhost:3000

# 管理端
cd frontend/admin
python3 -m http.server 3001
# 然后访问 http://localhost:3001
```

## API接口

### 用户端API (端口8712)

- `POST /api/submit` - 提交用户资料
  ```json
  {
    "name": "张三",
    "email": "zhangsan@example.com",
    "phone": "13800138000",
    "hobby": "阅读",
    "age": 25,
    "address": "北京市朝阳区"
  }
  ```

- `GET /api/health` - 健康检查

### 管理端API (端口8713)

- `GET /admin/users` - 获取所有用户列表
- `PUT /admin/users/:id/status` - 更新用户审核状态
  ```json
  {
    "status": "approved"  // 或 "rejected"
  }
  ```
- `DELETE /admin/users/:id` - 删除用户
- `GET /admin/health` - 健康检查

## 环境变量（可选）

可以通过环境变量覆盖默认配置：

- `DB_HOST` - 数据库主机（默认: 127.0.0.1）
- `DB_PORT` - 数据库端口（默认: 6666）
- `DB_USER` - 数据库用户名（默认: agile）
- `DB_PASSWORD` - 数据库密码（默认: agile）
- `DB_NAME` - 数据库名称（默认: tuna）
- `API_PORT` - API服务端口（默认: 8712）
- `ADMIN_PORT` - Admin服务端口（默认: 8713）

## 注意事项

- 确保MySQL服务正在运行且可以连接到指定的端口
- 确保数据库和表已经创建（参考原项目的sql/init.sql）
- 如果遇到CORS问题，确保后端服务已启动
- 前端页面需要与后端服务在同一网络环境下，或者修改前端代码中的API地址

