from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

app = FastAPI(title="Guidewire Claims API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "claims_data.json"

VALID_STATUSES = {"Open", "InReview", "Approved", "Closed", "Denied"}


class StatusUpdateRequest(BaseModel):
    claimStatus: str


def load_claims():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_claims(claims):
    with open(DATA_FILE, "w") as f:
        json.dump(claims, f, indent=2)


@app.get("/get_records")
def read_root():
    claims = load_claims()
    return {"count": len(claims), "claims": claims}

@app.get("/claim_numbers")
def get_claim_numbers():
    claims = load_claims()
    return [
        {"claimNumber": c["claimNumber"], "policyNumber": c["policyNumber"], "claimStatus": c["claimStatus"]}
        for c in claims
    ]

@app.get("/claim/{claim_number}")
def get_claim_by_number(claim_number: str):
    claims = load_claims()
    for claim in claims:
        if claim["claimNumber"] == claim_number:
            return claim
    return {"error": "Claim not found"}

@app.put("/claim/{claim_number}/status")
def update_claim_status(claim_number: str, payload: StatusUpdateRequest):
    if payload.claimStatus not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status '{payload.claimStatus}'. Valid statuses are: {sorted(VALID_STATUSES)}",
        )

    claims = load_claims()
    for claim in claims:
        if claim["claimNumber"] == claim_number:
            claim["claimStatus"] = payload.claimStatus
            save_claims(claims)
            return claim

    raise HTTPException(status_code=404, detail=f"Claim '{claim_number}' not found")

@app.get("/applications/")
def get_applications(): 
  return {"applications": ["RSS Feed", "Guidewire ClaimCenter", "Guidewire BillingCenter"]}


