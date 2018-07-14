module.exports = function(sequelize, DataTypes) {
  return sequelize.define(
    'service_call',
    {
      id: {
        type: DataTypes.INTEGER,
        field: 'id',
        primaryKey: true
      },
      building_id: {
        type: DataTypes.INTEGER,
        field: 'building_id'
      },
      description: {
        type: DataTypes.STRING,
        field: 'description'
      },
      resolution_description: {
        type: DataTypes.INTEGER,
        field: 'resolution_description'
      },
      resolution_violation: {
        type: DataTypes.BOOLEAN,
        field: 'resolution_violation'
      }
    },
    {
      tableName: 'service_calls'
    }
  )
}
