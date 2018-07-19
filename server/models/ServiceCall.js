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
      resolutionDescription: {
        type: DataTypes.INTEGER,
        field: 'resolution_description'
      },
      resolutionViolation: {
        type: DataTypes.BOOLEAN,
        field: 'resolution_violation'
      },
      resolutionNoAction: {
        type: DataTypes.BOOLEAN,
        field: 'resolution_no_action'
      },
      unableToInvestigte: {
        type: DataTypes.BOOLEAN,
        field: 'unable_to_investigate'
      },
      status: {
        type: DataTypes.BOOLEAN,
        field: 'status'
      },
      openOverMonth: {
        type: DataTypes.BOOLEAN,
        field: 'open_over_month'
      },
      daysToClose: {
        type: DataTypes.STRING,
        field: 'days_to_close'
      }
    },
    {
      tableName: 'service_calls'
    }
  )
}
