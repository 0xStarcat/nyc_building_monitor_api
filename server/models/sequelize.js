const Sequelize = require('sequelize')
const dbPath = __dirname + '../../../nyc_data_map.sqlite'
const sequelize = new Sequelize('sqlite://' + dbPath, {
  pool: {
    max: 5,
    min: 0,
    acquire: 30000,
    idle: 10000
  },
  // logging: false,
  // logging: process.env.NODE_ENV === 'test' ? false : true,
  define: {
    timestamps: false
  },

  // http://docs.sequelizejs.com/manual/tutorial/querying.html#operators
  operatorsAliases: false
})

const db = {
  Sequelize: Sequelize,
  sequelize: sequelize
}

db.Borough = sequelize.import(__dirname + '/Borough.js')
db.Neighborhood = sequelize.import(__dirname + '/Neighborhood.js')
db.CensusTract = sequelize.import(__dirname + '/CensusTract.js')
db.Income = sequelize.import(__dirname + '/Income.js')
db.Rent = sequelize.import(__dirname + '/Rent.js')
db.RacialMakeup = sequelize.import(__dirname + '/RacialMakeup.js')
db.Building = sequelize.import(__dirname + '/Building.js')
db.Violation = sequelize.import(__dirname + '/Violation.js')
db.Sale = sequelize.import(__dirname + '/Sale.js')
db.Permit = sequelize.import(__dirname + '/Permit.js')
db.ServiceCall = sequelize.import(__dirname + '/ServiceCall.js')
db.BuildingEvent = sequelize.import(__dirname + '/BuildingEvent.js')

// http://docs.sequelizejs.com/manual/tutorial/associations.html
// db.BuildingEvent.prototype.getItem = function(options) {
//   return this[
//     'get' +
//       this.get('eventable')
//         .substr(0, 1)
//         .toUpperCase() +
//       this.get('eventable').substr(1)
//   ](options)
// }

db.Borough.hasMany(db.Neighborhood, { foreignKey: 'borough_id', sourceKey: 'id' })
db.Borough.hasMany(db.CensusTract, { foreignKey: 'borough_id', sourceKey: 'id' })
db.Borough.hasMany(db.Building, { foreignKey: 'borough_id', sourceKey: 'id' })

db.Neighborhood.belongsTo(db.Borough, { foreignKey: 'borough_id', targetKey: 'id' })
db.Neighborhood.hasMany(db.CensusTract, { foreignKey: 'neighborhood_id', sourceKey: 'id' })
db.Neighborhood.hasMany(db.Building, { foreignKey: 'neighborhood_id', sourceKey: 'id' })
db.Neighborhood.hasMany(db.BuildingEvent, { foreignKey: 'neighborhood_id', sourceKey: 'id' })
db.Neighborhood.hasMany(db.Rent, { foreignKey: 'neighborhood_id', sourceKey: 'id' })
db.Neighborhood.hasMany(db.Income, { foreignKey: 'neighborhood_id', sourceKey: 'id' })
db.Neighborhood.hasMany(db.RacialMakeup, { foreignKey: 'neighborhood_id', sourceKey: 'id' })

db.CensusTract.belongsTo(db.Borough, { foreignKey: 'borough_id', targetKey: 'id' })
db.CensusTract.belongsTo(db.Neighborhood, { foreignKey: 'neighborhood_id', targetKey: 'id' })
db.CensusTract.hasMany(db.Building, { foreignKey: 'census_tract_id', sourceKey: 'id' })
db.CensusTract.hasMany(db.BuildingEvent, { foreignKey: 'census_tract_id', sourceKey: 'id' })
db.CensusTract.hasOne(db.Rent, { foreignKey: 'census_tract_id', sourceKey: 'id' })
db.CensusTract.hasOne(db.Income, { foreignKey: 'census_tract_id', sourceKey: 'id' })
db.CensusTract.hasOne(db.RacialMakeup, { foreignKey: 'census_tract_id', sourceKey: 'id' })

db.Building.belongsTo(db.Borough, { foreignKey: 'borough_id', targetKey: 'id' })
db.Building.belongsTo(db.Neighborhood, { foreignKey: 'neighborhood_id', targetKey: 'id' })
db.Building.belongsTo(db.CensusTract, { foreignKey: 'census_tract_id', targetKey: 'id' })
db.Building.hasMany(db.Sale, { foreignKey: 'building_id', sourceKey: 'id' })
db.Building.hasMany(db.Permit, { foreignKey: 'building_id', sourceKey: 'id' })
db.Building.hasMany(db.Violation, { foreignKey: 'building_id', sourceKey: 'id' })
db.Building.hasMany(db.ServiceCall, { foreignKey: 'building_id', sourceKey: 'id' })

db.RacialMakeup.belongsTo(db.CensusTract, { foreignKey: 'census_tract_id', targetKey: 'id' })
db.RacialMakeup.belongsTo(db.Neighborhood, { foreignKey: 'neighborhood_id', targetKey: 'id' })

db.Income.belongsTo(db.Neighborhood, { foreignKey: 'neighborhood_id', targetKey: 'id' })
db.Income.belongsTo(db.CensusTract, { foreignKey: 'census_tract_id', targetKey: 'id' })

db.Rent.belongsTo(db.Neighborhood, { foreignKey: 'neighborhood_id', targetKey: 'id' })
db.Rent.belongsTo(db.CensusTract, { foreignKey: 'census_tract_id', targetKey: 'id' })

db.Sale.belongsTo(db.Building, { foreignKey: 'building_id', targetKey: 'id' })

db.Permit.belongsTo(db.Building, { foreignKey: 'building_id', targetKey: 'id' })
db.ServiceCall.belongsTo(db.Building, { foreignKey: 'building_id', targetKey: 'id' })

db.Violation.belongsTo(db.Building, { foreignKey: 'building_id', targetKey: 'id' })
// db.Violation.belongsTo(db.BuildingEvent, { foreignKey: 'eventable_id', constraints: false, as: 'violation' })

// db.BuildingEvent.hasMany(db.Violation, {
//   foreignKey: 'eventable_id',
//   constraints: false,
//   scope: {
//     eventable: 'violation'
//   }
// })

// db.BuildingEvent.hasMany(db.Sale, {
//   foreignKey: 'eventable_id',
//   constraints: false,
//   scope: {
//     eventable: 'sale'
//   }
// })

// db.BuildingEvent.hasMany(db.Permit, {
//   foreignKey: 'eventable_id',
//   constraints: false,
//   scope: {
//     eventable: 'permit'
//   }
// })

// db.BuildingEvent.hasMany(db.ServiceCall, {
//   foreignKey: 'eventable_id',
//   constraints: false,
//   scope: {
//     eventable: 'service_call'
//   }
// })

module.exports = {
  db: db
}
