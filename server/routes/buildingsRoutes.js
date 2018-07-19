const express = require('express')
const router = express.Router()
const BuildingsController = require(__dirname + '/../controllers/buildingsController')

router.get('/:id/violations', BuildingsController.violations)
router.get('/:id/service-calls', BuildingsController.serviceCalls)
router.get('/:id/sales', BuildingsController.sales)

module.exports = router
