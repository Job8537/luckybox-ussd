from flask import Flask, request

app = Flask(__name__)

PAYBILL = "0743740402"
PAYBILL_NAME = "LUCKY BOX"

# Simple in-memory storage (for testing)
users = {}

@app.route('/', methods=['GET'])
def home():
    return "LUCKY BOX USSD Service is running ✅<br><br>Open Africa's Talking simulator or dial your shortcode to use it."

@app.route('/ussd', methods=['GET', 'POST'])
def ussd():
    if request.method == 'GET':
        return "LUCKY BOX USSD is running ✅<br>Use Africa's Talking to access the full menu."

    # Africa's Talking sends POST
    phone = request.values.get('phoneNumber')
    text = request.values.get('text', '').strip()

    if text == "":
        response = f"CON {PAYBILL_NAME} 20 KES 🎟️\n1. Top Up\n2. Play Now (20)\n3. My Balance\n4. Withdraw (min 200)\n0. Exit"
    elif text.startswith("1"):
        response = f"CON Send money to Paybill {PAYBILL}\nAccount Number = your phone number\nThen reply with the M-Pesa code\nExample: 1*RJ21D4NFLF"
    elif text.startswith("2"):
        response = "CON Balance too low. Top up first!"
    elif text.startswith("3"):
        response = "END Your current balance is 0 KES (testing mode)"
    elif text.startswith("4"):
        response = "END Withdraw feature coming soon (min 200 KES)"
    else:
        response = "CON Invalid option. Try again.\n1. Top Up\n2. Play Now\n3. My Balance\n4. Withdraw"

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
