import uvicorn
from fastapi import FastAPI, HTTPException
import stripe
import os
import dotenv
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from send_email import send_email

# Load environment variables from .env file
dotenv.load_dotenv()
# Replace with your Stripe secret key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

app = FastAPI()

# Allow all origins (for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PaymentRequest(BaseModel):
    amount: int
    currency: str
    token: str
    email: str


import os
import dotenv
import uvicorn
import stripe
import smtplib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from email.mime.text import MIMEText

# Load environment variables
dotenv.load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PaymentRequest(BaseModel):
    amount: int
    currency: str
    token: str
    email: str


@app.post("/process-payment/")
async def process_payment(request: PaymentRequest):
    try:
        # Create a charge with Stripe
        charge = stripe.Charge.create(
            amount=request.amount,
            currency=request.currency,
            source=request.token,
            description="Payment for FaceSearch Telegram Bot",
            receipt_email=request.email,  # Stripe will email their official receipt
        )

        # Calculate number of searches (50 cents per search)
        searches = int((request.amount / 100) / 0.5)

        # Custom confirmation email
        subject = "Your FaceSearch Payment Confirmation"
        body = (
            f"Hello,\n\n"
            f"Thank you for your payment!\n\n"
            f"Charge ID: {charge.id}\n"
            f"Amount Paid: ${request.amount / 100:.2f}\n"
            f"Credits Purchased: {searches} searches\n\n"
            f"Your Official Receipt: {charge.receipt_url}\n\n"
            f"You can now use your searches in FaceSearch Telegram Bot.\n\n"
            f"Thank you for your support!"
        )

        # Send custom email
        send_email(request.email, subject, body)

        # Determine if Stripe generated a receipt
        stripe_receipt_sent = (
            charge.receipt_email is not None and charge.receipt_url is not None
        )
        print(f"Stripe receipt sent: { charge.receipt_url}")
        return {
            "status": "success",
            "charge_id": charge.id,
            "searches": searches,
            "stripe_receipt_sent": stripe_receipt_sent,
            "stripe_receipt_url": charge.receipt_url,
        }

    except stripe.error.CardError as e:
        return {"status": "error", "message": str(e)}
    except stripe.error.StripeError:
        return {
            "status": "error",
            "message": "Something went wrong. Please try again later.",
        }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
