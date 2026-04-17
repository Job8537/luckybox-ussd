from flask import Flask, request

app = Flask(__name__)

@app.route('/ussd', methods=['GET', 'POST'])
def ussd():
    if request.method == 'GET':
        return "Lucky Box USSD is running ✅"

    # Africa's Talking POST request
    text = request.values.get('text', '').strip()

    if text == "":
        response = "CON LUCKY BOX 20 KES 🎟️\n1. Top Up\n2. Play Now\n3. My Balance\n4. Withdraw\n0. Exit"
    elif text.startswith("1"):
        response = "CON Send to Paybill 0743740402\nAccount = your phone number\nThen reply with M-Pesa code"
    elif text.startswith("2"):
        response = "CON Balance low. Top up first!"
    elif text.startswith("3"):
        response = "END Balance: 0 KES (test mode)"
    elif text.startswith("4"):
        response = "END Withdraw coming soon"
    elif text.startswith("0"):
        response = "END Goodbye!"
    else:
        response = "CON Invalid. Try again:\n1. Top Up\n2. Play\n3. Balance\n4. Withdraw"

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
