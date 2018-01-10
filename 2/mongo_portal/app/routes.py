from app import app, mongo
from app.forms import LoginForm
from flask import render_template, flash, redirect, url_for


# posts = [
#     {'id': '0', 'date': '22.6.2018.', 'image': '/static/rpi.png', 'body': 'body nula' * 50, 'title': 'Nulti clanak', 'author': 'Andro :('},
#     {'id': '1', 'date': '22.6.2018.', 'image': '/static/rpi.png', 'body': 'body jedan', 'title': 'Prvi clanak', 'author': 'Jandra'},
#     {'id': '2', 'date': '22.6.2018.', 'image': '/static/rpi.png', 'body': 'body dva', 'title': 'Drugi clanak', 'author': 'Suhi'},
#     {'id': '3', 'date': '22.6.2018.', 'image': '/static/rpi.png', 'body': 'body tri', 'title': 'Treci clanak', 'author': 'Aco'},
#     {'id': '4', 'date': '22.6.2018.', 'image': '/static/rpi.png', 'body': 'body cetiri', 'title': 'Cetvrti clanak', 'author': 'jplavi'}
# ]


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'StrikeX'}
    posts = []
    for post in mongo.news.find():
        posts.append(post)
    return render_template('index.html', title="lalala", user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login requested for user {}, remember_me={}".format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/news/<news_id>')
def news_post(news_id):
    error_flag = None
    post = mongo.news.find_one({'_id': news_id})  # try to find a news article with the given ID

    if post is None:
        print("No post found with the ID: {}".format(news_id))
        error_flag = True
        # post = {'id': news_id, 'body': 'Not found!'}

    return render_template('news_post.html', post=post, error=error_flag)
