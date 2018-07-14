import React from 'react'
import LeafletMap from '../../LeafletMap'
import SideBar from '../../SideBar'
import Layout from '../Layout'

const MapPage = props => {
  return (
    <Layout>
      <LeafletMap position={{ lat: 40.6881, lng: -73.9671 }} zoom={13} store={props.store} />
    </Layout>
  )
}

export default MapPage
