from flask import Blueprint, render_template, request, redirect, url_for, current_app, abort
from .models import Post, Image
from . import db
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from .utils import clear_post_images, replace_geojson_file

bp = Blueprint("main", __name__)
@bp.route('/')
def index():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template('index.html', posts=posts)

# About page
@bp.route('/about')
def about():
    return render_template('about.html')

# Add new post
@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_post():
    if not current_user.is_admin:
        abort(403)  # Forbidden

    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        location = request.form['location']
        content = request.form['content']
        geojson_file = request.files.get('geojson_file')
        images = request.files.getlist('images')

        # Step 1: create post without file paths (so we have post.id)
        post = Post(title=title, date=date, location=location,
                    content=content, geojson_file=None)
        db.session.add(post)
        db.session.flush()  # ensures post.id is available before commit

        # --- Handle GeoJSON replacement ---
        if geojson_file and geojson_file.filename.endswith('.geojson'):
            # Delete old GeoJSON file from disk nad replace
            post.geojson_file = replace_geojson_file(post.id, geojson_file)

        # --- Handle image replacement ---
        if images and any(img.filename for img in images):

            # Save new images
            for image in images:
                if image and image.filename:
                    img_filename = secure_filename(image.filename)
                    img_dir = os.path.join(current_app.static_folder, 'uploads', 'images', str(post.id))
                    os.makedirs(img_dir, exist_ok=True)
                    img_path = os.path.join(img_dir, img_filename)
                    image.save(img_path)

                    new_img = Image(filepath=img_path, post=post)
                    db.session.add(new_img)

        # Step 4: commit everything
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template("add.html")


# Edit existing post
@bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    if not current_user.is_admin:
        abort(403)  # Forbidden

    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.date = request.form['date']
        post.location = request.form['location']
        post.content = request.form['content']
        geojson_file = request.files.get('geojson_file')
        images = request.files.getlist('images')

        # --- Handle GeoJSON replacement ---
        if geojson_file and geojson_file.filename.endswith('.geojson'):
            # Delete old GeoJSON file from disk nad replace
            post.geojson_file = replace_geojson_file(post.id, geojson_file)

        # --- Handle image replacement ---
        if images and any(img.filename for img in images):
            # Delete old images from disk
            clear_post_images(post.id)
            # Delete old images from DB
            for old_img in post.images:
                db.session.delete(old_img)


            # Save new images
            for image in images:
                if image and image.filename:
                    img_filename = secure_filename(image.filename)
                    img_dir = os.path.join(current_app.static_folder, 'uploads', 'images', str(post.id))
                    os.makedirs(img_dir, exist_ok=True)
                    img_path = os.path.join(img_dir, img_filename)
                    image.save(img_path)

                    new_img = Image(filepath=img_path, post=post)
                    db.session.add(new_img)

        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('edit.html', post=post)

# Delete a post
@bp.route('/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    if not current_user.is_admin:
        abort(403)  # Forbidden
    post = Post.query.get_or_404(post_id)
    #db.session.delete(post)
    #db.session.commit()
    return redirect(url_for('main.index'))