module.exports = function(sequelize, DataTypes) {
  return sequelize.define(
    'building',
    {
      id: {
        type: DataTypes.INTEGER,
        field: 'id',
        primaryKey: true
      },
      census_tract_id: {
        type: DataTypes.INTEGER,
        field: 'census_tract_id'
      },
      neighborhood_id: {
        type: DataTypes.INTEGER,
        field: 'neighborhood_id'
      },
      boroCode: {
        type: DataTypes.INTEGER,
        field: 'boro_code'
      },
      block: {
        type: DataTypes.STRING,
        field: 'block'
      },
      lot: {
        type: DataTypes.STRING,
        field: 'lot'
      },
      address: {
        type: DataTypes.STRING,
        field: 'address'
      },
      yearBuilt: {
        type: DataTypes.STRING,
        field: 'year_built'
      },
      geometry: {
        type: DataTypes.JSON,
        field: 'geometry'
      },
      representativePoint: {
        type: DataTypes.JSON,
        field: 'representative_point'
      },
      buildingClass: {
        type: DataTypes.STRING,
        field: 'bldg_class'
      },
      residentialUnits: {
        type: DataTypes.INTEGER,
        field: 'residential_units'
      },
      isResidential: {
        type: DataTypes.BOOLEAN,
        field: 'residential'
      },
      totalViolations: {
        type: DataTypes.INTEGER,
        field: 'total_violations'
      },
      totalServiceCalls: {
        type: DataTypes.INTEGER,
        field: 'total_service_calls'
      },
      totalServiceCallsOpenOverMonth: {
        type: DataTypes.INTEGER,
        field: 'total_service_calls_open_over_month'
      },
      averageDaysToResolveServiceCalls: {
        type: DataTypes.FLOAT,
        field: 'service_calls_average_days_to_resolve'
      }
    },
    {
      tableName: 'buildings'
    }
  )
}
