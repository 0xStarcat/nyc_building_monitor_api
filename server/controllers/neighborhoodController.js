const { db } = require(__dirname + '/../models/sequelize.js')

const constructNeighborhoodJSON = data => {
  return {
    features: data.map(row => {
      return {
        type: 'Feature',
        geometry: JSON.parse(row['geometry']),
        properties: {
          name: row['name']
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
