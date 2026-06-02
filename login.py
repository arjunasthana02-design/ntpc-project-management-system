from flask import Flask,render_template,request,session,redirect
import mysql.connector

app=Flask(__name__)

app.secret_key="ntpc"

db=mysql.connector.connect(
host="localhost",
user="root",
password="Arjun@0901",
database="Project"
)

cursor=db.cursor()


@app.route("/login")
def login():

    return render_template(
    "login.html"
    )


@app.route("/login_user",methods=["POST"])
def login_user():

    username=request.form["username"]

    password=request.form["password"]


    cursor.execute("""

    SELECT role,approved

    FROM users

    WHERE username=%s
    AND password=%s

    """,

    (username,password)
    )

    user=cursor.fetchone()


    if user:

        role=user[0]

        approved=user[1]

        if role=="admin" and approved=="Pending":

            return """

            <script>

            alert("Waiting Prime Admin Approval")

            window.location='/login'

            </script>

            """


        if role=="admin":

            return redirect(
            "http://127.0.0.1:5000"
            )


        return redirect(
        "http://127.0.0.1:5000"
        )


    return """

    <script>

    alert("Wrong Credentials")

    window.location='/login'

    </script>

    """


if __name__=="__main__":

    app.run(
    debug=True,
    port=5002
    )