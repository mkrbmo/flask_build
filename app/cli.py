import click
from flask import current_app
from . import db
from .models import Post

def register_commands(app):
    @app.cli.command("init-db")
    def init_db():
        """Initialize the database (drop + create tables)."""
        db.drop_all()
        db.create_all()
        click.echo("✅ Database initialized!")

    @app.cli.command("seed-db")
    def seed_db():
        """Insert sample blog posts."""
        sample_posts = [
            Post(title="Hello Flask", body="This is my first blog post!"),
            Post(title="App Factory", body="We’re using the application factory pattern."),
            Post(title="SQLite + SQLAlchemy", body="The blog is backed by a simple SQLite DB."),
        ]
        db.session.bulk_save_objects(sample_posts)
        db.session.commit()
        click.echo("🌱 Database seeded with sample posts.")
