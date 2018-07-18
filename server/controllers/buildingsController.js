const { db } = require(__dirname + '/../models/sequelize.js')

const { constructViolationJson } = require(__dirname + '/helpers/jsonHelpers.js')

module.exports = {
  violations: async (req, res) => {
    db.Violation.findAll({
      where: {
        building_id: req.params['id']
      }
    })
      .then(data => {
        res.json(constructViolationJson(data))
      })
      .catch(data => {
        console.log('ERROR', data)
        res.json({ errors: data })
      })
  }
}
