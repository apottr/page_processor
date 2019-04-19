from flask import Flask

app = Flask(__name__)

app.route("/",methods=["GET","POST"])
def index():
    dat = get_current()
    if request.method == "POST":
        out = handle_response(request.form)
        if out["status"] == "confirm":
                return render_template("confirmation.html",data=out["data"])
        elif out["status"] == "approved":
                return redirect("/")
        elif out["status"] == "declined":
                return render_template("selector.html",url=dat)
    else:
        return render_template("selector.html",url=dat)
        