const { db } = require(__dirname + '/../models/sequelize.js')

const constructNeighborhoodJSON = data => {
  return {
    features: data.map(row => {
      console.log(row)
      return {
        type: 'Feature',
        geometry: JSON.parse(row['geometry']),
        properties: {
          name: row['name'],
          parentBoundaryName: row.borough.name,
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
          violationsTotal: parseFloat(row.total_violations),
          violationsPerBuilding: parseFloat((row.total_violations / row.total_buildings).toFixed(2))
        }
      }
    })
  }
}

module.exports = {
  index: async (req, res) => {
    db.Neighborhood.findAll().then(data => {
      res.json(constructNeighborhoodJSON(data))
    })
  }
}
