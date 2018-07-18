import request from 'supertest'
import server from '../../nyc_data_server.js'

describe('/census-tracts', () => {
  describe('GET /', () => {
    it('returns a 200 code', async () => {
      const response = await request(server).get('/census-tracts')
      expect(response.status).toEqual(200)
    })
    it('returns the appropriate headers', async () => {
      const response = await request(server).get('/census-tracts')
      expect(response.headers['content-type']).toMatch('json')
    })
  })

  describe('GET /:id/buildings', () => {
    it('returns a 200 code', async () => {
      const response = await request(server).get('/census-tracts/1/buildings')
      expect(response.status).toEqual(200)
    })

    it('returns the appropriate headers', async () => {
      const response = await request(server).get('/census-tracts/1/buildings/')
      expect(response.headers['content-type']).toMatch('json')
    })
  })
})
