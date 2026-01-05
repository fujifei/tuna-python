import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# 添加backend目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import load_config
from database.database import init_db, close_db
from models.user import UserInfo, CreateUserRequest
from models import user_repository

app = Flask(__name__)
CORS(app)  # 启用CORS支持

cfg = None


def setup_routes():
    """设置路由"""
    @app.route('/api/submit', methods=['POST'])
    def submit_user_info():
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid request body"}), 400

            # 验证必填字段
            required_fields = ['name', 'email', 'phone', 'hobby', 'age', 'address']
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400

            # 验证邮箱格式
            if '@' not in data['email']:
                return jsonify({"error": "Invalid email format"}), 400

            # 验证年龄
            age = data['age']
            if not isinstance(age, int) or age < 1 or age > 150:
                return jsonify({"error": "Age must be between 1 and 150"}), 400

            user = UserInfo(
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                hobby=data['hobby'],
                age=age,
                address=data['address']
            )

            user_id = user_repository.create_user_info(user)
            user.id = user_id

            return jsonify({
                "message": "User info submitted successfully",
                "id": user_id
            }), 200

        except Exception as e:
            return jsonify({"error": f"Failed to save user info: {str(e)}"}), 500

    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "ok"}), 200


def main():
    global cfg
    cfg = load_config()

    # 初始化数据库
    try:
        init_db(cfg)
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        sys.exit(1)

    # 设置路由
    setup_routes()

    # 启动服务器
    print(f"API server starting on port {cfg.api_port}")
    try:
        app.run(host='0.0.0.0', port=int(cfg.api_port), debug=False)
    except KeyboardInterrupt:
        print("\nShutting down API server...")
    finally:
        close_db()
        print("API server exited")


if __name__ == '__main__':
    main()

