const { db } = require(__dirname + '/../models/sequelize.js')
const { dbPromise } = require('../db.js')

const {
  constructViolationJson,
  constructServiceCallJson,
  constructSaleJson,
  constructBuildingJson
} = require(__dirname + '/helpers/jsonHelpers.js')

const hasNumber = string => /\d/.test(string)

const selectFullTextSearchQuery = query => {
  let house_number, street, borough_name
  const split = query.split(' ')

  const houseQuery = house_number =>
    `SELECT * FROM building_search WHERE building_search MATCH "house_number:${house_number}*" ORDER BY rank LIMIT 4`
  const houseStreetQuery = (house_number, street) =>
    `SELECT * FROM building_search WHERE building_search MATCH "house_number:${house_number}* address:${street}*" ORDER BY rank LIMIT 4`
  const houseStreetBoroughQuery = (house_number, street, borough_name) =>
    `SELECT * FROM building_search WHERE house_number = "${house_number}" AND building_search MATCH ("address:${street}* borough_name:${borough_name}*") ORDER BY rank LIMIT 4`
  const streetQuery = street =>
    `SELECT * FROM building_search WHERE building_search MATCH "address:${street}*" ORDER BY rank LIMIT 4`

  if (!hasNumber(split[0])) {
    return streetQuery(split.join(' ')) // If no number in first split section, do generic street search
  } else if (hasNumber(split[0]) && split.length > 1) {
    house_number = split[0]
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
    let userQuery = req.body['query'].trim()
    if (userQuery === '') res.json({ results: [] })

    const dbQuery = selectFullTextSearchQuery(userQuery)

    const db = await dbPromise
    const data = await db.all(dbQuery).catch(error => {
      console.log('ERROR', error)
      res.json(error)
    })
    res.json(data)
  }
}
