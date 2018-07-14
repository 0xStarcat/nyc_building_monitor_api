import L from '../../engines/leaflet/leaflet'

import Store from '../../store'
import { styleIncomeLayers } from './styles/incomeLayerStyle.js'
import { styleRentLayers } from './styles/rentLayerStyle.js'
import { styleIncomeChangeLayers } from './styles/incomeChangeLayerStyle.js'
import { styleRentChangeLayers } from './styles/rentChangeLayerStyle.js'
import { violationPerBuildingStyle } from './styles/violationPerBuildingLayerStyle.js'
import { totalSalesStyle } from './styles/totalSalesStyle.js'
import { totalPermitsStyle } from './styles/totalPermitsStyle.js'
import { totalSalesPriorViolationsStyle } from './styles/totalSalesPriorViolationsStyle.js'
import { avgSalesPriorViolationsStyle } from './styles/avgSalesPriorViolationsStyle.js'
import { avgViolations3YearsBeforeSaleStyle } from './styles/avgViolations3YearsBeforeSaleStyle.js'
import { totalServiceCallsStyle } from './styles/totalServiceCallsStyle.js'
import { percentServiceCallsWithViolationStyle } from './styles/percentServiceCallsWithViolationStyle'

import { onCensusTractFeatureEach } from './bindings/ctBindings.js'
export const ctIncomeLayer = () => {
  return L.geoJSON(Store.boundaryData.censusTracts, {
    onEachFeature: onCensusTractFeatureEach,
    style: styleIncomeLayers,
    elevation: 500,
    elevationMode: 'heightAboveGround'
  })
}

export const ctIncomeChangeLayer = () => {
  return L.geoJSON(Store.boundaryData.censusTracts, {
    onEachFeature: onCensusTractFeatureEach,
    style: styleIncomeChangeLayers
  })
}

export const ctRentLayer = () => {
  return L.geoJSON(Store.boundaryData.censusTracts, {
    onEachFeature: onCensusTractFeatureEach,
    style: styleRentLayers
  })
}

export const addStackMarkers = () => {
  var myCenter = new L.LatLng(40.6881, -73.9671)
  Store.stack = L.marker.stack(myCenter, {
    icons: [
      L.icon.chip({ color: 'red' }),
      L.icon.chip({ color: 'red' }),
      L.icon.chip({ color: 'blue' }),
      L.icon.chip({ color: 'lime' })
    ],
    stackOffset: [0, -5]
  })

  Store.map.addLayer(Store.stack)
}

export const removeStackMarkers = () => {
  Store.map.removeLayer(Store.stack)
}

export const ctRentChangeLayer = () => {
  return L.geoJSON(Store.boundaryData.censusTracts, {
    onEachFeature: onCensusTractFeatureEach,
    style: styleRentChangeLayers
  })
}

export const ctViolationPerBuildingLayer = () => {
  return L.geoJSON(Store.boundaryData.censusTracts, {
    onEachFeature: onCensusTractFeatureEach,
    style: violationPerBuildingStyle
  })
}

export const ctTotalSales = () => {
  return L.geoJSON(Store.boundaryData.censusTracts, {
    onEachFeature: onCensusTractFeatureEach,
    style: totalSalesStyle
  })
}

export const ctTotalPermits = () => {
  return L.geoJSON(Store.boundaryData.censusTracts, {
    onEachFeature: onCensusTractFeatureEach,
    style: totalPermitsStyle
  })
}

export const ctTotalSalesPriorViolations = () => {
  return L.geoJSON(Store.boundaryData.censusTracts, {
    onEachFeature: onCensusTractFeatureEach,
    style: totalSalesPriorViolationsStyle
  })
}

export const ctAvgSalesPriorViolations = () => {
  return L.geoJSON(Store.boundaryData.censusTracts, {
    onEachFeature: onCensusTractFeatureEach,
    style: avgSalesPriorViolationsStyle
  })
}

export const ctViolations3YearsBeforeSale = () => {
  return L.geoJSON(Store.boundaryData.censusTracts, {
    onEachFeature: onCensusTractFeatureEach,
    style: avgViolations3YearsBeforeSaleStyle
  })
}

export const ctTotalServiceCalls = () => {
  return L.geoJSON(Store.boundaryData.censusTracts, {
    onEachFeature: onCensusTractFeatureEach,
    style: totalServiceCallsStyle
  })
}

export const ctPercentServiceCallsWithViolation = () => {
  return L.geoJSON(Store.boundaryData.censusTracts, {
    onEachFeature: onCensusTractFeatureEach,
    style: percentServiceCallsWithViolationStyle
  })
}
