const { db } = require(__dirname + '/../models/sequelize.js')
const { constructNeighborhoodJson, constructBuildingJson } = require(__dirname + '/helpers/jsonHelpers.js')
const { dbPromise } = require('../db.js')

const constructNeighborhoodBoundaryJSON = data => {
  return {
    features: data.map(row => {
      return {
        type: 'Feature',
        geometry: JSON.parse(row['geometry']),
        properties: {
          name: row.name
        }
      }
    })
  }
}

module.exports = {
  boundaries: async (req, res) => {
    db.Neighborhood.findAll({
      include: []
    }).then(data => {
      res.json(constructNeighborhoodBoundaryJSON(data))
    })
  },
  index: async (req, res) => {
    const db = await dbPromise
    const data = await db
      .all(
        'SELECT n.*, \
      bo.name as borough_name,\
      inc.median_income_2017 as incomeMedian2017,\
      r.median_rent_2017 as rentMedian2017,\
      r.median_rent_change_2011_2017 as rentChange20112017,\
      rm.percent_white_2010 as racePercentWhite2010\
      FROM neighborhoods n \
      INNER JOIN boroughs bo ON bo.id = n.borough_id\
      INNER JOIN incomes inc ON inc.id = n.id\
      INNER JOIN rents r ON r.id = n.id\
      INNER JOIN racial_makeups rm ON rm.id = n.id\
      '
      )
      .catch(error => console.log('ERROR', error))
    res.json(constructNeighborhoodJson(data))
  },
  buildings: async (req, res) => {
    db.Building.findAll({
      where: {
        neighborhood_id: req.params['id']
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
