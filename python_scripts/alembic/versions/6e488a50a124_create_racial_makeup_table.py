"""create racial makeup table

Revision ID: 6e488a50a124
Revises: 2ddddb9d00f6
Create Date: 2018-08-30 19:50:33.628670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e488a50a124'
down_revision = '2ddddb9d00f6'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('racial_makeups',
                  sa.Column('id', sa.Integer, primary_key=True),
                  sa.Column('borough_id', sa.Integer, sa.ForeignKey('boroughs.id'), nullable=False),
                  sa.Column('neighborhood_id', sa.Integer, sa.ForeignKey('neighborhoods.id'), nullable=False),
                  sa.Column('census_tract_id', sa.Integer, sa.ForeignKey('census_tracts.id'), nullable=False),
                  sa.Column('percent_white_2010', sa.Float)
                  )

  op.create_index('idx_racial_makeup_ct', 'racial_makeups', ['census_tract_id'], None, unique=True)


def downgrade():
  op.drop_table('racial_makeups')
  pass
