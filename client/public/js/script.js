import { fetchData } from './fetchData'
import { setupMap } from './map/map.js'
import Store from './store'

/* eslint-disable */

fetchData()
  .then(() => {
    console.log('fetch complete')
    setupMap()
    // setupMapMarkers()
    console.log('setup complete')
  })
  .catch(error => {
    console.log('error ', error)
  })

const geojsonMarkerOptions = {
  radius: 1,
  fillColor: 'hotpink',
  color: 'hotpink',
  weight: 1,
  opacity: 1,
  fillOpacity: 0.8
}

const setupGeoJsonBoundaries = () => {
  var map = L.map('map', { layers: [mapLayers.Rent] }).setView({ lat: 40.6881, lon: -73.9671 }, 13)

  L.tileLayer(
    'https://api.tiles.mapbox.com/v4/mapbox.wheatpaste/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoic3RhcmNhdCIsImEiOiJjamlpYmlsc28wbjlmM3FwbXdwaXozcWEzIn0.kLmWiUbmdqNLA1atmnTXXA',
    {
      attribution:
        'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      maxZoom: 18,
      id: 'mapbox.wheatpaste',
      accessToken: 'pk.eyJ1Ijoic3RhcmNhdCIsImEiOiJjamlpYmlsc28wbjlmM3FwbXdwaXozcWEzIn0.kLmWiUbmdqNLA1atmnTXXA'
    }
  ).addTo(map)

  setTimeout(() => map.invalidateSize(), 1)

  L.control.layers(mapLayers).addTo(map)

  L.geoJSON(Store.boundaryData.neighborhoods, {
    onEachFeature: onNeighborhoodFeatureEach,
    interactive: false,
    style: {
      weight: '1.5',
      color: '#e10033',
      fillOpacity: 0
    }
  }).addTo(map)
}

const setupMapMarkers = () => {
  // setupViolationMarkers("2015")
  setupNewBuildingMarkers()
}

const setupNewBuildingMarkers = year => {
  let filtered_data = Store.geoJson.newBuildings
  // filtered_data.features = Store.violationData.features.filter((feature) => feature["properties"]["issue_date"].substring(0, 4) === year)
  L.geoJSON(filtered_data, {
    pointToLayer: (feature, latlng) => {
      return L.circleMarker(latlng, geojsonMarkerOptions)
    },
    onEachFeature: onViolationEachFeature
  }).addTo(map)
}

const setupViolationMarkers = year => {
  let filtered_data = Store.geoJson.violationData
  filtered_data.features = Store.violationData.features.filter(
    feature => feature['properties']['issue_date'].substring(0, 4) === year
  )
  L.geoJSON(filtered_data, {
    pointToLayer: (feature, latlng) => {
      return L.circleMarker(latlng, geojsonMarkerOptions)
    },
    onEachFeature: onViolationEachFeature
  }).addTo(map)
}

function onCensusTractFeatureEach(feature, layer) {
  layer.on({
    click: onCensusTractClick,
    mouseover: onCensusTrackMouseover,
    mouseout: onCensusTractMouseout
  })
}

function onNeighborhoodFeatureEach(feature, layer) {
  layer.on({
    mouseover: onNeighborhoodMouseover
  })
}

function onNewBuildingEachFeature(feature, layer) {}

function onViolationEachFeature(feature, layer) {
  layer.on({
    click: onViolationClick
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

function onNeighborhoodClick(e, layer) {
  L.popup()
    .setLatLng(e.latlng)
    .setContent(e.target.feature.properties.neighborhood)
    .openOn(map)
}

function onViolationClick(e) {
  console.log(e.target.feature.geometry.coordinates)
}
