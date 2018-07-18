const { db } = require(__dirname + '/../models/sequelize.js')

const constructBuildingJson = data => {
  return {
    features: data.map(row => {
      return {
        type: 'Feature',
        geometry: JSON.parse(row['geometry']),
        properties: {
          name: row.address,
          parentBoundaryName: row.neighborhood.name,
          topParentBoundaryName: row.borough.name,
          violationsTotal: row.totalViolations,
          salesTotal: row.totalSales,
          serviceCallsTotal: row.totalServiceCalls,
          serviceCallsPercentOpenOneMonth: row.totalServiceCallsOpenOverMonth
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
      },
      include: [
        {
          model: db.Neighborhood,
          attributes: ['name']
        },
        {
          model: db.Borough,
          attributes: ['name']
        }
      ]
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
