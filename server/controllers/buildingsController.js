const { db } = require(__dirname + '/../models/sequelize.js')

const {
  constructViolationJson,
  constructServiceCallJson,
  constructSaleJson,
  constructBuildingJson
} = require(__dirname + '/helpers/jsonHelpers.js')

module.exports = {
  index: async (req, res) => {
    db.Building.findAll()
      .then(data => {
        res.json(constructBuildingJson(data))
      })
      .catch(data => {
        console.log('ERROR', data)
        res.json({ errors: data })
      })
  },
  violationsByBuilding: async (req, res) => {
    db.Violation.findAll({
      where: {
        building_id: req.params['id']
      },
      include: [{ model: db.Building, attributes: ['address'] }]
    })
      .then(data => {
        res.json(constructViolationJson(data))
      })
      .catch(data => {
        console.log('ERROR', data)
        res.json({ errors: data })
      })
  },
  serviceCallsByBuilding: async (req, res) => {
    db.ServiceCall.findAll({
      where: {
        building_id: req.params['id']
      },
      include: [{ model: db.Building, attributes: ['address'] }]
    })
      .then(data => {
        res.json(constructServiceCallJson(data))
      })
      .catch(data => {
        console.log('ERROR', data)
        res.json({ errors: data })
      })
  },
  salesByBuilding: async (req, res) => {
    db.Sale.findAll({
      where: {
        building_id: req.params['id']
      },
      include: [{ model: db.Building, attributes: ['address'] }]
    })
      .then(data => {
        res.json(constructSaleJson(data))
      })
      .catch(data => {
        console.log('ERROR', data)
        res.json({ errors: data })
      })
  }
}
