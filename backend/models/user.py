from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserInfo:
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    phone: str = ""
    hobby: str = ""
    age: int = 0
    address: str = ""
    status: str = "pending"  # pending, approved, rejected
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "hobby": self.hobby,
            "age": self.age,
            "address": self.address,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


@dataclass
class CreateUserRequest:
    name: str
    email: str
    phone: str
    hobby: str
    age: int
    address: str


@dataclass
class UpdateStatusRequest:
    status: str  # approved or rejected

