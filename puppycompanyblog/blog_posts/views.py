from os import abort
from flask import render_template, redirect, request, Blueprint, url_for, flash
from flask_login import current_user, login_required
from puppycompanyblog import db
from puppycompanyblog.blog_posts.forms import BlogpostForm
from puppycompanyblog.models import Blogpost

blog_posts = Blueprint('blog_posts', __name__)


###############
# CREATE POST #
###############
@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogpostForm()
    if form.validate_on_submit():
        blog_post = Blogpost(title=form.title.data,
                             text=form.text.data,
                             user_id=current_user.id)
        db.session.add(blog_post)
        db.session.commit()
        flash("Blogpost created")
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)


#############
# VIEW POST #
#############

@blog_posts.route('/<int:blog_post_id>')
def view_blog_post(blog_post_id):
    blog_post = Blogpost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title=blog_post.title, date=blog_post.date, post=blog_post)


#################
# UPDATE POST   #
#################

@blog_posts.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = Blogpost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)
    form = BlogpostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Blogpost updated')
        return redirect(url_for('blog_posts.view_blog_post', blog_post_id=blog_post_id))
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text

    return render_template('create_post.html', title='Updating', form=form)


############
# DELETE   #
############

@blog_posts.route('/<int:blog_post_id>/delete', methods=['POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = Blogpost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog post deleted')
    return redirect(url_for('core.index'))
