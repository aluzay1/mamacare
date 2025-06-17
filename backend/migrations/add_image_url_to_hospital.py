from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db

def upgrade():
    # Add image_url column to Hospital table
    db.engine.execute('ALTER TABLE hospital ADD COLUMN image_url VARCHAR(500)')

def downgrade():
    # Remove image_url column from Hospital table
    db.engine.execute('ALTER TABLE hospital DROP COLUMN image_url')

if __name__ == '__main__':
    upgrade() 