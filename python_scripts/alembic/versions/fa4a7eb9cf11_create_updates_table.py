"""create updates table

Revision ID: fa4a7eb9cf11
Revises: 753cdb6e6a5c
Create Date: 2018-08-30 21:20:40.664445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa4a7eb9cf11'
down_revision = '753cdb6e6a5c'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('updates',
                  sa.Column('date', sa.Text),
                  sa.Column('new_violations', sa.Integer),
                  sa.Column('new_service_calls', sa.Integer),
                  sa.Column('resolved_violations', sa.Integer),
                  sa.Column('resolved_service_calls', sa.Integer)
                  )


def downgrade():
  op.drop_table('updates')
