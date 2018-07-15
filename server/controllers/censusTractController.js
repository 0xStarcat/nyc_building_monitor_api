const { db } = require(__dirname + '/../models/sequelize.js')

const constructCensusTractJson = data => {
  return {
    features: data.map(row => {
      return {
        type: 'Feature',
        geometry: JSON.parse(row['geometry']),
        properties: {
          name: row['name'],
          parentBoundaryName: row.neighborhood.name,
          // churnPercent: parseFloat((row.total_sales / row.total_buildings) * 100),
          incomeMedian2017: parseFloat((row.income || {}).median_income_2017),
          incomeChange20112017: parseFloat((row.income || {}).median_income_change_2011_2017),
          rentMedian2017: parseFloat((row.rent || {}).median_rent_2017),
          rentChange20112017: parseFloat((row.rent || {}).median_rent_change_2011_2017),
          racePercentWhite2010: (row.racial_makeup || {}).percent_white_2010,
          buildingsTotal: parseFloat(row.total_buildings),
          salesTotal: parseFloat(row.total_sales),
          permitsTotal: parseFloat(row.total_permits),
          serviceCallsTotal: parseFloat(row.total_service_calls),
          serviceCallsPercentOpenOneMonth: parseFloat(
            ((row.total_service_calls_open_over_month / row.total_service_calls) * 100).toFixed(2)
          ),
          // serviceCallsPercentWithViolation: parseFloat(
          //   ((row.total_service_calls_with_violation_result / row.total_service_calls) * 100).toFixed(2)
          // ),
          // serviceCallsPercentNoAction: parseFloat(
          //   ((row.total_service_calls_with_no_action_result / row.total_service_calls) * 100).toFixed(2)
          // ),
          // serviceCallsPercentUnresolved: parseFloat(
          //   ((row.total_service_calls_unresolved_result / row.total_service_calls) * 100).toFixed(2)
          // ),
          // salesTotalPriorViolations: parseFloat(row.total_sales_prior_violations),
          // salesPercentPriorViolations: parseFloat(
          //   ((row.total_sales_prior_violations / row.total_sales) * 100).toFixed(2)
          // ),
          // violationsAverageBeforeSalePerBuilding: parseFloat(row.avg_violation_count_3years_before_sale),
          violationsTotal: parseFloat(row.total_violations),
          violationsPerBuilding: parseFloat((row.total_violations / row.total_buildings).toFixed(2))
          // violationsNonCommunityPerBuilding: parseFloat(
          //   ((row.total_violations - row.total_service_calls_with_violation_result) / row.total_buildings).toFixed(2)
          // ),
          // violationsPercentNonCommunity: parseFloat(
          //   (row.total_service_calls_with_violation_result / row.total_violations).toFixed(2) * 100
          // )
        }
      }
    })
  }
}

module.exports = {
  index: async (req, res) => {
    db.CensusTract.findAll({
      include: [
        {
          model: db.Neighborhood
        },
        {
          model: db.Income
        },
        {
          model: db.Rent
        },
        {
          model: db.RacialMakeup
        }
      ]
    }).then(data => {
      const json = constructCensusTractJson(data)
      // console.log(json)
      res.json(json)
    })
  }
}
