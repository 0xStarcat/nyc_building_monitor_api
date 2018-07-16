module.exports = function(sequelize, DataTypes) {
  return sequelize.define(
    'borough',
    {
      id: {
        type: DataTypes.INTEGER,
        field: 'id',
        primaryKey: true
      },
      name: {
        type: DataTypes.STRING,
        field: 'name'
      },
      geometry: {
        type: DataTypes.JSON,
        field: 'geometry'
      },
      total_buildings: {
        type: DataTypes.INTEGER,
        field: 'total_buildings'
      },
      total_violations: {
        type: DataTypes.INTEGER,
        field: 'total_violations'
      },
      total_sales: {
        type: DataTypes.INTEGER,
        field: 'total_sales'
      },
      total_permits: {
        type: DataTypes.INTEGER,
        field: 'total_permits'
      },
      total_service_calls: {
        type: DataTypes.INTEGER,
        field: 'total_service_calls'
      },
      total_service_calls_open_over_month: {
        type: DataTypes.INTEGER,
        field: 'total_service_calls_open_over_month'
      }
    },
    {
      tableName: 'boroughs'
    }
  )
}
