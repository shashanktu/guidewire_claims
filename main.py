from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import init_db, get_session, seed_from_json, Claim

app = FastAPI(title="Guidewire Claims API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VALID_STATUSES = {"Open", "InReview", "Approved", "Closed", "Denied"}


class StatusUpdateRequest(BaseModel):
    claimStatus: str


@app.on_event("startup")
def on_startup():
    # Create the claims table if it does not already exist.
    init_db()


@app.post("/admin/seed")
def seed_database():
    """
    One-time (idempotent) utility to load claims_data.json into the
    Retool DB `claims` table. Safe to call multiple times; existing
    claim numbers are skipped.
    """
    try:
        result = seed_from_json("claims_data.json")
        return {"status": "ok", **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Seeding failed: {e}")


@app.get("/get_records")
def read_root(db: Session = Depends(get_session)):
    claims = db.query(Claim).all()
    return {"count": len(claims), "claims": [c.to_dict() for c in claims]}

@app.get("/claim_numbers")
def get_claim_numbers(db: Session = Depends(get_session)):
    claims = db.query(Claim.claimNumber, Claim.policyNumber, Claim.claimStatus).all()
    return [
        {"claimNumber": c.claimNumber, "policyNumber": c.policyNumber, "claimStatus": c.claimStatus}
        for c in claims
    ]

@app.get("/claim/{claim_number}")
def get_claim_by_number(claim_number: str, db: Session = Depends(get_session)):
    claim = db.query(Claim).filter(Claim.claimNumber == claim_number).first()
    if not claim:
        return {"error": "Claim not found"}
    return claim.to_dict()

@app.put("/claim/{claim_number}/status")
def update_claim_status(
    claim_number: str, payload: StatusUpdateRequest, db: Session = Depends(get_session)
):
    if payload.claimStatus not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status '{payload.claimStatus}'. Valid statuses are: {sorted(VALID_STATUSES)}",
        )

    try:
        claim = db.query(Claim).filter(Claim.claimNumber == claim_number).first()
        if not claim:
            raise HTTPException(status_code=404, detail=f"Claim '{claim_number}' not found")

        claim.claimStatus = payload.claimStatus
        db.commit()
        db.refresh(claim)
        return claim.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error updating claim status: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the claim status: {e}")

@app.get("/applications/")
def get_applications(): 
  return {"applications": ["RSS Feed", "Guidewire ClaimCenter", "Guidewire BillingCenter"]}


