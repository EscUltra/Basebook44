
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)



@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm() #Form created in forms.py

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user) #Creates a new post form modles.py
        db.session.add(post) #readys database
        db.session.commit() #Adds the post to the database
        flash("Your post has been created!", 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title="New Post", form=form, legend="New Post")





@posts.route("/post/<int:post_id>")  #Look at an individual post from the id
def post(post_id): #Post id will be gottom from home.html it will get the id of that post from the database
    post = Post.query.get_or_404(post_id)  #stores the post with the id
    return render_template('post.html', title=post.title, post=post)





@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user: #If the current user is not the same as the author of the post then they cant edit the post
        abort(403)

    form = PostForm() #Reuse the form from creating a post
    if form.validate_on_submit():
        post.title = form.title.data #Change the title in the database
        post.content = form.content.data #Change content in database
        db.session.commit() #Update data in database
        flash("Your Post Has Been Updated", 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title  #Fill it with the current post data
        form.content.data = post.content
    return render_template('create_post.html', title="Update Post", form=form, legend="Update Post")




@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id) #Get the post from id
    if post.author != current_user: #Only allow if the author = current user
        abort(403)
    db.session.delete(post)
    db.session.commit() #Delete post from database
    flash("Your Post Has Been Deleted", 'success')
    return redirect(url_for('main.home'))