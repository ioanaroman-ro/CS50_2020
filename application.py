import os
import hashlib

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

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

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///training.db")


@app.route("/")
@login_required
def index():
    """Show courses and students"""
    user_id = session["user_id"]
    total_students = db.execute("SELECT COUNT(IDStudent) AS Students FROM Students WHERE User_id = :user_id", user_id=user_id)
    total_courses = db.execute("SELECT COUNT(IDCourse) As Courses FROM Courses WHERE User_id = :user_id", user_id=user_id)
    return render_template("index.html", total_students = total_students[0]['Students'], total_courses = total_courses[0]['Courses'])


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
        rows = db.execute("SELECT * FROM Users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["HashPass"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["ID"]

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
        if len(password) < 5:
            return apology("Password must have at least 5 characters.", 400)
        if password != password2:
            return apology("Passwords do not match. Please enter the same password.", 400)
        if db.execute("SELECT Username FROM Users WHERE Username = :username", username = username):
            return apology("Username already exists, please choose new username.", 400)
        else:
            hash = generate_password_hash(password)
            db.execute("INSERT INTO Users (Username, Hashpass) VALUES (:username, :hash)", username = username, hash = hash)
            flash("Registered!")
            return redirect("/")


@app.route("/courses", methods=["GET", "POST"])
@login_required
def courses():
    """View Courses"""
    user_id = session["user_id"]
    current_courses = db.execute("SELECT IDCourse FROM Courses WHERE User_id = :user_id", user_id=user_id)
    if request.method == "GET":
        if current_courses != []:
            courses = list()
            length = range(len(current_courses))
            for i in length:
                courses_info = dict()
                courses_name = db.execute("SELECT CourseName FROM Courses WHERE User_id = :user_id", user_id=user_id)
                courses_date = db.execute("SELECT CoursePeriod FROM Courses WHERE User_id = :user_id", user_id=user_id)
                courses_info["IDCourse"] = current_courses[i]['IDCourse']
                courses_info["CourseName"] = courses_name[i]['CourseName']
                courses_info["CoursePeriod"] = courses_date[i]['CoursePeriod']
                courses.append(courses_info)
            return render_template("courses.html", courses = courses)
        else:
            return render_template("courses.html")


@app.route("/addcourse", methods=["GET", "POST"])
@login_required
def addcourses():
    """Add Courses"""
    user_id = session["user_id"]
    if request.method == "GET":
        return render_template("addcourse.html")
    if request.method == "POST":
        if not request.form.get("CourseName"):
            return apology("Missing course name", 400)
        if not request.form.get("CoursePeriod"):
            return apology("Missing course period", 400)
        CourseName = request.form.get("CourseName")
        CoursePeriod = request.form.get("CoursePeriod")
        db.execute("INSERT INTO Courses (User_id, CourseName, CoursePeriod)\
                       VALUES(:user_id, :CourseName, :CoursePeriod)",
                       user_id=user_id, CourseName=CourseName, CoursePeriod=CoursePeriod)
        flash("Added")
        return redirect("/")


@app.route("/students", methods=["GET", "POST"])
@login_required
def students():
    """View Students"""
    user_id = session["user_id"]
    current_students = db.execute("SELECT IDStudent FROM Students WHERE User_id = :user_id", user_id=user_id)
    if request.method == "GET":
        if current_students != []:
            students = list()
            length = range(len(current_students))
            for i in length:
                students_info = dict()
                students_first = db.execute("SELECT FirstName FROM Students WHERE User_id = :user_id", user_id=user_id)
                students_middle = db.execute("SELECT MiddleName FROM Students WHERE User_id = :user_id", user_id=user_id)
                students_last = db.execute("SELECT LastName FROM Students WHERE User_id = :user_id", user_id=user_id)
                students_info["IDStudent"] = current_students[i]['IDStudent']
                students_info["FirstName"] = students_first[i]['FirstName']
                students_info["MiddleName"] = students_middle[i]['MiddleName']
                students_info["LastName"] = students_last[i]['LastName']
                students.append(students_info)
            return render_template("students.html", students = students)
        else:
            return render_template("students.html")


@app.route("/addstudent", methods=["GET", "POST"])
@login_required
def addstudents():
    """Add Students"""
    user_id = session["user_id"]
    if request.method == "GET":
        return render_template("addstudent.html")
    if request.method == "POST":
        if not request.form.get("FirstName"):
            return apology("Missing first name", 400)
        if not request.form.get("LastName"):
            return apology("Missing last name", 400)
        FirstName = request.form.get("FirstName")
        if not request.form.get("MiddleName"):
            MiddleName = "NONE"
        else:
            MiddleName = request.form.get("MiddleName")
        LastName = request.form.get("LastName")
        db.execute("INSERT INTO Students (User_id, FirstName, MiddleName, LastName)\
                       VALUES(:user_id, :FirstName, :MiddleName, :LastName)",
                       user_id=user_id, FirstName=FirstName, MiddleName=MiddleName, LastName=LastName)
        flash("Added")
        return redirect("/")


@app.route("/grades", methods=["GET", "POST"])
@login_required
def grades():
    """View Grades"""
    user_id = session["user_id"]
    grades_students = db.execute("SELECT IDStudent FROM Grades WHERE User_id = :user_id", user_id=user_id)
    if request.method == "GET":
        if grades_students != []:
            grades = list()
            length = range(len(grades_students))
            for i in length:
                grades_info = dict()
                grades_courses = db.execute("SELECT IDCourse FROM Grades WHERE User_id = :user_id", user_id=user_id)
                grades_grades = db.execute("SELECT Grade FROM Grades WHERE User_id = :user_id", user_id=user_id)
                grades_info["IDStudent"] = grades_students[i]['IDStudent']
                grades_info["IDCourse"] = grades_courses[i]['IDCourse']
                grades_info["Grade"] = grades_grades[i]['Grade']
                grades.append(grades_info)
            return render_template("grades.html", grades = grades)
        else:
            return render_template("grades.html")


@app.route("/addgrade", methods=["GET", "POST"])
@login_required
def addgrades():
    """Add Grades"""
    user_id = session["user_id"]
    current_students = db.execute("SELECT IDStudent FROM Students WHERE user_id = :user_id GROUP BY IDStudent", user_id=user_id)
    current_courses = db.execute("SELECT IDCourse FROM Courses WHERE user_id = :user_id GROUP BY IDCourse", user_id=user_id)
    if request.method == "GET":
        student_list = list()
        course_list = list()
        for i in range(len(current_students)):
            if current_students[i]["IDStudent"]:
                student_list.append(current_students[i]["IDStudent"])
        for j in range(len(current_courses)):
            if current_courses[j]["IDCourse"]:
                course_list.append(current_courses[j]["IDCourse"])
        return render_template("addgrade.html", student_list=student_list, course_list=course_list)
    else:
        if not request.form.get("IDStudent"):
            return apology("MISSING IDStudent", 400)
        if not request.form.get("IDCourse"):
            return apology("MISSING IDCourse", 400)
        if not request.form.get("Grade"):
            return apology("MISSING GRADE", 400)
        IDStudent = request.form.get("IDStudent")
        IDCourse = request.form.get("IDCourse")
        Grade = request.form.get("Grade")
        current_grades = db.execute("SELECT Grade FROM Grades WHERE user_id = :user_id", user_id=user_id)
        if current_grades != []:
            graded_student = db.execute("SELECT IDStudent FROM Grades WHERE user_id = :user_id AND IDStudent = :IDStudent", user_id=user_id, IDStudent=IDStudent)
            if not graded_student:
                db.execute("INSERT INTO Grades (User_id, IDStudent, IDCourse, Grade)\
                        VALUES(:user_id, :IDStudent, :IDCourse, :Grade)",
                        user_id=user_id, IDStudent=IDStudent, IDCourse=IDCourse, Grade=Grade)
                flash("Added")
                return redirect("/")
            graded_course = db.execute("SELECT IDCourse FROM Grades WHERE user_id = :user_id AND IDStudent = :IDStudent", user_id=user_id, IDStudent=IDStudent)
            if not graded_course:
                db.execute("INSERT INTO Grades (User_id, IDStudent, IDCourse, Grade)\
                        VALUES(:user_id, :IDStudent, :IDCourse, :Grade)",
                        user_id=user_id, IDStudent=IDStudent, IDCourse=IDCourse, Grade=Grade)
                flash("Added")
                return redirect("/")
            for i in range(len(graded_student)):
                for j in range(len(graded_course)):
                    if (int(graded_student[i]['IDStudent']) == int(IDStudent[0])) and (int(graded_course[j]['IDCourse']) == int(IDCourse[0])):
                        return apology("Already graded", 405)
                    else:
                        db.execute("INSERT INTO Grades (User_id, IDStudent, IDCourse, Grade)\
                                VALUES(:user_id, :IDStudent, :IDCourse, :Grade)",
                                user_id=user_id, IDStudent=IDStudent, IDCourse=IDCourse, Grade=Grade)
                        flash("Added")
                        return redirect("/")
        else:
            db.execute("INSERT INTO Grades (User_id, IDStudent, IDCourse, Grade)\
                        VALUES(:user_id, :IDStudent, :IDCourse, :Grade)",
                        user_id=user_id, IDStudent=IDStudent, IDCourse=IDCourse, Grade=Grade)
            flash("Added")
            return redirect("/")


@app.route("/updategrade", methods=["GET", "POST"])
@login_required
def updategrades():
    """Update Grades"""
    user_id = session["user_id"]
    current_students = db.execute("SELECT IDStudent FROM Students WHERE user_id = :user_id GROUP BY IDStudent", user_id=user_id)
    current_courses = db.execute("SELECT IDCourse FROM Courses WHERE user_id = :user_id GROUP BY IDCourse", user_id=user_id)
    if request.method == "GET":
        student_list = list()
        course_list = list()
        for i in range(len(current_students)):
            if current_students[i]["IDStudent"]:
                student_list.append(current_students[i]["IDStudent"])
        for j in range(len(current_courses)):
            if current_courses[j]["IDCourse"]:
                course_list.append(current_courses[j]["IDCourse"])
        return render_template("updategrade.html", student_list=student_list, course_list=course_list)
    else:
        if not request.form.get("IDStudent"):
            return apology("MISSING IDStudent", 400)
        if not request.form.get("IDCourse"):
            return apology("MISSING IDCourse", 400)
        if not request.form.get("Grade"):
            return apology("MISSING GRADE", 400)
        IDStudent = request.form.get("IDStudent")
        IDCourse = request.form.get("IDCourse")
        Grade = request.form.get("Grade")
        current_grades = db.execute("SELECT Grade FROM Grades WHERE user_id = :user_id", user_id=user_id)
        if current_grades != []:
            graded_student = db.execute("SELECT IDStudent FROM Grades WHERE user_id = :user_id AND IDStudent = :IDStudent", user_id=user_id, IDStudent=IDStudent)
            if not graded_student:
                return apology("Not graded yet", 405)
            graded_course = db.execute("SELECT IDCourse FROM Grades WHERE user_id = :user_id AND IDStudent = :IDStudent", user_id=user_id, IDStudent=IDStudent)
            if not graded_course:
                return apology("Not graded yet", 405)
            for i in range(len(graded_student)):
                for j in range(len(graded_course)):
                    if (int(graded_student[i]['IDStudent']) == int(IDStudent[0])) and (int(graded_course[j]['IDCourse']) == int(IDCourse[0])):
                        db.execute("UPDATE Grades SET Grade = :Grade WHERE User_id = :user_id", Grade=Grade, user_id=user_id)
                        flash("Updated")
                        return redirect("/")
                    else:
                        return apology("Not graded yet", 405)
        else:
            return apology("Not graded yet", 405)



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
