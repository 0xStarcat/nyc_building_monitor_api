const { db } = require(__dirname + '/../models/sequelize.js')
const { constructUpdateJson } = require(__dirname + '/helpers/jsonHelpers.js')

module.exports = {
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
