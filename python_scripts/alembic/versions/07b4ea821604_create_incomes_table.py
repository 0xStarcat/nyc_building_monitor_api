"""create incomes table

Revision ID: 07b4ea821604
Revises: 86e967c6c079
Create Date: 2018-08-21 10:05:09.301709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07b4ea821604'
down_revision = '86e967c6c079'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('incomes',
                  sa.Column('id', sa.Integer, primary_key=True),
                  sa.Column('borough_id', sa.Integer, sa.ForeignKey('boroughs.id'), nullable=False),
                  sa.Column('neighborhood_id', sa.Integer, sa.ForeignKey('neighborhoods.id'), nullable=False),
                  sa.Column('census_tract_id', sa.Integer, sa.ForeignKey('census_tracts.id'), nullable=False),
                  sa.Column('median_income_2011', sa.Float),
                  sa.Column('median_income_2017', sa.Float),
                  sa.Column('median_income_change_2011_2017', sa.Float)
                  )
  op.create_index('idx_income_ct', 'incomes', ['census_tract_id'], None, unique=True)
  pass


def downgrade():
  op.drop_table('incomes')
