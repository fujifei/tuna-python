from datetime import datetime
from typing import List, Optional
from database.database import get_db
from models.user import UserInfo


def create_user_info(user: UserInfo) -> int:
    """创建用户信息"""
    db = get_db()
    query = """INSERT INTO user_info_tab (name, email, phone, hobby, age, address, status, created_at, updated_at) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    now = datetime.now()
    cursor = db.cursor()
    try:
        cursor.execute(query, (
            user.name, user.email, user.phone, user.hobby, user.age,
            user.address, "pending", now, now
        ))
        db.commit()
        return cursor.lastrowid
    finally:
        cursor.close()


def get_all_users() -> List[UserInfo]:
    """获取所有用户"""
    db = get_db()
    query = """SELECT id, name, email, phone, hobby, age, address, status, created_at, updated_at 
               FROM user_info_tab ORDER BY created_at DESC"""
    
    users = []
    cursor = db.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            user = UserInfo(
                id=row['id'],
                name=row['name'],
                email=row['email'],
                phone=row['phone'],
                hobby=row['hobby'],
                age=row['age'],
                address=row.get('address', ''),
                status=row['status'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            users.append(user)
    finally:
        cursor.close()
    
    return users


def get_user_by_id(user_id: int) -> Optional[UserInfo]:
    """根据ID获取用户"""
    db = get_db()
    query = """SELECT id, name, email, phone, hobby, age, address, status, created_at, updated_at 
               FROM user_info_tab WHERE id = %s"""
    
    cursor = db.cursor()
    try:
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        if not row:
            return None
        
        return UserInfo(
            id=row['id'],
            name=row['name'],
            email=row['email'],
            phone=row['phone'],
            hobby=row['hobby'],
            age=row['age'],
            address=row.get('address', ''),
            status=row['status'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
    finally:
        cursor.close()


def update_user_status(user_id: int, status: str) -> None:
    """更新用户状态"""
    db = get_db()
    query = """UPDATE user_info_tab SET status = %s, updated_at = %s WHERE id = %s"""
    
    now = datetime.now()
    cursor = db.cursor()
    try:
        cursor.execute(query, (status, now, user_id))
        db.commit()
    finally:
        cursor.close()


def delete_user(user_id: int) -> None:
    """删除用户"""
    db = get_db()
    query = """DELETE FROM user_info_tab WHERE id = %s"""
    
    cursor = db.cursor()
    try:
        cursor.execute(query, (user_id,))
        db.commit()
    finally:
        cursor.close()

