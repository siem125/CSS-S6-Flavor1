from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base

class Repo(Base):
    __tablename__ = "repos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)

    scans = relationship("Scan", back_populates="repo")


class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repos.id"), nullable=False)
    sha = Column(String)
    event = Column(String)
    status = Column(String)
    block = Column(Boolean, default=False)
    reason = Column(String)
    vulnerability_count = Column(Integer, default=0)
    duration = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    repo = relationship("Repo", back_populates="scans")
    vulnerabilities = relationship(
        "Vulnerability",
        back_populates="scan",
        cascade="all, delete-orphan"
    )


class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"))
    vulnerability_id = Column(String)
    severity = Column(String)
    package_name = Column(String)
    installed_version = Column(String)
    fixed_version = Column(String)
    description = Column(String)

    scan = relationship(
        "Scan",
        back_populates="vulnerabilities"
    )