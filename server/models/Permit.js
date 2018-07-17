module.exports = function(sequelize, DataTypes) {
  return sequelize.define(
    'permit',
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
      date: {
        type: DataTypes.STRING,
        field: 'date'
      },
      geometry: {
        type: DataTypes.JSON,
        field: 'geometry'
      }
    },
    {
      tableName: 'permits'
    }
  )
}
