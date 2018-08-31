"""create_rents_table

Revision ID: 2ddddb9d00f6
Revises: 07b4ea821604
Create Date: 2018-08-30 19:39:03.792330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ddddb9d00f6'
down_revision = '07b4ea821604'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('rents',
                  sa.Column('id', sa.Integer, primary_key=True),
                  sa.Column('borough_id', sa.Integer, sa.ForeignKey('boroughs.id'), nullable=False),
                  sa.Column('neighborhood_id', sa.Integer, sa.ForeignKey('neighborhoods.id'), nullable=False),
                  sa.Column('census_tract_id', sa.Integer, sa.ForeignKey('census_tracts.id'), nullable=False),
                  sa.Column('median_rent_2011', sa.Float),
                  sa.Column('median_rent_2017', sa.Float),
                  sa.Column('median_rent_change_2011_2017', sa.Float)
                  )

  op.create_index('idx_rent_ct', 'rents', ['census_tract_id'], None, unique=True)


def downgrade():
  op.drop_table('rents')
