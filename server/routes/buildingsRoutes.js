const express = require('express')
const router = express.Router()
const BuildingsController = require(__dirname + '/../controllers/buildingsController')

router.get('/census-tract/:id', BuildingsController.censusTract)
module.exports = router
