import os
import hashlib

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    current_stocks = db.execute("SELECT symbol FROM transactions WHERE user_id = :user_id GROUP BY symbol", user_id=user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
    total_available = cash[0]["cash"]
    if current_stocks != []:
        storages = list()
        for symbol in current_stocks:
            stock_data = lookup(symbol["symbol"])
            current_price = stock_data["price"]
            stock_info = dict()
            shares_info = db.execute("SELECT SUM(shares) AS shares_sum FROM transactions WHERE user_id = :user_id\
                                    GROUP BY symbol HAVING symbol = :symbol", user_id=user_id, symbol=symbol["symbol"])
            current_shares = shares_info[0]["shares_sum"]
            if current_shares > 0:
                stock_info["symbol"] = symbol["symbol"]
                stock_info["name"] = stock_data["name"]
                stock_info["price"] = usd(current_price)
                stock_info["shares"] = current_shares
                total = current_price * current_shares
                total_available += total
                stock_info["total"] = usd(total)
                storages.append(stock_info)
        return render_template("index.html", storages=storages, cash=usd(cash[0]["cash"]), total_available=usd(total_available))
    else:
        return render_template("index.html", cash=usd(cash[0]["cash"]), total_available=usd(total_available))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Missing symbol", 400)
        check = lookup(request.form.get("symbol"))
        if not check:
            return apology("Invalid symbol", 400)
        # not nessesary to check shares since form type is number, but cs50 check need it
        if (request.form.get("shares")).isdigit() == False:
            return apology("Enter positive shares", 400)
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        money = cash[0]["cash"]
        shares = float(request.form.get("shares"))
        price = check["price"]
        amount = price * shares
        user_id = session["user_id"]
        if money < amount:
            return apology("Can't afford", 400)
        else:
            db.execute("INSERT INTO transactions (user_id, stock_name, symbol, shares, price, total)\
                       VALUES(:user_id, :stock_name, :symbol, :shares, :price, :total)",
                       user_id=user_id, stock_name=check["name"], symbol=check["symbol"],
                       shares=shares, price=price, total=amount)
            balance = money - amount
            db.execute("UPDATE users SET cash = :balance WHERE id = :user_id",
                       balance=balance, user_id=user_id)
            flash("Bought!")
            return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = :user_id", user_id=user_id)
    for stock in transactions:
        stock["price"] = usd(stock["price"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Missing symbol", 400)
        check = lookup(request.form.get("symbol"))
        if not check:
            return apology("Invalid symbol", 400)
        else:
            check["price"] = usd(check["price"])
            return render_template("quoted.html", stock=check)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        if len(password) == 0 or len(username) == 0:
            return apology("Please enter valid data.", 400)
        if len(password) < 6:
            return apology("Password must have at least 6 characters.", 400)
        if password != password2:
            return apology("Passwords do not match. Please enter the same password.", 400)
        if db.execute("SELECT username FROM users WHERE username = :username", username = username):
            return apology("Username already exists, please choose new username.", 400)
        else:
            hash = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username = username, hash = hash)
            flash("Registered!")
            return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    current_stocks = db.execute("SELECT symbol FROM transactions WHERE user_id = :user_id GROUP BY symbol", user_id=user_id)

    if request.method == "GET":
        list_symbols = list()
        for symbol in current_stocks:
            shares_info = db.execute("SELECT SUM(shares) AS shares_sum FROM transactions\
                                    WHERE user_id = :user_id GROUP BY symbol HAVING symbol = :symbol", user_id=user_id, symbol=symbol["symbol"])
            current_shares = shares_info[0]
            if shares_info[0]["shares_sum"]:
                list_symbols.append(symbol["symbol"])
        return render_template("sell.html", list_symbols=list_symbols)
    else:
        if not request.form.get("symbol"):
            return apology("MISSING SYMBOL", 400)
        if not request.form.get("shares"):
            return apology("MISSING SHARES", 400)
        sell_symbol = request.form.get("symbol")
        sell_shares = float(request.form.get("shares"))
        shares_info = db.execute("SELECT SUM(shares) AS shares_sum FROM transactions\
                                    WHERE user_id = :user_id GROUP BY symbol HAVING symbol = :symbol", user_id=user_id, symbol=sell_symbol)
        if shares_info[0]["shares_sum"] < sell_shares:
            return apology("TOO MANY SHARES", 400)
        else:
            check = lookup(sell_symbol)
            price = check["price"]
            money = -sell_shares * price
            cash = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
            balance = cash[0]["cash"] - money
            db.execute("INSERT INTO transactions (user_id, stock_name, symbol, shares, price, total)\
                        VALUES(:user_id, :stock_name, :symbol, :shares, :price, :total)",
                       user_id=user_id, stock_name=check["name"], symbol=sell_symbol, shares=-sell_shares, price=price, total=money)
            db.execute("UPDATE users SET cash = :balance WHERE id = :user_id", balance=balance, user_id=user_id)
            flash("Sold")
            return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
