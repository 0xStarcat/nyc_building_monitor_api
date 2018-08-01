const express = require('express')
const router = express.Router()
const BuildingsController = require(__dirname + '/../controllers/buildingsController')

router.get('/', BuildingsController.index)
router.post('/search', BuildingsController.search)
router.get('/:id/violations', BuildingsController.violationsByBuilding)
router.get('/:id/service-calls', BuildingsController.serviceCallsByBuilding)
router.get('/:id/sales', BuildingsController.salesByBuilding)

module.exports = router
