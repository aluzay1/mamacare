"""Remove crowdfunding tables

Revision ID: remove_crowdfunding_tables
Revises: create_admin_table
Create Date: 2024-12-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'remove_crowdfunding_tables'
down_revision = 'create_admin_table'
branch_labels = None
depends_on = None


def upgrade():
    # Drop crowdfunding tables in correct order (respecting foreign key constraints)
    
    # First drop withdrawal_request table (depends on campaign)
    op.drop_table('withdrawal_request')
    
    # Then drop donation table (depends on campaign)
    op.drop_table('donation')
    
    # Finally drop campaign table
    op.drop_table('campaign')


def downgrade():
    # Recreate crowdfunding tables (for rollback purposes)
    
    # Create campaign table
    op.create_table('campaign',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('target_amount', sa.Float(), nullable=False),
        sa.Column('current_amount', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('deadline', sa.DateTime(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=True),
        sa.Column('creator_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create donation table
    op.create_table('donation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('payment_method', sa.String(length=20), nullable=False),
        sa.Column('transaction_id', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('donor_id', sa.Integer(), nullable=False),
        sa.Column('campaign_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaign.id'], ),
        sa.ForeignKeyConstraint(['donor_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('transaction_id')
    )
    
    # Create withdrawal_request table
    op.create_table('withdrawal_request',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('processed_at', sa.DateTime(), nullable=True),
        sa.Column('hospital_id', sa.Integer(), nullable=False),
        sa.Column('campaign_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaign.id'], ),
        sa.ForeignKeyConstraint(['hospital_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    ) 