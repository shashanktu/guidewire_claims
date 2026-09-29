"""
Database layer for the Guidewire Claims API.

Connects to a Retool DB (hosted PostgreSQL) instance using SQLAlchemy.
Provides a single `claims` table that stores the top-level scalar fields
as normal columns (for fast filtering/searching) and the nested JSON
structures (insured, claimant, coverages, financials, assignedAdjuster,
exposures) as JSON columns so the original document shape can be
reconstructed exactly.
"""

import os
import json

from sqlalchemy import create_engine, Column, String, Float, JSON, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Connection
# ---------------------------------------------------------------------------
# Retool DB connection string. Get this from Retool -> Resources -> your
# Retool DB -> "Connection details" (use the PostgreSQL connection string).
# Example: postgresql://retool:password@host.retooldb.com:5432/retool
DATABASE_URL = os.getenv("RETOOL_DB_URL") or os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "No database connection string found. Please set the RETOOL_DB_URL "
        "(or DATABASE_URL) environment variable to your Retool DB Postgres "
        "connection string."
    )

# SQLAlchemy requires the 'postgresql://' prefix (some providers give 'postgres://')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# Use JSONB on postgres, fall back to generic JSON elsewhere (e.g. sqlite for tests)
JSONType = JSONB if engine.dialect.name == "postgresql" else JSON


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
class Claim(Base):
    __tablename__ = "claims"

    claimNumber = Column(String, primary_key=True)
    policyNumber = Column(String, index=True)
    lineOfBusiness = Column(String, index=True)
    lossDate = Column(String)
    reportedDate = Column(String)
    claimStatus = Column(String, index=True)
    lossCause = Column(String)
    jurisdiction = Column(String)

    insured = Column(JSONType)
    claimant = Column(JSONType)
    coverages = Column(JSONType)
    financials = Column(JSONType)
    assignedAdjuster = Column(JSONType)
    exposures = Column(JSONType)

    def to_dict(self) -> dict:
        return {
            "claimNumber": self.claimNumber,
            "policyNumber": self.policyNumber,
            "lineOfBusiness": self.lineOfBusiness,
            "lossDate": self.lossDate,
            "reportedDate": self.reportedDate,
            "claimStatus": self.claimStatus,
            "lossCause": self.lossCause,
            "jurisdiction": self.jurisdiction,
            "insured": self.insured,
            "claimant": self.claimant,
            "coverages": self.coverages,
            "financials": self.financials,
            "assignedAdjuster": self.assignedAdjuster,
            "exposures": self.exposures,
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def init_db():
    """Create the claims table if it doesn't already exist."""
    Base.metadata.create_all(bind=engine)


def get_session():
    """FastAPI dependency that yields a DB session and closes it afterwards."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def seed_from_json(json_path: str = "claims_data.json"):
    """
    Populate the claims table from the local claims_data.json file.
    Only inserts claims that don't already exist (safe to re-run).
    """
    with open(json_path) as f:
        claims_data = json.load(f)

    session = SessionLocal()
    try:
        existing_ids = {row[0] for row in session.query(Claim.claimNumber).all()}
        inserted = 0

        for claim in claims_data:
            if claim["claimNumber"] in existing_ids:
                continue

            session.add(
                Claim(
                    claimNumber=claim.get("claimNumber"),
                    policyNumber=claim.get("policyNumber"),
                    lineOfBusiness=claim.get("lineOfBusiness"),
                    lossDate=claim.get("lossDate"),
                    reportedDate=claim.get("reportedDate"),
                    claimStatus=claim.get("claimStatus"),
                    lossCause=claim.get("lossCause"),
                    jurisdiction=claim.get("jurisdiction"),
                    insured=claim.get("insured"),
                    claimant=claim.get("claimant"),
                    coverages=claim.get("coverages"),
                    financials=claim.get("financials"),
                    assignedAdjuster=claim.get("assignedAdjuster"),
                    exposures=claim.get("exposures"),
                )
            )
            inserted += 1

        session.commit()
        return {"inserted": inserted, "skipped": len(claims_data) - inserted}
    finally:
        session.close()
