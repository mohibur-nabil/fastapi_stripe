const stripe = Stripe("pk_test_51RqVPuGVfKwvdZOVY2MS3MtXk3qNGGw3TJZrV7oBl4vvg5vMyy06aGTjLa06QDfYSWcwLfHVC7dEXHrnlsUSvQvV001ucP0aER"); 
const cardElement = elements.create('card');
cardElement.mount('#card-element');

let selectedAmount = null;
let selectedButton = null;

function highlightButton(button) {
  if (selectedButton) selectedButton.classList.remove("selected");
  selectedButton = button;
  selectedButton.classList.add("selected");
}

document.querySelectorAll(".amount-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    selectedAmount = parseFloat(btn.dataset.amount);
    highlightButton(btn);
    document.getElementById("custom-amount").value = "";
    document.getElementById("result-message").innerHTML = "";
  });
});

document.getElementById("custom-pay-btn").addEventListener("click", () => {
  const customValue = parseFloat(document.getElementById("custom-amount").value);
  if (isNaN(customValue) || customValue <= 0) {
    alert("Please enter a valid custom amount.");
    return;
  }
  selectedAmount = customValue;
  if (selectedButton) selectedButton.classList.remove("selected");
  selectedButton = null;
  document.getElementById("result-message").innerHTML = "";
});

document.getElementById("payment-form").addEventListener("submit", async e => {
  e.preventDefault();
  const payButton = document.getElementById("pay-button");
  const spinner = document.getElementById("spinner");
  const resultDiv = document.getElementById("result-message");

  const email = document.getElementById("email").value;
  if (!selectedAmount) {
    alert("Please select or enter an amount.");
    return;
  }

  // Show spinner and disable pay button
  spinner.style.display = "block";
  payButton.disabled = true;
  resultDiv.innerHTML = "";

  const { token, error } = await stripe.createToken(cardElement);
  if (error) {
    spinner.style.display = "none";
    payButton.disabled = false;
    resultDiv.innerHTML =
      `<p style="color:red;">${error.message}</p>`;
    return;
  }

  try {
    const response = await fetch("http://localhost:8000/process-payment/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        amount: Math.round(selectedAmount * 100),
        currency: "usd",
        token: token.id,
        email: email
      })
    });

    const data = await response.json();

    if (data.status === "success") {
      let html = `
        <div style="padding:12px; border:1px solid #28a745; border-radius:6px; background:#e6ffed;">
          <h4 style="color:#28a745;">Payment Successful!</h4>
          <p><strong>Charge ID:</strong> ${data.charge_id}</p>
          <p><strong>Credits Purchased:</strong> ${data.searches} searches</p>
      `;
      if (data.stripe_receipt_url) {
        html += `<p><a href="${data.stripe_receipt_url}" target="_blank">View Stripe Receipt</a></p>`;
      }
      html += `</div>`;
      resultDiv.innerHTML = html;
    } else {
      resultDiv.innerHTML =
        `<p style="color:red;">Payment failed: ${data.message}</p>`;
    }

  } catch (err) {
    resultDiv.innerHTML =
      `<p style="color:red;">An error occurred: ${err.message}</p>`;
  } finally {
    spinner.style.display = "none";
    payButton.disabled = false;
  }
});