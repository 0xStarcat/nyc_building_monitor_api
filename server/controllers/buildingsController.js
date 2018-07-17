const { db } = require(__dirname + '/../models/sequelize.js')

const constructBuildingJson = data => {
  return {
    features: data.map(row => {
      console.log(row)
      return {
        type: 'Feature',
        geometry: JSON.parse(row['geometry']),
        properties: {
          violations: row.violations,
          sales: row.sales,
          totalViolations: row.totalViolations,
          totalSales: row.totalSales,
          totalServiceCalls: row.totalServiceCalls,
          totalServiceCallsOpenOverMonth: row.totalServiceCallsOpenOverMonth
        }
      }
    })
  }
}

module.exports = {
  censusTract: async (req, res) => {
    db.Building.findAll({
      where: {
        census_tract_id: req.params['id']
      }
    })
      .then(data => {
        res.json(constructBuildingJson(data))
      })
      .catch(data => {
        console.log('ERROR', data)
        res.json({ errors: data })
      })
  }
}
