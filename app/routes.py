from flask import Blueprint, render_template, request, redirect, url_for, current_app, abort
from .models import Post, Image
from . import db
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename

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

        # Step 2: handle GeoJSON file upload
        if geojson_file and geojson_file.filename.endswith('.geojson'):
            filename = secure_filename(geojson_file.filename)

            # Create directory static/geojson/<postid> if it doesn't exist
            geojson_dir = os.path.join(current_app.static_folder, 'geojson', str(post.id))
            os.makedirs(geojson_dir, exist_ok=True)

            # Save file
            geojson_path = os.path.join(geojson_dir, filename)
            geojson_file.save(geojson_path)

            # Store relative path for static access
            post.geojson_file = f"geojson/{post.id}/{filename}"

        # Step 3: handle image uploads
        for image_file in images:
            if image_file and image_file.filename:
                img_filename = secure_filename(image_file.filename)
                img_dir = os.path.join(current_app.static_folder, 'images', str(post.id))
                os.makedirs(img_dir, exist_ok=True)
                img_path = os.path.join(img_dir, img_filename)
                image_file.save(img_path)

                # Save image record in DB
                new_img = Image(filename=f"images/{post.id}/{img_filename}", post=post)
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

        if geojson_file and geojson_file.filename.endswith('.geojson'):
            geojson_filename = geojson_file.filename
            geojson_path = os.path.join(app.config['UPLOAD_FOLDER'], geojson_filename)
            geojson_file.save(geojson_path)
            post.geojson_file = geojson_filename

        for image in images:
            if image and image.filename:
                img_filename = secure_filename(image.filename)
                img_dir = os.path.join('static/images', str(post.id))
                os.makedirs(img_dir, exist_ok=True)
                img_path = os.path.join(img_dir, img_filename)
                image.save(img_path)

                new_img = Image(filename=f"images/{post.id}/{img_filename}", post=post)
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