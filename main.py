from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/applications/")
def get_applications(): 
  return {"applications": ["RSS Feed", "Guidewire ClaimCenter", "Guidewire BillingCenter"]}


