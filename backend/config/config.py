import os
import yaml
from pathlib import Path
from typing import Optional


class Config:
    def __init__(self):
        self.db_host: str = "127.0.0.1"
        self.db_port: str = "6666"
        self.db_user: str = "agile"
        self.db_password: str = "agile"
        self.db_name: str = "tuna"
        self.api_port: str = "8712"
        self.admin_port: str = "8713"

    def get_dsn(self) -> str:
        """生成MySQL连接DSN"""
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4"

    def get_mysql_dsn(self) -> str:
        """生成MySQL原生连接字符串（用于pymysql）"""
        return f"{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4"


def get_config_path() -> Optional[str]:
    """获取配置文件路径"""
    # 首先检查环境变量
    if path := os.getenv("CONFIG_PATH"):
        return path

    # 获取当前工作目录
    wd = os.getcwd()

    # 尝试多个可能的路径
    paths = [
        os.path.join(wd, "config.yaml"),
        os.path.join(wd, "backend", "config.yaml"),
        os.path.join(os.path.dirname(wd), "backend", "config.yaml"),
    ]

    for path in paths:
        if os.path.exists(path):
            return path

    return None


def load_from_file(path: str) -> dict:
    """从YAML文件加载配置"""
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_env(key: str, default: str) -> str:
    """获取环境变量，如果不存在则返回默认值"""
    return os.getenv(key, default)


def load_config() -> Config:
    """加载配置"""
    cfg = Config()

    # 尝试从配置文件加载
    config_path = get_config_path()
    if config_path:
        try:
            file_cfg = load_from_file(config_path)
            if file_cfg:
                db_cfg = file_cfg.get("database", {})
                ports_cfg = file_cfg.get("ports", {})

                cfg.db_host = get_env("DB_HOST", db_cfg.get("host", cfg.db_host))
                cfg.db_port = get_env("DB_PORT", db_cfg.get("port", cfg.db_port))
                cfg.db_user = get_env("DB_USER", db_cfg.get("user", cfg.db_user))
                cfg.db_password = get_env("DB_PASSWORD", db_cfg.get("password", cfg.db_password))
                cfg.db_name = get_env("DB_NAME", db_cfg.get("name", cfg.db_name))
                cfg.api_port = get_env("API_PORT", ports_cfg.get("api", cfg.api_port))
                cfg.admin_port = get_env("ADMIN_PORT", ports_cfg.get("admin", cfg.admin_port))
                return cfg
        except Exception:
            pass

    # 如果配置文件不存在或读取失败，使用默认值
    cfg.db_host = get_env("DB_HOST", "127.0.0.1")
    cfg.db_port = get_env("DB_PORT", "6666")
    cfg.db_user = get_env("DB_USER", "agile")
    cfg.db_password = get_env("DB_PASSWORD", "agile")
    cfg.db_name = get_env("DB_NAME", "tuna")
    cfg.api_port = get_env("API_PORT", "8712")
    cfg.admin_port = get_env("ADMIN_PORT", "8713")

    return cfg

