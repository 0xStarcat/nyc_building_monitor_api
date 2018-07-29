module.exports = function(sequelize, DataTypes) {
  return sequelize.define(
    'violation',
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
      building_id: {
        type: DataTypes.INTEGER,
        field: 'building_id'
      },
      date: {
        type: DataTypes.STRING,
        field: 'date'
      },
      description: {
        type: DataTypes.STRING,
        field: 'description'
      },
      penaltyImposed: {
        type: DataTypes.STRING,
        field: 'penalty_imposed'
      },
      source: {
        type: DataTypes.STRING,
        field: 'source'
      },
      code: {
        type: DataTypes.STRING,
        field: 'violation_code'
      },
      status: {
        type: DataTypes.STRING,
        field: 'status'
      },
      statusDescription: {
        type: DataTypes.STRING,
        field: 'status_description'
      }
    },
    {
      tableName: 'violations'
    }
  )
}
