"""create building_events table

Revision ID: 753cdb6e6a5c
Revises: eb5f8c221e68
Create Date: 2018-08-30 21:06:45.493021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '753cdb6e6a5c'
down_revision = 'eb5f8c221e68'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('building_events',
                  sa.Column('borough_id', sa.Integer, sa.ForeignKey('boroughs.id'), nullable=False),
                  sa.Column('neighborhood_id', sa.Integer, sa.ForeignKey('neighborhoods.id'), nullable=False),
                  sa.Column('census_tract_id', sa.Integer, sa.ForeignKey('census_tracts.id'), nullable=False),
                  sa.Column('building_id', sa.Integer, sa.ForeignKey('buildings.id'), nullable=False),
                  sa.Column('eventable', sa.Text),
                  sa.Column('eventable_id', sa.Integer),
                  sa.Column('event_date', sa.Text)
                  )

  op.create_index('idx_borough_building_events', 'building_events', ['borough_id'], None, unique=False)
  op.create_index('idx_neighborhood_building_events', 'building_events', ['neighborhood_id'], None, unique=False)
  op.create_index('idx_census_tract_building_events', 'building_events', ['census_tract_id'], None, unique=False)
  op.create_index('idx_building_building_events', 'building_events', ['building_id'], None, unique=False)
  op.create_index('idx_building_eventables', 'building_events', ['eventable'], None, unique=False)
  op.create_index('idx_building_ct_eventables', 'building_events', ['eventable', 'census_tract_id'], None, unique=False)
  op.create_index('idx_building_n_eventables', 'building_events', ['eventable', 'neighborhood_id'], None, unique=False)
  op.create_index('idx_building_b_eventables', 'building_events', ['eventable', 'borough_id'], None, unique=False)


def downgrade():
  op.drop_table('building_events')
