



from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("bank.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    user_id TEXT UNIQUE,
    balance REAL DEFAULT 0
)
""")
conn.commit()

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/Create', methods=['POST'])
def create():
    name = request.form['name']
    user_id = request.form['user_id']

    cursor.execute("""
    INSERT INTO accounts (name, user_id, balance)
    VALUES (?, ?, ?)
    """, (name, user_id, 0))

    conn.commit()
    return "Account Created!"

@app.route('/Balance', methods=['POST'])
def balance():
    user_id = request.form['user_id']

    cursor.execute("SELECT balance FROM accounts WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result:
        return f"Balance: {result[0]}"
    else:
        return "User not found"

@app.route('/deposit', methods=['POST'])
def deposit():
    user_id = request.form['user_id']
    amount = float(request.form['amount'])

    cursor.execute("""
    UPDATE accounts
    SET balance = balance + ?
    WHERE user_id = ?
    """, (amount, user_id))

    conn.commit()
    return "Money added!"

@app.route('/summary', methods=['POST'])
def summary():
    user_id = request.form['user_id']

    cursor.execute("SELECT * FROM accounts WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result:
        return f"""
        Account ID: {result[0]}<br>
        Name: {result[1]}<br>
        User ID: {result[2]}<br>
        Balance: {result[3]}
        """
    else:
        return "User not found"

@app.route('/all')
def all_accounts():
    cursor.execute("SELECT * FROM accounts")
    rows = cursor.fetchall()

    output = ""
    for row in rows:
        output += f"""
        <hr>
        ID: {row[0]}<br>
        Name: {row[1]}<br>
        User ID: {row[2]}<br>
        Balance: {row[3]}<br>
        """
    return output

if __name__ == "__main__":
    app.run(debug=True)