import React, { Component } from 'react'
import PropTypes from 'prop-types'
import LayersMenu from './LayersMenu'

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

    this.layersLoaded = 0
    this.mapRef = React.createRef()
    this.neighborhoodLayerGroupRef = React.createRef()
    this.neighborhoodOverlayRef = React.createRef()
    this.bringNeighborhoodsToFront = this.bringNeighborhoodsToFront.bind(this)
    this.onLayerAdd = this.onLayerAdd.bind(this)
    this.onBaseLayerChange = this.onBaseLayerChange.bind(this)
  }

  bringNeighborhoodsToFront() {
    this.neighborhoodLayerGroupRef.current.leafletElement.setZIndex(1000)
    this.neighborhoodLayerGroupRef.current.leafletElement.eachLayer(layer => {
      if (layer._map) layer.bringToFront()
    })
  }

  onLayerAdd(event) {
    this.layersLoaded++
    // console.log(this.layersLoaded)
  }

  onBaseLayerChange(event) {
    setTimeout(this.bringNeighborhoodsToFront(), 10)
  }

  render() {
    const position = [this.state.lat, this.state.lng]
    return (
      <Map
        ref={this.mapRef}
        id="leaflet-map"
        center={position}
        zoom={this.state.zoom}
        onLoad={this.onBaseLayerChange}
        onlayeradd={this.onLayerAdd}
        onBaseLayerChange={this.onBaseLayerChange}
      >
        {/*mapbox.streets-satellite*/}
        {/*https://api.tiles.mapbox.com/v4/mapbox.wheatpaste/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoic3RhcmNhdCIsImEiOiJjamlpYmlsc28wbjlmM3FwbXdwaXozcWEzIn0.kLmWiUbmdqNLA1atmnTXXA*/}
        <TileLayer
          attribution="&amp;copy <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors"
          url="https://api.mapbox.com/styles/v1/starcat/cjjmbqf4pg6vq2rlqun4aquq9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoic3RhcmNhdCIsImEiOiJjamlpYmlsc28wbjlmM3FwbXdwaXozcWEzIn0.kLmWiUbmdqNLA1atmnTXXA"
        />
        <LayersMenu
          neighborhoodOverlayRef={this.neighborhoodOverlayRef}
          neighborhoodLayerGroupRef={this.neighborhoodLayerGroupRef}
          store={this.props.store}
          position="topright"
        />
      </Map>
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
