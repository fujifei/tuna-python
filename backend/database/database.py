import pymysql
from typing import Optional
from config.config import Config

_db: Optional[pymysql.Connection] = None


def init_db(cfg: Config) -> None:
    """初始化数据库连接"""
    global _db
    try:
        _db = pymysql.connect(
            host=cfg.db_host,
            port=int(cfg.db_port),
            user=cfg.db_user,
            password=cfg.db_password,
            database=cfg.db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        # 设置连接池参数
        _db.ping(reconnect=True)
        print(f"Database connected: {cfg.db_host}:{cfg.db_port}/{cfg.db_name}")
    except Exception as e:
        raise Exception(f"Failed to initialize database: {e}")


def close_db() -> None:
    """关闭数据库连接"""
    global _db
    if _db:
        _db.close()
        _db = None


def get_db() -> pymysql.Connection:
    """获取数据库连接"""
    if _db is None:
        raise Exception("Database not initialized")
    return _db

