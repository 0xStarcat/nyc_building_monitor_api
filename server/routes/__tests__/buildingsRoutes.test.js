import request from 'supertest'
import server from '../../nyc_data_server.js'

describe('/census-tracts', () => {
  describe('GET /census-tract/:id', () => {
    it('returns a 200 code', async () => {
      const response = await request(server).get('/buildings/census-tract/1')
      expect(response.status).toEqual(200)
    })

    it('returns the appropriate headers', async () => {
      const response = await request(server).get('/buildings/census-tract/1')
      expect(response.headers['content-type']).toMatch('json')
    })
  })
})
