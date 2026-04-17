from flask import Flask, request

app = Flask(__name__)
DB = "luckybox.db"
PAYBILL = "0743740402"
PAYBILL_NAME = "LUCKY BOX"

# Simple in-memory storage for testing (we'll improve later)
users = {}

@app.route('/ussd', methods=['GET', 'POST'])
def ussd():
    if request.method == 'GET':
        return "LUCKY BOX USSD is running ✅<br>Use Africa's Talking to access the game."

    # Africa's Talking sends POST
    phone = request.values.get('phoneNumber')
    text = request.values.get('text', '').strip()
    user_input = text.split('*') if text else []

    if text == "":
        response = f"CON {PAYBILL_NAME} 20 KES 🎟️\n1. Top Up\n2. Play Now (20)\n3. My Balance\n4. Withdraw (min 200)\n0. Exit"
    elif user_input[0] == "1":   # Top Up
        response = f"CON Send money to Paybill {PAYBILL}\nUse your phone as Account Number\nThen reply with M-Pesa code\nExample: 1*RJ21D4NFLF"
    elif user_input[0] == "2":   # Play
        response = "CON Balance too low. Top up first to play!"
    elif user_input[0] == "3":
        response = "END Your current balance is 0 KES (for testing)"
    else:
        response = "CON Invalid option. Try again."

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
