from flask import Flask, request

app = Flask(__name__)

PAYBILL = "0743740402"
PAYBILL_NAME = "LUCKY BOX"

@app.route('/', methods=['GET'])
def home():
    return "LUCKY BOX USSD Service is running ✅<br><br>Dial your shortcode *384*4681# to test it."

@app.route('/ussd', methods=['GET', 'POST'])
def ussd():
    if request.method == 'GET':
        return "LUCKY BOX USSD is running ✅<br>Use Africa's Talking simulator or your phone to access the menu."

    # This part runs when Africa's Talking sends the real POST request
    phone = request.values.get('phoneNumber')
    text = request.values.get('text', '').strip()

    if text == "":
        # First screen - must start with CON
        response = f"CON {PAYBILL_NAME} 20 KES 🎟️\n1. Top Up\n2. Play Now (20)\n3. My Balance\n4. Withdraw (min 200)\n0. Exit"
    elif text.startswith("1"):
        response = f"CON Send money to Paybill {PAYBILL}\nUse your phone number as Account Number\nThen reply with the M-Pesa code here\nExample: 1*RJ21D4NFLF"
    elif text.startswith("2"):
        response = "CON Your balance is too low. Please top up first to play!"
    elif text.startswith("3"):
        response = "END Your current balance is 0 KES (testing mode)"
    elif text.startswith("4"):
        response = "END Withdraw feature coming soon (minimum 200 KES)"
    elif text.startswith("0"):
        response = "END Thank you for using Lucky Box! Goodbye."
    else:
        response = "CON Invalid option. Please try again.\n1. Top Up\n2. Play Now\n3. My Balance\n4. Withdraw"

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
