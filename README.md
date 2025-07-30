# Stripe Payment Gateway with FastAPI and Custom Email Confirmation

This project implements a simple **Stripe payment backend using FastAPI** with a lightweight **HTML/JS frontend**.

Features:

* Predefined payment buttons (\$1, \$2, \$5, \$10) and custom amount
* Each \$0.50 = 1 search credit
* Stripe checkout using card input (Stripe Elements)
* Custom email confirmation sent via SMTP (in addition to Stripe’s official receipt)
* Clickable receipt link displayed after successful payment

---

## Requirements

* Python 3.9+
* Node/HTML (for the frontend – no build system needed)
* Stripe test account
* Gmail account for SMTP (or another SMTP provider)

---

## Setup

### 1. Clone this repository

```bash
git clone https://github.com/yourusername/fastapi-stripe-payments.git
cd fastapi-stripe-payments
```

---

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

---

### 3. Install dependencies

```bash
pip install fastapi uvicorn python-dotenv stripe
```

---

### 4. Configure `.env`

Create a `.env` file in the project root:

```
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxx
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

**Notes:**

* Generate `SMTP_PASSWORD` as a Google App Password (enable 2FA, then create App Password).
* Get `STRIPE_SECRET_KEY` from the Stripe dashboard (Test Mode).

---

### 5. Run the FastAPI backend

```bash
uvicorn main:app --reload
```

The API will be running at:

```
http://localhost:8000
```

---

### 6. Open the Frontend

* Open `index.html` in your browser (double-click or serve with a simple server).
* Update `pk_test_YOUR_PUBLISHABLE_KEY` in `index.html` with your **Stripe publishable key** (Test Mode).

---

## How it works

1. Choose a preset amount (\$1, \$2, \$5, \$10) or enter a custom amount.
2. Enter your email and card details.
3. Click **Pay**.
4. FastAPI backend:

   * Creates a Stripe charge using `stripe.Charge.create()`.
   * Stripe sends an official receipt to the email.
   * Backend also sends a **custom confirmation email** via SMTP.
5. The frontend displays a clean success message with:

   * Charge ID
   * Number of searches credited
   * A clickable Stripe receipt link.

---

## Endpoints

### `POST /process-payment/`

**Body:**

```json
{
  "amount": 500,          // in cents (e.g., 500 = $5)
  "currency": "usd",
  "token": "tok_visa",
  "email": "user@example.com"
}
```

**Response:**

```json
{
  "status": "success",
  "charge_id": "ch_3Qxxxxxx",
  "searches": 10,
  "stripe_receipt_sent": true,
  "stripe_receipt_url": "https://pay.stripe.com/receipts/acct_xxx..."
}
```

---

## Test Mode

Use Stripe test cards:

```
4242 4242 4242 4242
Any future expiry
Any CVC
ZIP 12345
```

---

## Live Mode

* Switch to live API keys.
* Make sure you have a verified Gmail SMTP setup or replace SMTP with SendGrid/Mailgun in production.

---

## Project Structure

```
.
├── main.py          # FastAPI backend
├── index.html       # Frontend
├── .env             # Environment variables
└── README.md
```

---

## Future Improvements

* Use Stripe **PaymentIntents** (recommended for new projects).
* Store purchases/credits in a database.
* Use a production-grade email service (SendGrid, SES, Mailgun).

---

## License

MIT License
