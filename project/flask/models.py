﻿from database import Base
from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey


class RolesUsers(Base):
    __tablename__ = "roles_users"
    id = Column(Integer(), primary_key=True)
    user_id = Column("user_id", Integer(), ForeignKey("user.id"))
    role_id = Column("role_id", Integer(), ForeignKey("role.id"))


class Role(Base, RoleMixin):
    __tablename__ = "role"
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(Base, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    active = Column(Boolean())
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    roles = relationship(
        "Role",
        secondary="roles_users",
        backref=backref("users", lazy="dynamic"),
    )
