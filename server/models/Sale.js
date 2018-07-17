module.exports = function(sequelize, DataTypes) {
  return sequelize.define(
    'sale',
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
      price: {
        type: DataTypes.INTEGER,
        field: 'price'
      }
    },
    {
      tableName: 'sales'
    }
  )
}
