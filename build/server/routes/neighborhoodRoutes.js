'use strict';

var express = require('express');
var router = express.Router();
var NeighborhoodController = require(__dirname + '/../controllers/neighborhoodController');

router.get('/', NeighborhoodController.index);
module.exports = router;