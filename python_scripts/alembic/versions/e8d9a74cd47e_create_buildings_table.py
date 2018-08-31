"""create buildings table

Revision ID: e8d9a74cd47e
Revises: 6e488a50a124
Create Date: 2018-08-30 19:59:33.205114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8d9a74cd47e'
down_revision = '6e488a50a124'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('buildings',
                  sa.Column('id', sa.Integer, primary_key=True),
                  sa.Column('borough_id', sa.Integer, sa.ForeignKey('boroughs.id'), nullable=False),
                  sa.Column('neighborhood_id', sa.Integer, sa.ForeignKey('neighborhoods.id'), nullable=False),
                  sa.Column('census_tract_id', sa.Integer, sa.ForeignKey('census_tracts.id'), nullable=False),
                  sa.Column('boro_code', sa.Integer),
                  sa.Column('CT2010', sa.Text),
                  sa.Column('bbl', sa.Integer),
                  sa.Column('block', sa.Text),
                  sa.Column('lot', sa.Text),
                  sa.Column('address', sa.Text),
                  sa.Column('geometry', sa.Text),
                  sa.Column('representative_point', sa.Text),
                  sa.Column('year_built', sa.Integer),
                  sa.Column('residential_units', sa.Integer),
                  sa.Column('bldg_class', sa.Text),
                  sa.Column('residential', sa.Boolean),
                  sa.Column('total_violations', sa.Integer),
                  sa.Column('total_sales', sa.Integer),
                  sa.Column('total_service_calls', sa.Integer),
                  sa.Column('total_service_calls_open_over_month', sa.Integer),
                  sa.Column('service_calls_average_days_to_resolve', sa.Integer)
                  )

  op.create_index('idx_bldg_borough_and_residential', 'buildings', ['borough_id', 'residential'], None, unique=False)
  op.create_index('idx_bldg_neighborhood_and_residential', 'buildings', [
                  'neighborhood_id', 'residential'], None, unique=False),
  op.create_index('idx_bldg_census_tract_and_residential', 'buildings', [
                  'census_tract_id', 'residential'], None, unique=False)

  op.create_index('idx_bldg_boroid_and_address', 'buildings', ['boro_code', 'address'], None, unique=True)
  op.create_index('idx_bldg_bbl', 'buildings', ['bbl'], None, unique=True)


def downgrade():
  op.drop_table('buildings')
