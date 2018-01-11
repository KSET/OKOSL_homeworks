from app import app, mongo
from app.forms import LoginForm, CommentForm
from flask import render_template, flash, redirect, url_for
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
import datetime
from pymongo import DESCENDING

NUMBER_OF_ARTICLES = 3


@app.route('/')
@app.route('/index')
@app.route('/index/<page>')
def index(page=1):
    posts = []
    page = int(page)
    if page < 1:
        page = 1
    if page != 1:
        no_of_pages = int(mongo.news.count() / 3) + 1  # calculate total number of pages
        try:
            page = int(page) if page <= no_of_pages else no_of_pages
        except ValueError as e:
            print("Invalid page index!")

    for post in mongo.news.find().sort('date', DESCENDING).skip((page - 1) * NUMBER_OF_ARTICLES).limit(NUMBER_OF_ARTICLES):
        if len(post['body']) > 502:
            post['body'] = post['body'][:500] + "..."

        posts.append(post)
        print(post['_id'])
    return render_template('index.html', title="Home", posts=posts)


@app.route('/publish', methods=['GET', 'POST'])
def publish():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Published!")
        title = form.title.data
        author = form.author.data
        date = datetime.datetime.now().isoformat()
        body = form.body.data
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
    form = None

    post = mongo.news.find_one({'_id': ObjectId(news_id)})  # try to find a news article with the given ID

    if post is None:
        print("No post found with the ID: {}".format(news_id))
        error_flag = True
        # post = {'id': news_id, 'body': 'Not found!'}
    else:
        form = CommentForm()
    return render_template('news_post.html', post=post, title=post['title'], error=error_flag, form=form)
