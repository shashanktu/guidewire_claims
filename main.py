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

with open("claims_data.json") as f:
    claims_data = json.load(f)

VALID_STATUSES = {"Open", "InReview", "Approved", "Closed", "Denied"}


class StatusUpdateRequest(BaseModel):
    claimStatus: str


@app.get("/get_records")
def read_root():
    return {"count": len(claims_data), "claims": claims_data}

@app.get("/claim_numbers")
def get_claim_numbers():
    return [{"claimNumber": claim["claimNumber"], "policyNumber": claim["policyNumber"], "claimStatus": claim["claimStatus"]} for claim in claims_data]

@app.get("/claim/CLM-2025-00123456")
def get_claim_1():
    return claims_data[0]

@app.get("/claim/CLM-2025-001312")
def get_claim_2():
    return claims_data[1]

@app.get("/claim/CLM-2025-001388")
def get_claim_3():
    return claims_data[2]

@app.get("/claim/CLM-2025-001447")
def get_claim_4():
    return claims_data[3]

@app.get("/claim/CLM-2025-001509")
def get_claim_5():
    return claims_data[4]

@app.get("/claim/{claim_number}")
def get_claim_by_number(claim_number: str):
    for claim in claims_data:
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

    try:
        for claim in claims_data:
            if claim["claimNumber"] == claim_number:
                claim["claimStatus"] = payload.claimStatus
                with open("claims_data.json", "w") as f:
                    json.dump(claims_data, f, indent=2)
            return claim

        
    except Exception as e:
        print(f"Error updating claim status: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the claim status: {e}")

@app.get("/applications/")
def get_applications(): 
  return {"applications": ["RSS Feed", "Guidewire ClaimCenter", "Guidewire BillingCenter"]}


