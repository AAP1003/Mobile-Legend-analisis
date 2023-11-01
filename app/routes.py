from flask import render_template, url_for, request, redirect, flash
from app import app
from app.models import User, Video
from app.forms import RegistrationFrom, LoginFrom

@app.route("/")
def index():
    return render_template("index.html")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "mp4"


@app.route("/uploads", methods=["GET", "POST"])
def uploads():
    if request.method == "POST":
        title = request.form["title"]
        video_file = request.files["video_file"]

        if video_file:
            video_path = os.path.join("./static/uploads/", video_file.filename)
            video_file.save(video_path)

            new_video = Video(title=title, file_path=video_path)

            db.session.add(new_video)
            db.session.commit()

        return redirect(url_for("form"))

    title = None
    return render_template("uploads.html")


@app.route("/form")
def form():
    videos = Video.query.all()

    return render_template("uploads.html", videos=videos)

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationFrom()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form = form)


@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You Been Loggen in!!!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccesful. please check you password and email', 'danger')
    return render_template('login.html', form = form)

@app.route("/list")
def query():
    videos = Video.query.all()
    return render_template("query.html", videos=videos)


# @app.route('/static/assets/video/video.mp4')
# def video():
#    return send_file('static/assets/video/video.mp4', mimetype='video/mp4')
