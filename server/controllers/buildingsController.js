const { db } = require(__dirname + '/../models/sequelize.js')
const { dbPromise } = require('../db.js')

const {
  constructViolationJson,
  constructServiceCallJson,
  constructSaleJson,
  constructBuildingJson,
  constructBuildingSearchJson
} = require(__dirname + '/helpers/jsonHelpers.js')

const hasHouseNumber = string => {
  return /((\d)+-(\d)+)|(\d)+/.test(string)
}

const selectFullTextSearchQuery = query => {
  let house_number, street, borough_name
  const split = query.split(' ')

  const houseQuery = house_number =>
    `SELECT * FROM building_search WHERE building_search MATCH '"${house_number}"*' ORDER BY rank LIMIT 3`
  const houseStreetQuery = (house_number, street) =>
    `SELECT * FROM building_search WHERE building_search MATCH "house_number:${house_number}* address:${street}*" ORDER BY rank LIMIT 3`
  const houseStreetBoroughQuery = (house_number, street, borough_name) =>
    `SELECT * FROM building_search WHERE building_search MATCH ("house_number:${house_number}* address:${street}* borough_name:${borough_name}*") ORDER BY rank LIMIT 3`
  const streetQuery = street =>
    `SELECT * FROM building_search WHERE building_search MATCH "address:${street}*" ORDER BY rank LIMIT 3`

  if (!hasHouseNumber(split[0])) {
    return streetQuery(split.join(' ').replace(',', '')) // If no number in first split section, do generic street search
  } else if (hasHouseNumber(split[0]) && split.length > 1) {
    house_number = split[0].replace(',', '')
    borough_name = query.split(',')[1]
    if (borough_name) {
      // if a number and a comma are present, and split has more than 1 word, do house-street-borough query
      street = split
        .slice(1)
        .join(' ')
        .split(',')[0]
      return houseStreetBoroughQuery(house_number.trim(), street.trim(), borough_name.trim())
    } else {
      // if number and no comma present, do a house street query
      street = split
        .slice(1)
        .join(' ')
        .replace(',', '')
      return houseStreetQuery(house_number.trim(), street.trim())
    }
  } else {
    // if number is present and split only has 1 word, do a house number query
    house_number = split[0]
    console.log('***', houseQuery(house_number.trim()))
    return houseQuery(house_number.trim())
  }
}
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
  buildingById: async (req, res) => {
    db.Building.findAll({
      where: {
        id: req.params['id']
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
  },
  search: async (req, res) => {
    let userQuery = req.body['query'].trim().replace(/@|!|#|\$|%|\^|&|\*|(|)|_|\+|{|}|\[|\]|'|"|;|:|<|>|\?|=/g, '')
    if (userQuery === '') res.json({ results: [] })

    const dbQuery = selectFullTextSearchQuery(userQuery)

    const rawDb = await dbPromise
    const data = await rawDb.all(dbQuery).catch(error => {
      console.log('ERROR', error)
      res.json({ errors: error })
    })

    const searchData = await db.Building.findAll({
      where: {
        id: data.map(building => building.id)
      },
      attributes: ['id', 'address', 'representativePoint'],
      include: [{ model: db.Borough, attributes: ['name'] }]
    })

    res.json(constructBuildingSearchJson(searchData))
  }
}
