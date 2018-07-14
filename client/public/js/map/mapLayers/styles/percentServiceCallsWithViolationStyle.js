import Store from '../../../store.js'

// http://colorbrewer2.org/#type=diverging&scheme=RdYlGn&n=7
export const percentServiceCallsWithViolationStyle = feature => {
  if (
    !feature.properties.percentServiceCallsWithViolation ||
    feature.properties.totalBuildings < Store.buildingThreshold
  ) {
    return {
      color: 'white',
      fillColor: 'white',
      opacity: 1,
      fillOpacity: 0.8,
      weight: 1
    }
  } else if (feature.properties.percentServiceCallsWithViolation >= 60) {
    return {
      color: 'white',
      fillColor: '#005a32',
      opacity: 0.5,
      fillOpacity: 0.8,
      weight: 1
    }
  } else if (feature.properties.percentServiceCallsWithViolation >= 50) {
    return {
      color: 'white',
      fillColor: '#238443',
      opacity: 0.5,
      fillOpacity: 0.8,
      weight: 1
    }
  } else if (feature.properties.percentServiceCallsWithViolation >= 40) {
    return {
      color: 'white',
      fillColor: '#41ab5d',
      opacity: 1,
      fillOpacity: 0.8,
      weight: 1
    }
  } else if (feature.properties.percentServiceCallsWithViolation >= 30) {
    return {
      color: 'white',
      fillColor: '#addd8e',
      opacity: 1,
      fillOpacity: 0.8,
      weight: 1
    }
  } else if (feature.properties.percentServiceCallsWithViolation >= 20) {
    return {
      color: 'white',
      fillColor: '#d9f0a3',
      opacity: 1,
      fillOpacity: 0.8,
      weight: 1
    }
  } else if (feature.properties.percentServiceCallsWithViolation >= 10) {
    return {
      color: 'white',
      fillColor: '#ffffcc',
      opacity: 1,
      fillOpacity: 0.8,
      weight: 1
    }
  } else if (feature.properties.percentServiceCallsWithViolation >= 0) {
    return {
      color: 'white',
      fillColor: '#edf8e9',
      opacity: 1,
      fillOpacity: 0.8,
      weight: 1
    }
  } else {
    return {
      color: 'white',
      fillColor: 'lightgray',
      opacity: 1,
      fillOpacity: 0.8,
      weight: 1
    }
  }
}
