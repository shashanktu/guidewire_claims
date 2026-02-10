from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_records")
def read_root():
    sample={
  "count": 5,
  "claims": [
    {
      "claimNumber": "CLM-2025-00123456",
      "policyNumber": "PLC-AUTO-458912",
      "lineOfBusiness": "Auto",
      "lossDate": "2025-01-12",
      "reportedDate": "2025-01-13T09:42:18Z",
      "claimStatus": "Open",
      "lossCause": "Collision",
      "jurisdiction": "CA",
      "insured": {
        "insuredId": "INS-102345",
        "name": "Tudum Venkanna"
      },
      "claimant": {
        "claimantId": "CLMT-334589",
        "name": "Sarah Thompson",
        "type": "ThirdParty"
      },
      "coverages": [
        {
          "coverageType": "CollisionCoverage",
          "limit": 50000,
          "deductible": 500
        }
      ],
      "financials": {
        "totalPaid": 12450.75,
        "totalReserved": 6000.00,
        "totalIncurred": 18450.75,
        "currency": "USD"
      },
      "assignedAdjuster": {
        "adjusterId": "ADJ-77821",
        "name": "Mark Reynolds",
        "office": "Los Angeles Claims Office"
      },
      "exposures": [
        {
          "exposureType": "VehicleDamage",
          "status": "Open",
          "severity": "Medium"
        }
      ]
    },

    {
      "claimNumber": "CLM-2025-001312",
      "policyNumber": "PLC-WC-774521",
      "lineOfBusiness": "WorkersComp",
      "lossDate": "2025-02-03",
      "reportedDate": "2025-02-03T14:12:05Z",
      "claimStatus": "InReview",
      "lossCause": "SlipAndFall",
      "jurisdiction": "TX",
      "insured": {
        "insuredId": "INS-778912",
        "name": "Apex Logistics Inc."
      },
      "claimant": {
        "claimantId": "CLMT-221908",
        "name": "Carlos Hernandez",
        "type": "Employee"
      },
      "coverages": [
        {
          "coverageType": "MedicalOnly",
          "statutoryState": "TX"
        }
      ],
      "financials": {
        "totalPaid": 3820.40,
        "totalReserved": 3000.00,
        "totalIncurred": 6820.40,
        "currency": "USD"
      },
      "assignedAdjuster": {
        "adjusterId": "ADJ-44512",
        "name": "Anita Verma",
        "office": "Dallas WC Unit"
      },
      "exposures": [
        {
          "exposureType": "Medical",
          "status": "Open",
          "severity": "Low"
        }
      ]
    },

    {
      "claimNumber": "CLM-2025-001388",
      "policyNumber": "PLC-PROP-991204",
      "lineOfBusiness": "Property",
      "lossDate": "2025-01-28",
      "reportedDate": "2025-01-29T08:05:44Z",
      "claimStatus": "Open",
      "lossCause": "Fire",
      "jurisdiction": "FL",
      "insured": {
        "insuredId": "INS-556701",
        "name": "Emily Carter"
      },
      "claimant": {
        "claimantId": "CLMT-556701",
        "name": "Emily Carter",
        "type": "FirstParty"
      },
      "coverages": [
        {
          "coverageType": "DwellingCoverage",
          "limit": 250000,
          "deductible": 2500
        }
      ],
      "financials": {
        "totalPaid": 44300.00,
        "totalReserved": 50000.00,
        "totalIncurred": 94300.00,
        "currency": "USD"
      },
      "assignedAdjuster": {
        "adjusterId": "ADJ-99018",
        "name": "Steven Collins",
        "office": "Orlando Property Hub"
      },
      "exposures": [
        {
          "exposureType": "PropertyDamage",
          "status": "Open",
          "severity": "High"
        }
      ]
    },

    {
      "claimNumber": "CLM-2025-001447",
      "policyNumber": "PLC-HLTH-662198",
      "lineOfBusiness": "Health",
      "lossDate": "2025-02-10",
      "reportedDate": "2025-02-11T11:30:02Z",
      "claimStatus": "Approved",
      "lossCause": "Illness",
      "jurisdiction": "NY",
      "insured": {
        "insuredId": "INS-889341",
        "name": "Michael Brown"
      },
      "claimant": {
        "claimantId": "CLMT-889341",
        "name": "Michael Brown",
        "type": "Member"
      },
      "coverages": [
        {
          "coverageType": "InpatientHospitalization",
          "networkType": "InNetwork"
        }
      ],
      "financials": {
        "totalPaid": 21675.90,
        "totalReserved": 0.00,
        "totalIncurred": 21675.90,
        "currency": "USD"
      },
      "assignedAdjuster": {
        "adjusterId": "ADJ-66309",
        "name": "Ritu Sharma",
        "office": "NY Health Operations"
      },
      "exposures": [
        {
          "exposureType": "MedicalTreatment",
          "status": "Closed",
          "severity": "Medium"
        }
      ]
    },

    {
      "claimNumber": "CLM-2025-001509",
      "policyNumber": "PLC-LIAB-338774",
      "lineOfBusiness": "GeneralLiability",
      "lossDate": "2025-01-19",
      "reportedDate": "2025-01-20T10:18:55Z",
      "claimStatus": "Closed",
      "lossCause": "PremisesLiability",
      "jurisdiction": "IL",
      "insured": {
        "insuredId": "INS-441203",
        "name": "GreenMart Retail LLC"
      },
      "claimant": {
        "claimantId": "CLMT-775401",
        "name": "Olivia Wilson",
        "type": "ThirdParty"
      },
      "coverages": [
        {
          "coverageType": "BodilyInjury",
          "limit": 1000000
        }
      ],
      "financials": {
        "totalPaid": 42150.00,
        "totalReserved": 0.00,
        "totalIncurred": 42150.00,
        "currency": "USD"
      },
      "assignedAdjuster": {
        "adjusterId": "ADJ-55011",
        "name": "David Nguyen",
        "office": "Chicago Liability Unit"
      },
      "exposures": [
        {
          "exposureType": "BodilyInjury",
          "status": "Closed",
          "severity": "Medium"
        }
      ]
    }
  ]
}

    return sample
