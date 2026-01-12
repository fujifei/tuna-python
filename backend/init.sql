-- Tuna项目数据库初始化脚本

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS tuna CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE tuna;

-- 创建用户信息表
CREATE TABLE IF NOT EXISTS user_info_tab (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    name VARCHAR(100) NOT NULL COMMENT '姓名',
    email VARCHAR(100) NOT NULL COMMENT '邮箱',
    phone VARCHAR(20) NOT NULL COMMENT '电话',
    hobby VARCHAR(200) DEFAULT '' COMMENT '爱好',
    age INT NOT NULL DEFAULT 0 COMMENT '年龄',
    address VARCHAR(500) DEFAULT '' COMMENT '地址',
    status VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '状态: pending, approved, rejected',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户信息表';
