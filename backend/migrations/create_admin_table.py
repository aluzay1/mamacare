"""Create separate admin table

Revision ID: create_admin_table
Revises: add_doctor_fields_to_referral_feedback
Create Date: 2024-12-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'create_admin_table'
down_revision = 'add_doctor_fields_to_referral_feedback'
branch_labels = None
depends_on = None

def upgrade():
    # Create admin table
    op.create_table('admin',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=False),
        sa.Column('address', sa.String(length=200), nullable=True),
        sa.Column('is_verified', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=sa.func.current_timestamp()),
        sa.Column('updated_at', sa.DateTime(), nullable=True, default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    # Migrate existing admin users from user table to admin table
    op.execute("""
        INSERT INTO admin (email, password, name, phone, address, is_verified, created_at)
        SELECT email, password, name, phone, address, is_verified, created_at
        FROM "user"
        WHERE role = 'admin'
    """)
    # Remove admin users from user table
    op.execute("DELETE FROM \"user\" WHERE role = 'admin'")

def downgrade():
    # Migrate admin users back to user table
    op.execute("""
        INSERT INTO "user" (email, password, name, phone, address, role, is_verified, created_at)
        SELECT email, password, name, phone, address, 'admin', is_verified, created_at
        FROM admin
    """)
    # Drop admin table
    op.drop_table('admin') 