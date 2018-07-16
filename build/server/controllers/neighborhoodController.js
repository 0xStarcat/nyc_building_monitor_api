'use strict';

var _regenerator = require('babel-runtime/regenerator');

var _regenerator2 = _interopRequireDefault(_regenerator);

var _asyncToGenerator2 = require('babel-runtime/helpers/asyncToGenerator');

var _asyncToGenerator3 = _interopRequireDefault(_asyncToGenerator2);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var _require = require(__dirname + '/../models/sequelize.js'),
    db = _require.db;

var constructNeighborhoodBoundaryJSON = function constructNeighborhoodBoundaryJSON(data) {
  return {
    features: data.map(function (row) {
      return {
        type: 'Feature',
        geometry: JSON.parse(row['geometry']),
        properties: {
          name: row.name
        }
      };
    })
  };
};

var constructNeighborhoodJSON = function constructNeighborhoodJSON(data) {
  return {
    features: data.map(function (row) {
      return {
        type: 'Feature',
        geometry: JSON.parse(row['geometry']),
        properties: {
          name: row.name,
          parentBoundaryName: row.borough.name,
          incomeMedian2017: parseFloat((row.income || {}).median_income_2017),
          incomeChange20112017: parseFloat((row.income || {}).median_income_change_2011_2017),
          rentMedian2017: parseFloat((row.rent || {}).median_rent_2017),
          rentChange20112017: parseFloat((row.rent || {}).median_rent_change_2011_2017),
          racePercentWhite2010: (row.racial_makeup || {}).percent_white_2010,
          buildingsTotal: parseFloat(row.total_buildings),
          salesTotal: parseFloat(row.total_sales),
          permitsTotal: parseFloat(row.total_permits),
          serviceCallsTotal: parseFloat(row.total_service_calls),
          serviceCallsPercentOpenOneMonth: parseFloat((row.total_service_calls_open_over_month / row.total_service_calls * 100).toFixed(2)),
          violationsTotal: parseFloat(row.total_violations),
          violationsPerBuilding: parseFloat((row.total_violations / row.total_buildings).toFixed(2))
        }
      };
    })
  };
};

module.exports = {
  boundaries: function () {
    var _ref = (0, _asyncToGenerator3.default)( /*#__PURE__*/_regenerator2.default.mark(function _callee(req, res) {
      return _regenerator2.default.wrap(function _callee$(_context) {
        while (1) {
          switch (_context.prev = _context.next) {
            case 0:
              db.Neighborhood.findAll({
                include: []
              }).then(function (data) {
                res.json(constructNeighborhoodBoundaryJSON(data));
              });

            case 1:
            case 'end':
              return _context.stop();
          }
        }
      }, _callee, undefined);
    }));

    function boundaries(_x, _x2) {
      return _ref.apply(this, arguments);
    }

    return boundaries;
  }(),
  index: function () {
    var _ref2 = (0, _asyncToGenerator3.default)( /*#__PURE__*/_regenerator2.default.mark(function _callee2(req, res) {
      return _regenerator2.default.wrap(function _callee2$(_context2) {
        while (1) {
          switch (_context2.prev = _context2.next) {
            case 0:
              db.Neighborhood.findAll({
                include: [{
                  model: db.Borough
                }, {
                  model: db.Income
                }, {
                  model: db.Rent
                }, {
                  model: db.RacialMakeup
                }]
              }).then(function (data) {
                res.json(constructNeighborhoodJSON(data));
              });

            case 1:
            case 'end':
              return _context2.stop();
          }
        }
      }, _callee2, undefined);
    }));

    function index(_x3, _x4) {
      return _ref2.apply(this, arguments);
    }

    return index;
  }()
};