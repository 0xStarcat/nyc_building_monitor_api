"""create census_tracts table

Revision ID: 86e967c6c079
Revises: 400ddad296fc
Create Date: 2018-08-20 23:48:35.966100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86e967c6c079'
down_revision = '400ddad296fc'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('census_tracts',
                  sa.Column('id', sa.Integer, primary_key=True),
                  sa.Column('borough_id', sa.Integer, sa.ForeignKey('boroughs.id'), nullable=False),
                  sa.Column('neighborhood_id', sa.Integer, sa.ForeignKey('neighborhoods.id'), nullable=False),
                  sa.Column('name', sa.Text),
                  sa.Column('CTLabel', sa.Text),
                  sa.Column('boro_code', sa.Integer),
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
  op.create_index('idx_ct_neighborhood_id', 'census_tracts', ['neighborhood_id'], None, unique=False)
  op.create_index('idx_ct_borough_id', 'census_tracts', ['borough_id'], None, unique=False),
  op.create_index('idx_ct_boro_code', 'census_tracts', ['boro_code'], None, unique=False),
  op.create_index('idx_ct_boro_code_and_name', 'census_tracts', ['boro_code', 'name'], None, unique=True)
  op.create_index('idx_ct_boro_code_and_ctlabel', 'census_tracts', ['boro_code', 'CTLabel'], None, unique=True)
  pass


def downgrade():
  op.drop_table('census_tracts')
  pass
