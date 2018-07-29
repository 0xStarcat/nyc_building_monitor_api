module.exports = function(sequelize, DataTypes) {
  return sequelize.define(
    'service_call',
    {
      id: {
        type: DataTypes.INTEGER,
        field: 'id',
        primaryKey: true
      },
      uniqueId: {
        type: DataTypes.STRING,
        field: 'unique_id'
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
      unableToInvestigate: {
        type: DataTypes.BOOLEAN,
        field: 'unable_to_investigate'
      },
      status: {
        type: DataTypes.BOOLEAN,
        field: 'status'
      },
      source: {
        type: DataTypes.STRING,
        field: 'source'
      },
      openOverMonth: {
        type: DataTypes.BOOLEAN,
        field: 'open_over_month'
      },
      daysToClose: {
        type: DataTypes.STRING,
        field: 'days_to_close'
      },
      closedDate: {
        type: DataTypes.STRING,
        field: 'closed_date'
      },
      complaintType: {
        type: DataTypes.STRING,
        field: 'complaint_type'
      }
    },
    {
      tableName: 'service_calls'
    }
  )
}
