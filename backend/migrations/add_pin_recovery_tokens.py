"""Add PIN recovery tokens table

Revision ID: add_pin_recovery_tokens
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'add_pin_recovery_tokens'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create pin_recovery_token table
    op.create_table('pin_recovery_token',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('used', sa.Boolean(), nullable=True, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=datetime.utcnow),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )
    
    # Create index on token for faster lookups
    op.create_index(op.f('ix_pin_recovery_token_token'), 'pin_recovery_token', ['token'], unique=True)
    
    # Create index on user_id for faster queries
    op.create_index(op.f('ix_pin_recovery_token_user_id'), 'pin_recovery_token', ['user_id'], unique=False)

def downgrade():
    # Drop indexes
    op.drop_index(op.f('ix_pin_recovery_token_user_id'), table_name='pin_recovery_token')
    op.drop_index(op.f('ix_pin_recovery_token_token'), table_name='pin_recovery_token')
    
    # Drop table
    op.drop_table('pin_recovery_token') 