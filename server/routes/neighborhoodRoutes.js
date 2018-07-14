const express = require('express')
const router = express.Router()
const NeighborhoodController = require(__dirname + '/../controllers/neighborhoodController')

router.get('/', NeighborhoodController.index)
module.exports = router
