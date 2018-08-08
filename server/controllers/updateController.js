const { db } = require(__dirname + '/../models/sequelize.js')
const { constructUpdateJson } = require(__dirname + '/helpers/jsonHelpers.js')

module.exports = {
  index: async (req, res) => {
    db.Update.findAll({
      order: [['date', 'DESC']]
    })
      .then(data => {
        res.json(constructUpdateJson(data))
      })
      .catch(data => {
        console.log('ERROR', data)
        res.json({ errors: data })
      })
  },
  last: async (req, res) => {
    db.Update.findAll({
      limit: 1,
      order: [['date', 'DESC']]
    })
      .then(data => {
        res.json(constructUpdateJson(data))
      })
      .catch(data => {
        console.log('ERROR', data)
        res.json({ errors: data })
      })
  }
}
