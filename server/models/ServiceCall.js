module.exports = function(sequelize, DataTypes) {
  return sequelize.define(
    'service_call',
    {
      id: {
        type: DataTypes.INTEGER,
        field: 'id',
        primaryKey: true
      },
      date: {
        type: DataTypes.STRING,
        field: 'date'
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
      },
      resolution_no_action: {
        type: DataTypes.BOOLEAN,
        field: 'resolution_no_action'
      },
      unable_to_investigate: {
        type: DataTypes.BOOLEAN,
        field: 'unable_to_investigate'
      },
      status: {
        type: DataTypes.BOOLEAN,
        field: 'status'
      },
      open_over_month: {
        type: DataTypes.BOOLEAN,
        field: 'open_over_month'
      }
    },
    {
      tableName: 'service_calls'
    }
  )
}
