import request from 'supertest'
import server from '../../nyc_data_server.js'

describe('/buildings', () => {
  describe('GET /buildings/:id/violations', () => {
    it('returns a 200 code', async () => {
      const response = await request(server).get('/buildings/1/violations')
      expect(response.status).toEqual(200)
    })

    it('returns the appropriate headers', async () => {
      const response = await request(server).get('/buildings/1/violations')
      expect(response.headers['content-type']).toMatch('json')
    })
  })

  describe('GET /buildings/:id/service-calls', () => {
    it('returns a 200 code', async () => {
      const response = await request(server).get('/buildings/1/service-calls')
      expect(response.status).toEqual(200)
    })

    it('returns the appropriate headers', async () => {
      const response = await request(server).get('/buildings/1/service-calls')
      expect(response.headers['content-type']).toMatch('json')
    })
  })

  describe('GET /buildings/:id/sales', () => {
    it('returns a 200 code', async () => {
      const response = await request(server).get('/buildings/1/sales')
      expect(response.status).toEqual(200)
    })

    it('returns the appropriate headers', async () => {
      const response = await request(server).get('/buildings/1/sales')
      expect(response.headers['content-type']).toMatch('json')
    })
  })
})
