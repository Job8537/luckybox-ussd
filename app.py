from flask import Flask, request

app = Flask(__name__)

PAYBILL = "0743740402"
PAYBILL_NAME = "LUCKY BOX"

@app.route('/', methods=['GET'])
def home():
    return "LUCKY BOX USSD Service is running ✅<br><br>Use the Africa's Talking simulator to test."

@app.route('/ussd', methods=['GET', 'POST'])
def ussd():
    # Log everything so we can see in Render Logs
    print("=== NEW USSD REQUEST ===")
    print("Method:", request.method)
    print("All data received:", dict(request.values))

    if request.method == 'GET':
        return "LUCKY BOX USSD is running ✅<br>Use Africa's Talking simulator or dial *384*4681#"

    # === This is the important part for Africa's Talking (POST) ===
    text = request.values.get('text', '').strip()
    phone = request.values.get('phoneNumber', '')

    print(f"Phone: {phone} | Text received: '{text}'")

    if text == "":
        response = f"CON {PAYBILL_NAME} 20 KES 🎟️\n1. Top Up\n2. Play Now (20)\n3. My Balance\n4. Withdraw (min 200)\n0. Exit"
    elif text.startswith("1"):
        response = f"CON Send money to Paybill {PAYBILL}\nUse your phone as Account Number\nThen reply with M-Pesa code\nExample: 1*RJ21D4NFLF"
    elif text.startswith("2"):
        response = "CON Balance too low. Top up first to play!"
    elif text.startswith("3"):
        response = "END Your current balance is 0 KES (testing mode)"
    elif text.startswith("4"):
        response = "END Withdraw feature coming soon (min 200 KES)"
    elif text.startswith("0"):
        response = "END Thank you for using Lucky Box! Goodbye."
    else:
        response = "CON Invalid option. Try again.\n1. Top Up\n2. Play Now\n3. My Balance\n4. Withdraw"

    print("Sending back:", response)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
