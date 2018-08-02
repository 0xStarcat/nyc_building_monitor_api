const { app } = require('./app')
const port = process.env.NODE_ENV !== 'test' ? 5001 : 1234

if (process.env.NODE_ENV !== 'test') {
  app.listen(port, () => console.log(`Listening on port ${port}`))
}

module.exports = app
