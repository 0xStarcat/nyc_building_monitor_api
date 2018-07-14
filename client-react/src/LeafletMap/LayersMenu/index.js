import React, { Component } from 'react'
import {
  Circle,
  FeatureGroup,
  LayerGroup,
  LayersControl,
  Marker,
  Popup,
  Rectangle,
  GeoJSON,
  TileLayer,
  Pane
} from 'react-leaflet'

import {
  incomeMedianLayerStyle,
  incomeChangeLayerStyle,
  rentMedianLayerStyle,
  rentChangeLayerStyle,
  violationsPerBuildingLayerStyle,
  serviceCallsTotalLayerStyle,
  serviceCallsPercentViolationLayerStyle,
  salesTotalLayerStyle,
  salesWithViolationTotalLayerStyle,
  salesWithViolationPercentLayerStyle,
  violationsCountBeforeSaleLayerStyle,
  permitsTotalLayerStyle,
  racePercentWhite2010,
  raceWhitePercentChange
} from '../GeoJsonStyles'

import NeighborhoodsBoundary from './NeighborhoodsBoundary'
import CensusTractPopup from '../Popups/CensusTractPopup'
const { BaseLayer, Overlay } = LayersControl

export default class LayersMenu extends Component {
  constructor(props) {
    super(props)
  }

  render() {
    const center = [51.505, -0.09]
    const rectangle = [[51.49, -0.08], [51.5, -0.06]]

    return (
      <LayersControl collapsed={true} ref={this.props.layerControlRef} position={this.props.position}>
        <BaseLayer checked name="Median Income, 2017">
          <LayerGroup>
            {this.props.store.censusTracts.features.map((feature, index) => {
              return (
                <GeoJSON
                  key={`ct-${index}`}
                  data={feature['geometry']}
                  {...incomeMedianLayerStyle(feature.properties.incomeMedian2017, feature.properties.buildingsTotal)}
                >
                  <CensusTractPopup feature={feature} />
                </GeoJSON>
              )
            })}
          </LayerGroup>
        </BaseLayer>
        <BaseLayer name="Income Change, 2011 - 2017">
          <LayerGroup>
            {this.props.store.censusTracts.features.map((feature, index) => {
              return (
                <GeoJSON
                  key={`ct-${index}`}
                  data={feature['geometry']}
                  {...incomeChangeLayerStyle(
                    feature.properties.incomeChange20112017,
                    feature.properties.buildingsTotal
                  )}
                >
                  <CensusTractPopup feature={feature} />
                </GeoJSON>
              )
            })}
          </LayerGroup>
        </BaseLayer>
        <BaseLayer name="Median Rent, 2017">
          <LayerGroup>
            {this.props.store.censusTracts.features.map((feature, index) => {
              return (
                <GeoJSON
                  key={`ct-${index}`}
                  data={feature['geometry']}
                  {...rentMedianLayerStyle(feature.properties.rentMedian2017, feature.properties.buildingsTotal)}
                >
                  <CensusTractPopup feature={feature} />
                </GeoJSON>
              )
            })}
          </LayerGroup>
        </BaseLayer>
        <BaseLayer name="Rent Change, 2011 - 2017">
          <LayerGroup>
            {this.props.store.censusTracts.features.map((feature, index) => {
              return (
                <GeoJSON
                  key={`ct-${index}`}
                  data={feature['geometry']}
                  {...rentChangeLayerStyle(feature.properties.rentChange20112017, feature.properties.buildingsTotal)}
                >
                  <CensusTractPopup feature={feature} />
                </GeoJSON>
              )
            })}
          </LayerGroup>
        </BaseLayer>
        <BaseLayer name="% White 2010">
          <LayerGroup>
            {this.props.store.censusTracts.features.map((feature, index) => {
              return (
                <GeoJSON
                  key={`ct-${index}`}
                  data={feature['geometry']}
                  {...racePercentWhite2010(feature.properties.racePercentWhite2010, feature.properties.buildingsTotal)}
                >
                  <CensusTractPopup feature={feature} />
                </GeoJSON>
              )
            })}
          </LayerGroup>
        </BaseLayer>
        <BaseLayer name="Violations per Building, 2011 - 2017">
          <LayerGroup>
            {this.props.store.censusTracts.features.map((feature, index) => {
              return (
                <GeoJSON
                  key={`ct-${index}`}
                  data={feature['geometry']}
                  {...violationsPerBuildingLayerStyle(
                    feature.properties.violationsPerBuilding,
                    feature.properties.buildingsTotal
                  )}
                >
                  <CensusTractPopup feature={feature} />
                </GeoJSON>
              )
            })}
          </LayerGroup>
        </BaseLayer>
        <BaseLayer name="Percent Service Calls with Violation">
          <LayerGroup>
            {this.props.store.censusTracts.features.map((feature, index) => {
              return (
                <GeoJSON
                  key={`ct-${index}`}
                  data={feature['geometry']}
                  {...serviceCallsPercentViolationLayerStyle(
                    feature.properties.serviceCallsPercentWithViolation,
                    feature.properties.buildingsTotal
                  )}
                >
                  <CensusTractPopup feature={feature} />
                </GeoJSON>
              )
            })}
          </LayerGroup>
        </BaseLayer>
        <BaseLayer name="Total Sales, 2011 - 2017">
          <LayerGroup>
            {this.props.store.censusTracts.features.map((feature, index) => {
              return (
                <GeoJSON
                  key={`ct-${index}`}
                  data={feature['geometry']}
                  {...salesTotalLayerStyle(feature.properties.salesTotal, feature.properties.buildingsTotal)}
                >
                  <CensusTractPopup feature={feature} />
                </GeoJSON>
              )
            })}
          </LayerGroup>
        </BaseLayer>
        <BaseLayer name="Total Permits, 2011 - 2017">
          <LayerGroup>
            {this.props.store.censusTracts.features.map((feature, index) => {
              return (
                <GeoJSON
                  key={`ct-${index}`}
                  data={feature['geometry']}
                  {...permitsTotalLayerStyle(feature.properties.permitsTotal, feature.properties.buildingsTotal)}
                >
                  <CensusTractPopup feature={feature} />
                </GeoJSON>
              )
            })}
          </LayerGroup>
        </BaseLayer>
        <Overlay ref={this.props.neighborhoodOverlayRef} checked name="Neighborhood Boundaries">
          <Pane style={{ zIndex: 400 }}>
            <NeighborhoodsBoundary
              neighborhoodLayerGroupRef={this.props.neighborhoodLayerGroupRef}
              store={this.props.store}
            />
          </Pane>
        </Overlay>
      </LayersControl>
    )
  }
}
