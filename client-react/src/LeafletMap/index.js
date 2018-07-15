import React, { Component } from 'react'
import PropTypes from 'prop-types'
import LayersMenu from './LayersMenu'
import Loading from '../SharedComponents/Loading'

import { Map, TileLayer, LayerGroup, GeoJSON, Circle } from 'react-leaflet'

import './style.scss'

export default class LeafletMap extends Component {
  constructor(props) {
    super()
    this.state = {
      lat: props.position.lat,
      lng: props.position.lng,
      zoom: props.zoom
    }

    this.mapRef = React.createRef()
    this.onBaseLayerChange = this.onBaseLayerChange.bind(this)
  }

  onBaseLayerChange(event) {
    console.log('map load')
  }

  render() {
    console.log('map render')
    const position = [this.state.lat, this.state.lng]
    return (
      <div>
        <Map
          center={position}
          id="leaflet-map"
          onLoad={this.onBaseLayerChange}
          ref={this.mapRef}
          zoom={this.state.zoom}
        >
          {!(
            this.props.store.censusTracts.initialFetchCompleted &&
            this.props.store.neighborhoods.initialFetchCompleted &&
            this.props.store.appState.allLayersLoaded
          ) && <Loading />}
          <TileLayer
            attribution="&amp;copy <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors"
            url="https://api.mapbox.com/styles/v1/starcat/cjjmbqf4pg6vq2rlqun4aquq9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoic3RhcmNhdCIsImEiOiJjamlpYmlsc28wbjlmM3FwbXdwaXozcWEzIn0.kLmWiUbmdqNLA1atmnTXXA"
          />
          <LayersMenu position="topright" />
        </Map>
      </div>
    )
  }
}

LeafletMap.propTypes = {
  position: PropTypes.shape({
    lat: PropTypes.number,
    lng: PropTypes.number
  }),
  zoom: PropTypes.number
}
