from flask import Flask, render_template, request, redirect, session
import sql_connection_register as data_connection

# configurate

app = Flask(__name__)
app.secret_key = 'xjXBs72178#'


@app.route("/", methods=['GET', 'POST'])
def homepage():
    if session.get('user_email') is not None:
        return redirect("/expenses")
    else:
        return render_template("homepage.html")


@app.route("/login/", methods=['GET', 'POST'])
def login():
    if session.get('user_email') is not None:
        return redirect("/expenses")
    else:
        if request.method == "POST":
            added_user_mail = request.form.get("email")
            added_user_password = request.form.get("password")
            if data_connection.correct_login(added_user_mail, added_user_password):
                session["user_email"] = added_user_mail
                return redirect("/expenses")
            else:
                print("Wrong password or login. ")
                return redirect("/login")
        else:
            return render_template("login.html", login=False)


@app.route("/register/", methods=['GET', 'POST'])
def register():
    if session.get('user_email') is not None:
        return redirect("/expenses")
    else:
        if request.method == "POST":
            added_user_mail = request.form.get("email")
            added_user_password = request.form.get("password")
            added_user_f_name = request.form.get("first_name")
            added_user_l_name = request.form.get("last_name")

            if not data_connection.user_exist(added_user_mail):
                data_connection.register_new_user(added_user_mail, added_user_password, added_user_f_name,
                                                  added_user_l_name)
                session["user_email"] = added_user_mail
                return redirect("/expenses/")
            else:
                return print("User exist")
        #
        else:
            return render_template("registration.html", login=False)


@app.route("/expenses/", methods=['GET', 'POST'])
def expenses():

    if session.get('user_email') is not None:
        print("step1")
        user_mail = session.get('user_email')
        user_expenses = data_connection.see_user_expenses(user_mail)
        print(user_mail)
        if request.method == "POST":
            exp_description = request.form.get("description")
            exp_cost = request.form.get("cost")
            data_connection.add_expense(user_mail, exp_cost, exp_description)
            return redirect("/expenses")
        else:

            return render_template("expense_list.html", login=True, expenses_list=user_expenses)
    else:
        return redirect("/")


@app.route("/logout/", methods=['GET', 'POST'])
def logout():
    session.pop("user_email", None)
    return redirect("/")


if __name__ == "__main__":
    # start our application
    app.run(port=1234, host="0.0.0.0")
