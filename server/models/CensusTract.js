module.exports = function(sequelize, DataTypes) {
  return sequelize.define(
    'census_tract',
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
      neighborhood_id: {
        type: DataTypes.INTEGER,
        field: 'neighborhood_id'
      },
      totalBuildings: {
        type: DataTypes.INTEGER,
        field: 'total_buildings'
      },
      totalResidentialBuildings: {
        type: DataTypes.INTEGER,
        field: 'total_residential_buildings'
      },
      totalViolations: {
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
      // total_service_calls_with_violation_result: {
      //   type: DataTypes.INTEGER,
      //   field: 'total_service_calls_with_violation_result'
      // },
      // total_service_calls_with_no_action_result: {
      //   type: DataTypes.INTEGER,
      //   field: 'total_service_calls_with_no_action_result'
      // },
      // total_service_calls_unresolved_result: {
      //   type: DataTypes.INTEGER,
      //   field: 'total_service_calls_unresolved_result'
      // },
      // racial_makeup_id: {
      //   type: DataTypes.INTEGER,
      //   field: 'racial_makeup_id'
      // },
      // total_sales_prior_violations: {
      //   type: DataTypes.INTEGER,
      //   field: 'total_sales_prior_violations'
      // },
      // avg_violation_count_3years_before_sale: {
      //   type: DataTypes.FLOAT,
      //   field: 'avg_violation_count_3years_before_sale'
      // }
    },
    {
      tableName: 'census_tracts'
    }
  )
}
