module.exports = function(sequelize, DataTypes) {
  return sequelize.define(
    'building_event',
    {
      id: {
        type: DataTypes.INTEGER,
        field: 'id',
        primaryKey: true
      },
      census_tract_id: {
        type: DataTypes.INTEGER,
        field: 'census_tract_id'
      },
      neighborhood_id: {
        type: DataTypes.INTEGER,
        field: 'neighborhood_id'
      },
      building_id: {
        type: DataTypes.INTEGER,
        field: 'building_id'
      },
      eventable: {
        type: DataTypes.STRING,
        field: 'eventable'
      },
      eventable_id: {
        type: DataTypes.INTEGER,
        field: 'eventable_id'
      }
    },
    {
      tableName: 'building_events'
    }
  )
}
