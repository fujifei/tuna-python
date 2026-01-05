import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# 添加backend目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import load_config
from database.database import init_db, close_db
from models import user_repository

app = Flask(__name__)
CORS(app)  # 启用CORS支持

cfg = None


def setup_routes():
    """设置路由"""
    @app.route('/admin/users', methods=['GET'])
    def get_users():
        try:
            users = user_repository.get_all_users()
            users_dict = [user.to_dict() for user in users]
            return jsonify({"users": users_dict}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to fetch users: {str(e)}"}), 500

    @app.route('/admin/users/<int:user_id>/status', methods=['PUT'])
    def update_user_status(user_id):
        try:
            data = request.get_json()
            if not data or 'status' not in data:
                return jsonify({"error": "Missing status field"}), 400

            status = data['status']
            if status not in ['approved', 'rejected']:
                return jsonify({"error": "Status must be 'approved' or 'rejected'"}), 400

            # 检查用户是否存在
            user = user_repository.get_user_by_id(user_id)
            if user is None:
                return jsonify({"error": "User not found"}), 404

            user_repository.update_user_status(user_id, status)
            return jsonify({"message": "User status updated successfully"}), 200

        except Exception as e:
            return jsonify({"error": f"Failed to update user status: {str(e)}"}), 500

    @app.route('/admin/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        try:
            # 检查用户是否存在
            user = user_repository.get_user_by_id(user_id)
            if user is None:
                return jsonify({"error": "User not found"}), 404

            user_repository.delete_user(user_id)
            return jsonify({"message": "User deleted successfully"}), 200

        except Exception as e:
            return jsonify({"error": f"Failed to delete user: {str(e)}"}), 500

    @app.route('/admin/health', methods=['GET'])
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
    print(f"Admin server starting on port {cfg.admin_port}")
    try:
        app.run(host='0.0.0.0', port=int(cfg.admin_port), debug=False)
    except KeyboardInterrupt:
        print("\nShutting down Admin server...")
    finally:
        close_db()
        print("Admin server exited")


if __name__ == '__main__':
    main()

