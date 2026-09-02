"""Add generation_status

Revision ID: 9380b0ffdc75
Revises: 0001_initial
Create Date: 2026-08-16 14:01:41.220372
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9380b0ffdc75'
down_revision = '0001_initial'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('test_attempts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('generation_status', sa.String(), server_default='READY', nullable=True))
        batch_op.add_column(sa.Column('error_message', sa.String(), nullable=True))


def downgrade():
    with op.batch_alter_table('test_attempts', schema=None) as batch_op:
        batch_op.drop_column('error_message')
        batch_op.drop_column('generation_status')

