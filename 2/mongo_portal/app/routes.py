from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect, url_for


posts = [
    {'id': '0', 'body': 'body nula', 'title': 'Nulti clanak', 'author': 'Andro :('},
    {'id': '1', 'body': 'body jedan', 'title': 'Prvi clanak', 'author': 'Jandra'},
    {'id': '2', 'body': 'body dva', 'title': 'Drugi clanak', 'author': 'Suhi'},
    {'id': '3', 'body': 'body tri', 'title': 'Treci clanak', 'author': 'Aco'},
    {'id': '4', 'body': 'body cetiri', 'title': 'Cetvrti clanak', 'author': 'jplavi'}
]


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'StrikeX'}
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

    try:
        post = posts[int(news_id)]
    except IndexError as e:
        print("No post found with the ID: {}".format(news_id))
        post = {'id': news_id, 'body': 'Not found!'}

    return render_template('news_post.html', post=post)
