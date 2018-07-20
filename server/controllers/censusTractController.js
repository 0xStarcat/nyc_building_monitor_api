const { db } = require(__dirname + '/../models/sequelize.js')
const { constructBuildingJson, constructCensusTractJson } = require(__dirname + '/helpers/jsonHelpers.js')

// const { dbPromise } = require('../db.js')
module.exports = {
  // index: async (req, res) => {
  //   const db = await dbPromise
  //   const data = await db
  //     .all(
  //       "SELECT c.*, \
  //     n.name as n_name, \
  //     (SELECT COUNT(b.id) FROM buildings b WHERE c.id = b.census_tract_id) as buildings_total, \
  //     (\
  //       SELECT COUNT(sc.id) FROM service_calls sc \
  //       INNER JOIN building_events be ON c.id = be.census_tract_id \
  //       WHERE be.eventable ='service_call' AND sc.id = be.eventable_id\
  //     ) as service_calls_total\
  //     FROM census_tracts c \
  //     INNER JOIN neighborhoods n ON n.id = c.neighborhood_id\
  //     "
  //     )
  //     .catch(error => console.log('ERROR', error))
  //   console.log(data.length)
  //   res.json(constructCensusTractJson(data))
  // },
  index: async (req, res) => {
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
          }
        ]
      }).then(data => {
        console.log(data.length)
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
