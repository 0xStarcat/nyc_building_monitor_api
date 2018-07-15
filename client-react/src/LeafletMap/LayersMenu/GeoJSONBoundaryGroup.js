import React, { Component } from 'react'
import { GeoJSON, LayerGroup } from 'react-leaflet'
import CensusTractPopup from '../Popups/CensusTractPopup'

export default class GeoJSONBoundaryGroup extends Component {
  constructor(props) {
    super(props)
    this.state = {
      featuresLength: props.features.length
    }
    this.layerGroupRef = React.createRef()
  }

  componentDidMount() {
    if (this.layerGroupRef.current.leafletElement.getLayers().length === this.state.featuresLength) {
      this.props.onLoad()
    }
  }

  render() {
    return (
      <LayerGroup ref={this.layerGroupRef}>
        {this.props.features.map((feature, index) => {
          return (
            <GeoJSON
              interactive={this.props.interactive}
              key={`ct-${index}`}
              data={feature['geometry']}
              {...this.props.style(feature)}
            >
              {this.props.interactive && <CensusTractPopup feature={feature} />}
            </GeoJSON>
          )
        })}
      </LayerGroup>
    )
  }
}
