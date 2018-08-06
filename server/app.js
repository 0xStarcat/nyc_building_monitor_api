const express = require('express')
const app = express()
const fs = require('fs')
const path = require('path')
const bodyParser = require('body-parser')

app.use(bodyParser.json())
app.use(express.static(path.resolve(__dirname, '/build/static')))
app.use((req, res, next) => {
  res.set({
    Accept: 'application/json',
    'Content-Type': 'application/json',
    'Access-Control-Allow-Credentials': true,
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With',
    'Access-Control-Allow-Methods': 'GET'
  })
  next()
})
const neighborhoods = require('./routes/neighborhoodRoutes')
const census_tracts = require('./routes/censusTractRoutes')
const buildings = require('./routes/buildingsRoutes')
const updates = require('./routes/updatesRoutes')

//Define what happens then a user visits the root route
app.get(['/', '/about', '/story', '/support'], (req, res) => {
  res.set({
    'Content-Type': 'text/html'
  })
  res.sendFile(path.resolve(__dirname, '../build', 'index.html'))
})

app.use('/neighborhoods', neighborhoods)
app.use('/census-tracts', census_tracts)
app.use('/buildings', buildings)
app.use('/updates', updates)

app.get('/boundaries/:type/:fileName', function(req, res) {
  var file = './data/boundary_data/' + req.params['type'] + '/' + req.params['fileName'] + '.geojson'
  fs.readFile(file, function(err, content) {
    res.write(content)
    res.end()
  })
})

module.exports = { app }

