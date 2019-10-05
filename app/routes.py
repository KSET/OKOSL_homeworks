from app import app
from app.forms import LoginForm  # , CommentForm
from flask import render_template, flash, redirect, url_for
# from werkzeug.utils import secure_filename
from flask_user import login_required, roles_required, current_user
from .models import Homework, Task
# import datetime


NUMBER_OF_ARTICLES = 3


@app.route('/')
@app.route('/homeworks')
@login_required
def homeworks():
    years = sorted([homework.year for homework in Homework.query.distinct(Homework.year)])
    homeworks_by_year = {year: list(Homework.query.filter(Homework.year == year)) for year in years}
    return render_template('homeworks.html', years=years, homeworks_by_year=homeworks_by_year)


@app.route('/homeworks/<hw_id>')
@login_required
def homework(hw_id):
    homework = Homework.query.get(hw_id)
    return render_template('homework_page.html', homework=homework)


@app.route('/tasks/<task_id>')
@login_required
def task(task_id):
    task = Task.query.get(task_id)
    homework = Homework.query.get(task.homework_id)
    return render_template('task_page.html', task=task, homework=homework)


@app.route('/admin')
@roles_required('Admin')
def admin_page():
    return render_template('admin.html')


@app.route('/publish', methods=['GET', 'POST'])
def publish():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Published!")
        # title = form.title.data
        # author = form.author.data
        # date = datetime.datetime.now().isoformat()
        # body = form.body.data
        # image = form.image.data
        # filename = secure_filename(image.filename)
        # image.save(os.path.join(
        #     app.instance_path, 'static', filename
        # ))

        # mongo.news.save({
        #     'title': title,
        #     'author': author,
        #     'body': body,
        #     'date': date,
        #     'image': '/static/' + filename
        # })
        return redirect(url_for('index'))
    return render_template('publish.html', title='Publish', form=form)


@app.route('/news/<news_id>', methods=['GET', 'POST'])
def news_post(news_id):
    error_flag = None
    form = None
    post = None
    title = None
    # post = mongo.news.find_one({'_id': ObjectId(news_id)})  # try to find a news article with the given ID

    # if post is None:
    #     print("No post found with the ID: {}".format(news_id))
    #     error_flag = True
    #     # post = {'id': news_id, 'body': 'Not found!'}
    # else:
    #     form = CommentForm()
    #     if form.validate_on_submit():
    #         flash("Comment added!")
    #         author = form.author.data
    #         comment = form.body.data

    #         mongo.news.find_one_and_update(
    #             {'_id': ObjectId(news_id)},
    #             {'$push':
    #                 {'comments':
    #                     {
    #                         'author': author,
    #                         'comment': comment
    #                     }
    #                  }
    #              }
    #         )
    #         return redirect(url_for('news_post', news_id=news_id))
    # return render_template('news_post.html', post=post, title=post['title'], error=error_flag, form=form)
    return render_template('news_post.html', post=post, title=title, error=error_flag, form=form)
