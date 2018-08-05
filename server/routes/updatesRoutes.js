const express = require('express')
const router = express.Router()
const UpdateController = require(__dirname + '/../controllers/updateController')

router.get('/last', UpdateController.last)

module.exports = router
