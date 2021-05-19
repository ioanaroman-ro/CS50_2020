Hello!

My name is Ioana Roman, I am from Romania, and this is my project, a Gradebook for teachers.

My project is a web-based application using JavaScript, Python, and SQL, based in part on the web track’s distribution code.

The project is a web app via which teachers can manage their students, their courses and grade their students.

The SQL Database consists of 4 tables: Users, Students, Grades and Courses.

The file application.py

There are a several routes:

-route("/") index page, the first page any user sees, from where a user can login/register to acces the app, and, if logged in, he sees how many students he has and how many courses
-route("/login", methods=["GET", "POST"]) login page, where a registered user can log into his account
-route("/logout"), where an user logs ot from his account
-route("/register", methods=["GET", "POST"]), where a user can register into the database to be able to have an account, into the Users table,
    storing a hash of the user’s password, not the password itself
-route("/courses", methods=["GET", "POST"]), where the user sees his courses and can choose to add a new course
-route("/addcourse", methods=["GET", "POST"]), where the user adds a new course to the Courses table
-route("/students", methods=["GET", "POST"]), where the user sees his students and can choose to add a new student
-route("/addstudent", methods=["GET", "POST"]), where the user adds a new student to the Students table
-route("/grades", methods=["GET", "POST"]), where the user sees his grades for his students and can choose to add a new grade, or update a grade for a specific student/course.
For the purpose of protecting personal data, the grades page only shows ID for students, as their full names are not displayed. The user can only choose from his students and his courses.
-route("/addgrade", methods=["GET", "POST"]), where the user adds a new grade to the Grades table
-route("/updategrade", methods=["GET", "POST"]), where the user updates a grade to the Grades table, if he accidentally posted a different grade for a student,
or if that student had been reevaluated.

Routes are “decorated” with @login_required (a function defined in helpers.py).
That decorator ensures that, if a user tries to visit any of those routes, he or she will first be redirected to login so as to log in.

Inside static/ is styles.css

In templates/ there are HTML forms, stylized with Bootstrap. In apology.html is a template for an apology.

The app renders an apology for variuos situations, such as user does not exist, student does not exist, course does not exist, if a student has already been graded for a specific course,
or if any of the fields needed are not filled in correctly.