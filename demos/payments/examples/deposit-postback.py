from fastapi import FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from decimal import Decimal, ROUND_CEILING
import math

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DepositPostbackRequest(BaseModel):
    userId: str
    amount: Decimal
    currencyCode: str
    transactionId: str

@app.post("/v1/wallet/deposit-postback")
async def handle_deposit_done(
    request: DepositPostbackRequest,
    x_api_key: str = Header(None, alias="X-API-KEY")
):
    if x_api_key != "secretValue":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )

    if request.amount is None or request.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be positive"
        )

    raw_tokens = request.amount * Decimal("2.5")
    new_tokens = int(raw_tokens.to_integral_value(rounding=ROUND_CEILING))

    increase_user_balance(request.userId, new_tokens)
    return "OK"
