const express = require('express')
const router = express.Router()
const BuildingsController = require(__dirname + '/../controllers/buildingsController')

router.get('/:id/violations', BuildingsController.violations)

module.exports = router
