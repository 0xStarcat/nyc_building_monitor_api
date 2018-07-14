import L from '../engines/leaflet/leaflet'

import {
  ctIncomeLayer,
  ctIncomeChangeLayer,
  ctRentLayer,
  ctRentChangeLayer,
  ctViolationPerBuildingLayer,
  ctTotalSales,
  ctTotalPermits,
  ctTotalSalesPriorViolations,
  ctAvgSalesPriorViolations,
  ctViolations3YearsBeforeSale,
  ctTotalServiceCalls,
  ctPercentServiceCallsWithViolation,
  addStackMarkers,
  removeStackMarkers
} from './mapLayers/censusTractLayers.js'
import Store from '../store'

export const setupMap = () => {
  Store.map = L.map('map', {
    layers: []
  }).setView({ lat: 40.6881, lon: -73.9671 }, 13)

  const switchLayers = {
    'Median Income, 2017': ctIncomeLayer(),
    'Income Change, 2011 - 2017': ctIncomeChangeLayer(),
    'Median Rent, 2017': ctRentLayer(),
    'Rent Change, 2011 - 2017': ctRentChangeLayer(),
    'Violations per Building, 2011 - 2017': ctViolationPerBuildingLayer(),
    'Total Service Calls, 2011 - 2017': ctTotalServiceCalls(),
    'Percent Service Calls with Violation': ctPercentServiceCallsWithViolation(),
    'Total Sales, 2011 - 2017': ctTotalSales(),
    'Total Sales with Prior Violations, 2011-2017': ctTotalSalesPriorViolations(),
    'Avg Sales with Prior Violations, 2011-2017': ctAvgSalesPriorViolations(),
    'Avg # of violations 3 years before sale, 2011-2017': ctViolations3YearsBeforeSale(),
    'Total Permits, 2011 - 2017': ctTotalPermits()
  }

  const neighborhoodLayer = L.geoJSON(Store.boundaryData.neighborhoods, {
    onEachFeature: onNeighborhoodFeatureEach,
    interactive: false,
    style: {
      weight: '1.5',
      color: 'red',
      fillOpacity: 0
    }
  })

  const toggleLayers = {
    'Neighborhood Boundaries': neighborhoodLayer
  }

  Store.map.addLayer(switchLayers['Median Rent, 2017'])
  Store.map.addLayer(toggleLayers['Neighborhood Boundaries'])

  L.control.layers(switchLayers, toggleLayers).addTo(Store.map)
  Store.map.on('baselayerchange', event => {
    removeStackMarkers()
    event.layer.bringToBack()
  })

  L.tileLayer(
    'https://api.tiles.mapbox.com/v4/mapbox.wheatpaste/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoic3RhcmNhdCIsImEiOiJjamlpYmlsc28wbjlmM3FwbXdwaXozcWEzIn0.kLmWiUbmdqNLA1atmnTXXA',
    {
      attribution:
        'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      maxZoom: 18,
      id: 'mapbox.wheatpaste',
      accessToken: 'pk.eyJ1Ijoic3RhcmNhdCIsImEiOiJjamlpYmlsc28wbjlmM3FwbXdwaXozcWEzIn0.kLmWiUbmdqNLA1atmnTXXA'
    }
  ).addTo(Store.map)

  setTimeout(() => Store.map.invalidateSize(), 1)
}

const onNeighborhoodFeatureEach = (feature, layer) => {
  layer.on({
    mouseover: onNeighborhoodMouseover
  })
}
const onNeighborhoodMouseover = e => {
  e.target.options = {
    color: 'red',
    weight: '4',
    fillColor: 'purple',
    onEachFeature: e.target.options.onEachFeature
  }
}
