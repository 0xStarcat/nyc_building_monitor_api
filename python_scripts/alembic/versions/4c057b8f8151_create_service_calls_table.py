"""create service_calls table

Revision ID: 4c057b8f8151
Revises: e8d9a74cd47e
Create Date: 2018-08-30 20:48:48.870842

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c057b8f8151'
down_revision = 'e8d9a74cd47e'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('service_calls',
                  sa.Column('id', sa.Integer, primary_key=True),
                  sa.Column('building_id', sa.Integer, sa.ForeignKey('buildings.id'), nullable=False),
                  sa.Column('unique_id', sa.Text),
                  sa.Column('date', sa.Text),
                  sa.Column('status', sa.Text),
                  sa.Column('source', sa.Text),
                  sa.Column('description', sa.Text),
                  sa.Column('resolution_description', sa.Text),
                  sa.Column('resolution_violation', sa.Boolean),
                  sa.Column('resolution_no_action', sa.Boolean),
                  sa.Column('unable_to_investigate', sa.Boolean),
                  sa.Column('open_over_month', sa.Boolean),
                  sa.Column('closed_date', sa.Text),
                  sa.Column('days_to_close', sa.Integer),
                  sa.Column('complaint_type', sa.Text)
                  )

  op.create_index('idx_call_building_id', 'service_calls', ['building_id'], None, unique=False)
  op.create_index('idx_call_date', 'service_calls', ['date'], None, unique=False)
  op.create_index('idx_call_status', 'service_calls', ['status'], None, unique=False)
  op.create_index('idx_call_source', 'service_calls', ['source'], None, unique=False)
  op.create_index('idx_call_res_vio', 'service_calls', ['resolution_violation'], None, unique=False)
  op.create_index('idx_call_res_na', 'service_calls', ['resolution_no_action'], None, unique=False)
  op.create_index('idx_call_res_unable', 'service_calls', ['unable_to_investigate'], None, unique=False)
  op.create_index('idx_call_open_over_month', 'service_calls', ['open_over_month'], None, unique=False)
  op.create_index('idx_call_complaint_type', 'service_calls', ['complaint_type'], None, unique=False)

  op.create_index('idx_call_unique_id', 'service_calls', ['unique_id'], None, unique=True)


def downgrade():
  op.drop_table('service_calls')
  pass
