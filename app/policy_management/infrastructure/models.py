from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import date
from .db import Base

"""ORM models for Policy Management"""

"""Policy Status Model"""


class PolicyStatusModel(Base):
    __tablename__ = "policy_statuses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True, nullable=False)
    description = Column(String(100), nullable=True)

    # Relationship
    policies = relationship("PolicyModel", back_populates="status_rel")


"""Policy Type Model"""


class PolicyTypeModel(Base):
    __tablename__ = "policy_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True, nullable=False)
    description = Column(String(100), nullable=True)

    # Relationship
    policies = relationship("PolicyModel", back_populates="type_rel")


"""Policy Model"""


class PolicyModel(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    policy_number = Column(String(50), unique=True, nullable=False, index=True)
    insured_name = Column(String(200), nullable=False)

    # Premium information
    premium_amount = Column(Float, nullable=False)
    premium_currency = Column(String(3), nullable=False, default="GBP")

    # Period information
    period_start_date = Column(Date, nullable=False)
    period_end_date = Column(Date, nullable=False)

    # Foreign keys to status and type
    status_id = Column(Integer, ForeignKey("policy_statuses.id"), nullable=False)
    type_id = Column(Integer, ForeignKey("policy_types.id"), nullable=False)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    # Relationships
    status_rel = relationship("PolicyStatusModel", back_populates="policies")
    type_rel = relationship("PolicyTypeModel", back_populates="policies")
