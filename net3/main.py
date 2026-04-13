import sqlite3



conn = sqlite3.connect("bank.db")
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


def create_account():
    name = input("Enter name: ")
    user_id = input("Enter user id: ")

    cursor.execute("""
    INSERT INTO accounts (name, user_id, balance)
    VALUES (?, ?, ?)
    """, (name, user_id, 0))

    conn.commit()
    print(" Account created successfully  ")




def check_balance():
    user_id = input("Enter user id: ")

    cursor.execute("""
    SELECT balance FROM accounts
    WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    if result:
        print("balance:", result[0])
    else:
        print(" User not found")




def deposit_money():
    user_id = input("Enter user id: ")
    amount = float(input("Enter amount: "))

    cursor.execute("""
    UPDATE accounts
    SET balance = balance + ?
    WHERE user_id = ?
    """, (amount, user_id))

    conn.commit()
    print(" Money added successfully!")





def account_summary():
    user_id = input("Enter user id: ")

    cursor.execute("""
    SELECT * FROM accounts
    WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    if result:
        print("\n ACCOUNT SUMMARY")
        print("----------------------")
        print("Account ID:", result[0])
        print("Name:", result[1])
        print("User ID:", result[2])
        print("Balance:", result[3])
        print("----------------------\n")
    else:
        print(" User not found")








def view_all_accounts():
    cursor.execute("SELECT * FROM accounts")
    rows = cursor.fetchall()

    print("\nALL ACCOUNTS")
    print("----------------------")

    for row in rows:
        print("Account ID:", row[0])
        print("Name:", row[1])
        print("User ID:", row[2])
        print("Balance:", row[3])
        print("----------------------")






while True:
    print("\n ===== BANK MENU ===== ( click using number i mean select only no  )")
    print("1. Create Account")
    print("2. Check Balance")
    print("3. Deposit Money")
    print("4. Account Summary")
    print("5. View All Accounts")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        create_account()

    elif choice == "2":
        check_balance()

    elif choice == "3":
        deposit_money()

    elif choice == "4":
        account_summary()

    elif choice == "5":
        view_all_accounts()

    elif choice == "6":
        print(" Goodbye ab apna maa chuaaaadaaaaaa!")
        break

    else:
        print(" lauda sasta fuka hia kya ( Invalid choice)")