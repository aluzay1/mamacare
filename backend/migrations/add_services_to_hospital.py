"""add services to hospital

Revision ID: add_services_to_hospital
Revises: 
Create Date: 2024-03-19

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_services_to_hospital'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add services column to hospital table
    op.add_column('hospital', sa.Column('services', sa.Text(), nullable=True))

def downgrade():
    # Remove services column from hospital table
    op.drop_column('hospital', 'services') 