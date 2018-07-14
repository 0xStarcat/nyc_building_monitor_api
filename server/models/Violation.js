module.exports = function(sequelize, DataTypes) {
  return sequelize.define(
    'violation',
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
      issue_date: {
        type: DataTypes.STRING,
        field: 'issue_date'
      },
      description: {
        type: DataTypes.STRING,
        field: 'description'
      }
    },
    {
      tableName: 'violations'
    }
  )
}
