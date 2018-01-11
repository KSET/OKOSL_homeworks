from app import app, mongo
from app.forms import LoginForm, CommentForm
from flask import render_template, flash, redirect, url_for
from bson.objectid import ObjectId
from bson.code import Code
from werkzeug.utils import secure_filename
import datetime
from pymongo import DESCENDING

NUMBER_OF_ARTICLES = 3


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<page>', methods=['GET', 'POST'])
def index(page=1):
    posts = []
    comment_forms = []
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

        form = CommentForm()
        form.post_id.data = post['_id']
        posts.append(post)
        comment_forms.append(form)

        if form.validate_on_submit() and form.submit.data:
            flash("Comment added!")
            author = form.author.data
            comment = form.body.data
            mongo.news.find_one_and_update(
                {'_id': ObjectId(form.post_id.data)},
                {'$push':
                    {'comments':
                        {
                            'author': author,
                            'comment': comment
                        }
                     }
                 }
            )
            return redirect(url_for('index'))
    return render_template('index.html', title="Home", post_index=list(range(len(posts))), posts=posts, forms=comment_forms)


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


@app.route('/news/<news_id>', methods=['GET', 'POST'])
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
        if form.validate_on_submit():
            flash("Comment added!")
            author = form.author.data
            comment = form.body.data

            mongo.news.find_one_and_update(
                {'_id': ObjectId(news_id)},
                {'$push':
                    {'comments':
                        {
                            'author': author,
                            'comment': comment
                        }
                     }
                 }
            )
            return redirect(url_for('news_post', news_id=news_id))
    return render_template('news_post.html', post=post, title=post['title'], error=error_flag, form=form)


@app.route('/comments')
def map_reduce_comments():

    map = Code("function(){ if (this.comments !== undefined){   var count = 0; this.comments.forEach( function(comment) {   count +=1; }); emit(this._id, count); } };")
    reduce = Code("function(key, values) { var rv = {   comments: key,   count: 0 }; values.forEach( function(value) {   rv.count += value.count; }); return rv; };")

    result = mongo.news.map_reduce(map=map, reduce=reduce, out="map_reduce_result")
    for doc in result.find().sort('value', DESCENDING):
        print(doc)

    posts = []  # for pretty-print on HTML
    for post_key in result.find().sort('value', DESCENDING):
        post = mongo.news.find_one({'_id': ObjectId(post_key['_id'])})
        post['no_of_comments'] = int(post_key['value'])
        if len(post['body']) > 502:
            post['body'] = post['body'][:500] + "..."

        print(post['title'])
        posts.append(post)
    return render_template('mr_comments.html', title="MapReduce Comment-sort", posts=posts)


@app.route('/words')
def map_reduce_words():
    pass
    # map = Code()
