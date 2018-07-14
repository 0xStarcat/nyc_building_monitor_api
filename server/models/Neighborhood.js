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
      community_district_id: {
        type: DataTypes.INTEGER,
        field: 'community_district_id'
      }
      // total_buildings: {
      //   type: DataTypes.INTEGER,
      //   field: 'total_buildings'
      // },
      // total_violations: {
      //   type: DataTypes.INTEGER,
      //   field: 'total_violations'
      // },
      // total_sales: {
      //   type: DataTypes.INTEGER,
      //   field: 'total_sales'
      // },
      // total_permits: {
      //   type: DataTypes.INTEGER,
      //   field: 'total_permits'
      // },
      // total_service_calls: {
      //   type: DataTypes.INTEGER,
      //   field: 'total_service_calls'
      // },
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
      tableName: 'neighborhoods'
    }
  )
}
