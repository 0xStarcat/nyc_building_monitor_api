module.exports = function(sequelize, DataTypes) {
  return sequelize.define(
    'update',
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
      newViolations: {
        type: DataTypes.INTEGER,
        field: 'new_violations'
      },
      newServiceCalls: {
        type: DataTypes.INTEGER,
        field: 'new_service_calls'
      },
      resolvedViolations: {
        type: DataTypes.INTEGER,
        field: 'resolved_violations'
      },
      resolvedServiceCalls: {
        type: DataTypes.INTEGER,
        field: 'resolved_service_calls'
      }
    },
    {
      tableName: 'updates'
    }
  )
}
