const sqlite = require('sqlite')
const dbPath = __dirname + '/../nyc_data_map.sqlite'
module.exports = {
  dbPromise: sqlite.open(dbPath, { Promise })
}
