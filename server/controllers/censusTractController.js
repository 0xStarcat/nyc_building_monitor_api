// const { db } = require(__dirname + '/../models/sequelize.js')
const { constructBuildingJson, constructCensusTractJson } = require(__dirname + '/helpers/jsonHelpers.js')

const { dbPromise } = require('../db.js')
module.exports = {
  index: async (req, res) => {
    const db = await dbPromise
    const data = await db.get('SELECT * FROM census_tracts')
    console.log(constructCensusTractJson(data))
    res.json(constructCensusTractJson(data))
  },
  indexOld: async (req, res) => {
    db.Borough.findAll().then(boroughData => {
      db.CensusTract.findAll({
        include: [
          {
            model: db.Neighborhood,
            attributes: ['name']
          },
          {
            model: db.Income,
            attributes: ['median_income_2017', 'median_income_change_2011_2017']
          },
          {
            model: db.Rent,
            attributes: ['median_rent_2017', 'median_rent_change_2011_2017']
          },
          {
            model: db.RacialMakeup,
            attributes: ['percent_white_2010']
          },
          {
            model: db.Building,
            attributes: []
          }
        ]
      }).then(data => {
        const json = constructCensusTractJson(data, boroughData)
        res.json(json)
      })
    })
  },

  buildings: async (req, res) => {
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
