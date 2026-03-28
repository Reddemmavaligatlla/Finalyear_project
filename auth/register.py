from flask import Blueprint, render_template, request, redirect, url_for
import json
import os
import re

register_bp = Blueprint("register", __name__)

ACCOUNTS_FILE = "data/accounts.json"
USERS_FILE = "data/users.json"


# --------------------------------------------------
# LOAD ACCOUNTS
# --------------------------------------------------
def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as f:
            return json.load(f)
    return {}


# --------------------------------------------------
# SAVE ACCOUNTS
# --------------------------------------------------
def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=4)


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def generate_user_id(users, accounts):
    max_id = 999

    for uid in users.keys():
        if isinstance(uid, str) and uid.startswith("u") and uid[1:].isdigit():
            max_id = max(max_id, int(uid[1:]))

    for account in accounts.values():
        if not isinstance(account, dict):
            continue
        uid = str(account.get("user_id", "")).strip()
        if uid.startswith("u") and uid[1:].isdigit():
            max_id = max(max_id, int(uid[1:]))

    return f"u{max_id + 1}"


# --------------------------------------------------
# REGISTER
# --------------------------------------------------
@register_bp.route("/register", methods=["GET", "POST"])
def register():
    message = None
    accounts = load_accounts()
    users = load_users()

    if request.method == "POST":
        email = request.form["email"].strip().lower()
        name = request.form["name"].strip()
        mobile = request.form["mobile"].strip()
        password = request.form["password"].strip()
        confirm_password = request.form["confirm_password"].strip()

        if not email or not name or not mobile or not password or not confirm_password:
            message = "All fields are required ❌"

        elif email in accounts:
            message = "Email already registered ❌"

        elif not re.fullmatch(r"\d{10}", mobile):
            message = "Mobile number must be 10 digits ❌"

        elif password != confirm_password:
            message = "Password and confirm password do not match ❌"

        elif any(
            isinstance(account, dict) and str(account.get("mobile", "")).strip() == mobile
            for account in accounts.values()
        ):
            message = "Mobile number already registered ❌"

        else:
            user_id = generate_user_id(users, accounts)
            accounts[email] = {
                "user_id": user_id,
                "name": name,
                "mobile": mobile,
                "password": password  # plain password (demo purpose)
            }
            users[user_id] = {
                "name": name,
                "preferences": []
            }
            save_accounts(accounts)
            save_users(users)
            return redirect(url_for("user_login", registered="1"))

    return render_template("register.html", message=message)


# --------------------------------------------------
# FORGOT PASSWORD
# --------------------------------------------------
@register_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    message = None
    accounts = load_accounts()

    if request.method == "POST":
        account_input = request.form["account_input"].strip()
        email = account_input.lower()

        if email not in accounts:
            email = None
            for registered_email, account in accounts.items():
                if not isinstance(account, dict):
                    continue
                if str(account.get("user_id", "")).strip() == account_input:
                    email = registered_email
                    break

        if not email or email not in accounts:
            message = "Account not found ❌"
        else:
            return redirect(
                url_for("register.reset_password", email=email)
            )

    return render_template("forgot_password.html", message=message)


# --------------------------------------------------
# RESET PASSWORD
# --------------------------------------------------
@register_bp.route("/reset-password/<email>", methods=["GET", "POST"])
def reset_password(email):
    accounts = load_accounts()
    message = None

    if email not in accounts:
        return redirect(url_for("register.forgot_password"))

    if request.method == "POST":
        new_password = request.form["password"].strip()

        if not new_password:
            message = "Password cannot be empty ❌"
        else:
            accounts[email]["password"] = new_password
            save_accounts(accounts)
            return redirect(url_for("user_login"))  # ✅ FIXED

    return render_template(
        "reset_password.html",
        email=email,
        message=message
    )
