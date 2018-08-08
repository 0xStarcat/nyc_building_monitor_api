const express = require('express')
const router = express.Router()
const UpdateController = require(__dirname + '/../controllers/updateController')

router.get('/', UpdateController.index)
router.get('/last', UpdateController.last)

module.exports = router
