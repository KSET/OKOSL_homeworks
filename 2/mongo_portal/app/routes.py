from app import app, mongo
from app.forms import LoginForm
from flask import render_template, flash, redirect, url_for
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
import datetime
import os


@app.route('/')
@app.route('/index')
def index():
    posts = []
    for post in mongo.news.find():
        posts.append(post)
        print(post['_id'])
    return render_template('index.html', title="Home", posts=posts)


@app.route('/publish', methods=['GET', 'POST'])
def publish():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Published!")
        title = form.title.data
        print(title)
        author = form.author.data
        print(author)
        date = datetime.datetime.now().isoformat()
        print(date)
        body = form.body.data
        print(body)
        image = form.image.data
        filename = secure_filename(image.filename)
        # image.save(os.path.join(
        #     app.instance_path, 'static', filename
        # ))

        mongo.news.save({
            'title': title,
            'author': author,
            'body': body,
            'date': date,
            'image': '/static/' + filename
        })
        return redirect(url_for('index'))
    return render_template('publish.html', title='Publish', form=form)


@app.route('/news/<news_id>')
def news_post(news_id):
    error_flag = None
    post = mongo.news.find_one({'_id': ObjectId(news_id)})  # try to find a news article with the given ID

    if post is None:
        print("No post found with the ID: {}".format(news_id))
        error_flag = True
        # post = {'id': news_id, 'body': 'Not found!'}

    return render_template('news_post.html', post=post, title=post['title'], error=error_flag)
