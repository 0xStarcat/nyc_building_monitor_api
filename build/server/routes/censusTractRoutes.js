'use strict';

var express = require('express');
var router = express.Router();
var CensusTractController = require(__dirname + '/../controllers/censusTractController');

router.get('/', CensusTractController.index);
module.exports = router;