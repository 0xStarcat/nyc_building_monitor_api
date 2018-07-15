import React, { Component } from 'react'
import { GeoJSON, LayerGroup } from 'react-leaflet'

export default class NeighborhoodsBoundary extends Component {
  constructor(props) {
    super(props)
  }

  render() {
    return (
      <LayerGroup ref={this.props.neighborhoodLayerGroupRef} onToggle={this.moveToFront}>
        {this.props.store.neighborhoods.features.map((feature, index) => {
          return (
            <GeoJSON
              interactive={false}
              key={`ct-${index}`}
              data={feature['geometry']}
              color="hotpink"
              opacity={1}
              weight={1}
              fillOpacity={0}
            />
          )
        })}
      </LayerGroup>
    )
  }
}
