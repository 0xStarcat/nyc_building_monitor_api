const { app } = require('./app')
const port = 5001
const server = app.listen(port, () => console.log(`Listening on port ${port}`))

module.exports = { server }
