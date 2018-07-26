module.exports = function(sequelize, DataTypes) {
  return sequelize.define(
    'neighborhood',
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
      borough_id: {
        type: DataTypes.INTEGER,
        field: 'borough_id'
      },
      total_buildings: {
        type: DataTypes.INTEGER,
        field: 'total_buildings'
      },
      totalResidentialBuildings: {
        type: DataTypes.INTEGER,
        field: 'total_residential_buildings'
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
      totalServiceCalls: {
        type: DataTypes.INTEGER,
        field: 'total_service_calls'
      },
      totalServiceCallsOpenOverMonth: {
        type: DataTypes.INTEGER,
        field: 'total_service_calls_open_over_month'
      },
      representativePoint: {
        type: DataTypes.JSON,
        field: 'representative_point'
      }
    },
    {
      tableName: 'neighborhoods'
    }
  )
}
