
from flaskblog.posts.forms import  PostForm , CommentForm
from flask import render_template , flash , redirect , url_for , request , abort , Blueprint , jsonify , session
from flaskblog import db 
from flaskblog.models import Post , Like , Comment , Notification
from flask_login import current_user , login_required 
from datetime import datetime

posts = Blueprint('posts' , __name__)

@posts.route('/post/create' , methods=['GET','POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data , content=form.content.data , user_id = current_user.id)
        db.session.add(new_post)
        db.session.commit()

        # create Notification 
        notif = Notification(message = f"New Post : {new_post.title} from {new_post.author.username}" , 
                             link= url_for('posts.post' , post_id=new_post.id))
        db.session.add(notif)
        db.session.commit()

        flash('your post has been created!' , 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html' , title="new post" , form=form , legend="create post")

@posts.route('/post/<int:post_id>' ,methods=['GET'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if current_user.id != post.author.id:
        post.views += 1
        db.session.commit()
    user_liked = False
    if current_user.is_authenticated:
        user_liked = any(like.user_id == current_user.id for like in post.Likes)
    comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.date_posted.desc()).all()
    return render_template('post.html', title=post.title, post=post, form=form, comments=comments ,user_liked=user_liked)
    


@posts.route('/post/<int:post_id>/update', methods=['GET' , 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('the Post has been updated ' , 'success')
        return redirect(url_for('posts.post' , post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content 

    return render_template('create_post.html' , form=form , legend="update post" , title = 'update post')

@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("the post has been deleted " , 'success')
    return redirect(url_for('main.home'))

@posts.route('/post/<int:post_id>/like',methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)

    existing_like = Like.query.filter_by(user_id=current_user.id , post_id=post.id).first()
    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        liked = False
    else:
        new_like = Like(user_id=current_user.id , post_id=post.id)
        db.session.add(new_like)
        db.session.commit()
        liked = True
    
    return jsonify({
        'likes_count': len(post.Likes),
        'liked':liked
    })


@posts.route('/post/<int:post_id>/comment',methods=['POST'])
@login_required
def add_comment(post_id):
     post = Post.query.get_or_404(post_id)
     data = request.get_json()
     content = data.get('content')

     if not content:
        return jsonify({"error": "Comment cannot be empty"}), 400

     comment = Comment(content=content, user_id=current_user.id, post=post)
     db.session.add(comment)
     db.session.commit()

    # return the new comment as JSON so frontend can render it
     return jsonify({
        "username": current_user.username,
        "avatar": url_for('static' , filename='images/' + post.author.profile_image),
        "content": comment.content,
        "date_posted": comment.date_posted.strftime("%Y-%m-%d %H:%M")
    })


@posts.route('/get_notifications')
@login_required
def get_notifications():
    notifications = Notification.query.filter_by(is_read=False).order_by(Notification.created_at.desc()).all()
    notif_list = [
        {"id": n.id, "message": n.message, "link": n.link, "time": n.created_at.strftime("%Y-%m-%d %H:%M")}
        for n in notifications
    ]
    return jsonify(notif_list)


@posts.route("/notifications/read", methods=["POST"])
@login_required
def mark_notifications_read():
    notifications = Notification.query.filter_by(is_read=False).all()
    for notif in notifications:
        notif.is_read = True
    db.session.commit()
    return jsonify({"status": "ok"})