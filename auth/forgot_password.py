from flask import Blueprint, render_template, request, redirect, url_for
import json
import os

forgot_bp = Blueprint("forgot", __name__)

ACCOUNTS_FILE = "data/accounts.json"

def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=4)

# ------------------------------
# FORGOT PASSWORD
# ------------------------------
@forgot_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    message = None

    if request.method == "POST":
        email = request.form["email"].strip().lower()
        accounts = load_accounts()

        if email not in accounts:
            message = "Email not found ❌"
        else:
            return redirect(url_for("forgot.reset_password", email=email))

    return render_template("forgot_password.html", message=message)

# ------------------------------
# RESET PASSWORD
# ------------------------------
@forgot_bp.route("/reset-password/<email>", methods=["GET", "POST"])
def reset_password(email):
    accounts = load_accounts()
    message = None

    if email not in accounts:
        return redirect(url_for("forgot.forgot_password"))

    if request.method == "POST":
        new_password = request.form["password"].strip()

        if not new_password:
            message = "Password cannot be empty ❌"
        else:
            accounts[email]["password"] = new_password
            save_accounts(accounts)
            return redirect(url_for("login"))

    return render_template("reset_password.html", email=email, message=message)
