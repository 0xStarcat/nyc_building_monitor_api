"""create neighborhoods table


Revision ID: 400ddad296fc
Revises: c80e38dc75de
Create Date: 2018-08-20 11:07:13.910804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '400ddad296fc'
down_revision = 'c80e38dc75de'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('neighborhoods',
                  sa.Column('id', sa.Integer, primary_key=True),
                  sa.Column('borough_id', sa.Integer, sa.ForeignKey('boroughs.id'), nullable=False),
                  sa.Column('name', sa.Text),
                  sa.Column('geometry', sa.Text),
                  sa.Column('representative_point', sa.Text),
                  sa.Column('total_buildings', sa.Integer),
                  sa.Column('total_residential_buildings', sa.Integer),
                  sa.Column('total_violations', sa.Integer),
                  sa.Column('total_sales', sa.Integer),
                  sa.Column('total_permits', sa.Integer),
                  sa.Column('total_service_calls', sa.Integer),
                  sa.Column('total_service_calls_open_over_month', sa.Integer),
                  sa.Column('service_calls_average_days_to_resolve', sa.Integer)
                  )
  op.create_index('idx_n_borough_id', 'neighborhoods', ['borough_id'], None, unique=False)
  op.create_index('idx_n_name', 'neighborhoods', ['name'], None, unique=True)
  pass


def downgrade():

  op.drop_table('neighborhoods')
  pass
