"""Add doctor fields to ReferralFeedback table

Revision ID: add_doctor_fields_to_referral_feedback
Revises: add_referral_feedback
Create Date: 2024-01-15 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_doctor_fields_to_referral_feedback'
down_revision = 'add_referral_feedback'
branch_labels = None
depends_on = None


def upgrade():
    # Add doctor fields to referral_feedback table
    op.add_column('referral_feedback', sa.Column('doctor_name', sa.String(length=200), nullable=True))
    op.add_column('referral_feedback', sa.Column('doctor_phone', sa.String(length=20), nullable=True))
    op.add_column('referral_feedback', sa.Column('doctor_affiliation', sa.String(length=200), nullable=True))


def downgrade():
    # Remove doctor fields from referral_feedback table
    op.drop_column('referral_feedback', 'doctor_affiliation')
    op.drop_column('referral_feedback', 'doctor_phone')
    op.drop_column('referral_feedback', 'doctor_name') 