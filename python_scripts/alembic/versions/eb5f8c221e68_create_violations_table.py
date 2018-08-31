"""create violations table

Revision ID: eb5f8c221e68
Revises: 4c057b8f8151
Create Date: 2018-08-30 20:59:12.532116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb5f8c221e68'
down_revision = '4c057b8f8151'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('violations',
                  sa.Column('building_id', sa.Integer, sa.ForeignKey('buildings.id'), nullable=False),
                  sa.Column('unique_id', sa.Text),
                  sa.Column('date', sa.Text),
                  sa.Column('description', sa.Text),
                  sa.Column('penalty_imposed', sa.Text),
                  sa.Column('source', sa.Text),
                  sa.Column('violation_code', sa.Text),
                  sa.Column('status', sa.Text),
                  sa.Column('status_description', sa.Text),
                  sa.Column('ecb_number', sa.Text)
                  )

  op.create_index('idx_violation_building_id', 'violations', ['building_id'], None, unique=False)
  op.create_index('idx_violation_source', 'violations', ['source'], None, unique=False)
  op.create_index('idx_violation_code', 'violations', ['violation_code'], None, unique=False)
  op.create_index('idx_violation_date', 'violations', ['date'], None, unique=False)
  op.create_index('idx_violation_status', 'violations', ['status'], None, unique=False)

  op.create_index('idx_violation_unique_id', 'violations', ['unique_id'], None, unique=True)


def downgrade():
  op.drop_table('violations')
