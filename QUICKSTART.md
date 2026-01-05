# 快速启动指南

## 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

## 2. 确保数据库已初始化

确保MySQL服务正在运行，并且数据库和表已经创建（参考原项目的sql/init.sql）。

## 3. 启动后端服务

### 方式1：使用Python直接运行（推荐）

打开两个终端窗口：

**终端1 - 启动API服务（端口8712）：**
```bash
cd backend
python api/main.py
```

**终端2 - 启动Admin服务（端口8713）：**
```bash
cd backend
python admin/main.py
```

### 方式2：使用启动脚本

**终端1 - 启动API服务：**
```bash
cd backend
./run_api.sh
```

**终端2 - 启动Admin服务：**
```bash
cd backend
./run_admin.sh
```

启动后，你会看到：
- API服务（用户端）运行在: http://localhost:8712
- Admin服务（管理端）运行在: http://localhost:8713

## 4. 访问前端页面

### 用户端
直接在浏览器中打开文件：
```
frontend/user/index.html
```

或者使用本地服务器（推荐）：
```bash
cd frontend/user
python3 -m http.server 3000
# 然后访问 http://localhost:3000
```

### 管理端
直接在浏览器中打开文件：
```
frontend/admin/index.html
```

或者使用本地服务器（推荐）：
```bash
cd frontend/admin
python3 -m http.server 3001
# 然后访问 http://localhost:3001
```

## 测试流程

1. 在用户端页面填写并提交用户资料
2. 在管理端页面查看提交的用户列表
3. 在管理端点击"通过"或"拒绝"按钮进行审核
4. 审核后，用户状态会更新并在列表中显示

## 注意事项

- 确保MySQL服务正在运行且可以连接到指定的端口（默认6666）
- 确保数据库和表已经创建
- 如果遇到CORS问题，确保后端服务已启动
- 前端页面需要与后端服务在同一网络环境下，或者修改前端代码中的API地址

