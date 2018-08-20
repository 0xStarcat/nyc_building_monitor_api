"""create boroughs table

Revision ID: c80e38dc75de
Revises:
Create Date: 2018-08-19 21:52:33.050467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c80e38dc75de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('boroughs',
                  sa.Column('id', sa.Integer, primary_key=True),
                  sa.Column('name', sa.Text),
                  sa.Column('code', sa.Integer),
                  sa.Column('geometry', sa.Text),
                  sa.Column('representative_point', sa.Text),
                  sa.Column('total_buildings', sa.Integer),
                  sa.Column('total_violations', sa.Integer),
                  sa.Column('total_residential_buildings', sa.Integer),
                  sa.Column('total_sales', sa.Integer),
                  sa.Column('total_permits', sa.Integer),
                  sa.Column('total_service_calls', sa.Integer),
                  sa.Column('total_service_calls_open_over_month', sa.Integer),
                  sa.Column('service_calls_average_days_to_resolve', sa.Integer)
                  )
  op.create_index('idx_boro_name', 'boroughs', ['name'], None, unique=True)
  op.create_index('idx_boro_code', 'boroughs', ['code'], None, unique=True)
  pass


def downgrade():
  op.drop_table('boroughs')
  pass
