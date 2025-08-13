from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = "change_this_secret_key"   # sessions ke liye

# ----------------- Core Model -----------------
class Bank:
    def __init__(self, acc_no, name, address, phone, balance, pin):
        self.acc_no = acc_no
        self.name = name
        self.address = address
        self.phone = phone
        self.balance = float(balance)
        self.pin = str(pin)

    def deposit(self, amount):
        amount = float(amount)
        if amount <= 0:
            return False, "Amount must be positive."
        self.balance += amount
        return True, f"₹{amount:.2f} deposited. New balance: ₹{self.balance:.2f}"

    def withdraw(self, amount):
        amount = float(amount)
        if amount <= 0:
            return False, "Amount must be positive."
        if amount > self.balance:
            return False, "Insufficient balance."
        self.balance -= amount
        return True, f"₹{amount:.2f} withdrawn. Remaining balance: ₹{self.balance:.2f}"

    def details(self):
        return {
            "acc_no": self.acc_no,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "balance": self.balance
        }

# Dummy account (yahi change kar sakte ho)
bank = Bank(575944959040499, "Piyush", "Neemrana", "7357975446", 6000, pin="1234")

# In-memory transactions history: list of dicts
history = []  # {time, type, amount, balance}

# --------------- Helpers ----------------
def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("auth"):
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper

# --------------- Routes ------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        pin = request.form.get("pin", "")
        if pin == bank.pin:
            session["auth"] = True
            return redirect(url_for("dashboard"))
        else:
            error = "Incorrect PIN. Please try again."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/Account_panel")
@login_required
def dashboard():
    return render_template("Account_panel.html", info=bank.details())

@app.route("/deposit", methods=["POST"])
@login_required
def deposit():
    amount = request.form.get("amount", 0)
    ok, msg = bank.deposit(amount)
    if ok:
        history.append({
            "time": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
            "type": "Deposit",
            "amount": float(amount),
            "balance": bank.balance
        })
    return render_template("Account_panel.html", info=bank.details(), message=msg)

@app.route("/withdraw", methods=["POST"])
@login_required
def withdraw():
    amount = request.form.get("amount", 0)
    ok, msg = bank.withdraw(amount)
    if ok:
        history.append({
            "time": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
            "type": "Withdraw",
            "amount": float(amount),
            "balance": bank.balance
        })
    return render_template("Account_panel.html", info=bank.details(), message=msg)

@app.route("/history")
@login_required
def show_history():
    return render_template("history.html", history=history, info=bank.details())

if __name__ == "__main__":
    app.run(debug=True)
