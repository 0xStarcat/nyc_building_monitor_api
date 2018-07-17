const { db } = require(__dirname + '/../models/sequelize.js')

const constructBuildingJson = data => {
  return {
    features: data.map(row => {
      // console.log(row)
      return {
        type: 'Feature',
        geometry: JSON.parse(row['geometry']),
        properties: {
          violations: row.violations,
          sales: row.sales,
          permits: row.permits
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
          model: db.Violation,
          attributes: ['date', 'description', 'penaltyImposed', 'source']
        },
        {
          model: db.Sale,
          attributes: ['date', 'price']
        },
        {
          model: db.Permit,
          attributes: ['date']
        },
        {
          model: db.ServiceCall,
          attributes: [
            'date',
            'description',
            'resolution_description',
            'resolution_violation',
            'resolution_no_action',
            'unable_to_investigate',
            'status',
            'open_over_month'
          ]
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
