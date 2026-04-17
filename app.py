from flask import Flask, request
import random
import sqlite3
import datetime

app = Flask(__name__)
DB = "luckybox.db"
PAYBILL = "0743740402"           # Your personal number used here
PAYBILL_NAME = "LUCKY BOX"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (phone TEXT PRIMARY KEY, balance REAL DEFAULT 0, 
                  total_deposit REAL DEFAULT 0, total_won REAL DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS transactions 
                 (id INTEGER PRIMARY KEY, phone TEXT, amount REAL, 
                  type TEXT, details TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def get_balance(phone):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE phone=?", (phone,))
    row = c.fetchone()
    conn.close()
    return round(row[0], 2) if row else 0.0

def update_balance(phone, amount, trans_type, details):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (phone) VALUES (?)", (phone,))
    c.execute("UPDATE users SET balance = balance + ? WHERE phone=?", (amount, phone))
    if trans_type == "deposit":
        c.execute("UPDATE users SET total_deposit = total_deposit + ? WHERE phone=?", (amount, phone))
    if trans_type == "win":
        c.execute("UPDATE users SET total_won = total_won + ? WHERE phone=?", (amount, phone))
    c.execute("INSERT INTO transactions (phone, amount, type, details, timestamp) VALUES (?,?,?,?,?)",
              (phone, amount, trans_type, details, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

init_db()

@app.route('/ussd', methods=['POST'])
def ussd():
    phone = request.values.get('phoneNumber')
    text = request.values.get('text', '').strip()
    user_input = text.split('*') if text else []

    if text == "":
        response = f"CON {PAYBILL_NAME} 20 KES 🎟️\n1. Top Up\n2. Play Now (20)\n3. My Balance\n4. Withdraw (min 200)\n5. My History\n6. Rules\n0. Exit"

    elif user_input[0] == "1":  # Top Up
        if len(user_input) == 1:
            response = f"CON Send money to {PAYBILL_NAME} Paybill {PAYBILL}\nUse your phone number as Account Number\nThen reply with the M-Pesa code (e.g. RJ21D4NFLF)\nFormat: 1*CODE"
        else:
            ref = user_input[1].upper()
            response = f"END Deposit ref {ref} noted.\nCredit will appear in your {PAYBILL_NAME} wallet within 10 minutes."

    elif user_input[0] == "2":  # Play Now
        balance = get_balance(phone)
        if len(user_input) == 1:
            if balance < 20:
                response = "END Insufficient balance (20 KES needed). Top up first!"
            else:
                response = f"CON Balance: {balance} KES\nConfirm deduct 20 KES to pick a Lucky Box?\n1. Yes\n2. No"
        elif len(user_input) >= 2 and user_input[1] == "1":
            if balance < 20:
                response = "END Insufficient balance."
            else:
                update_balance(phone, -20, "play", "20 KES entry")
                # Hard & addictive prizes
                prizes = [0]*82 + [30]*14 + [80]*3 + [300]*0.9 + [100000]*0.1
                prize = random.choice(prizes)
                box = random.randint(1, 9)
                if prize > 0:
                    update_balance(phone, prize, "win", f"Box {box}")
                    if prize >= 100000:
                        msg = f"🎊 MEGA JACKPOT! Box {box} → +100,000 KES!!!"
                    elif prize >= 300:
                        msg = f"🎉 BIG WIN! Box {box} → +{prize} KES!"
                    else:
                        msg = f"🎉 WINNER! Box {box} → +{prize} KES!"
                else:
                    msg = f"😔 Box {box} was empty... 100,000 KES Jackpot still waiting!"
                new_bal = get_balance(phone)
                response = f"CON {msg}\nNew balance: {new_bal} KES\n1. Play Again\n2. Main Menu"
        else:
            response = "CON Back to menu"

    elif user_input[0] == "3":
        bal = get_balance(phone)
        response = f"END Your {PAYBILL_NAME} wallet: {bal} KES"

    elif user_input[0] == "4":
        bal = get_balance(phone)
        if bal < 200:
            response = "END Minimum withdrawal is 200 KES.\nKeep playing to reach it!"
        else:
            response = f"CON Confirm withdrawal of {bal} KES to your M-Pesa?\n1. Yes\n2. No"

    elif user_input[0] == "5":
        response = f"END Recent {PAYBILL_NAME} activity:\nKeep playing for the 100,000 KES Jackpot!"

    elif user_input[0] == "6":
        response = f"END {PAYBILL_NAME} Rules:\n• 20 KES per game\n• Pick 1 of 9 boxes\n• Wins stay in wallet\n• Withdraw only at 200+ KES\n• 100,000 KES Jackpot possible!\nPlay responsibly."

    elif user_input[0] == "0":
        response = f"END Thank you for playing {PAYBILL_NAME}! Come back soon 🎟️"

    else:
        response = "CON Invalid option. Try again."

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)