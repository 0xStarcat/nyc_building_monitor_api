import Store from '../../../store.js'

// http://colorbrewer2.org/#type=sequential&scheme=Greens&n=7

export const avgViolations3YearsBeforeSaleStyle = feature => {
  if (
    !feature.properties.avgViolationCount3YearsBeforeSale ||
    feature.properties.totalBuildings < Store.buildingThreshold
  ) {
    return {
      color: 'white',
      fillColor: 'white',
      opacity: 1,
      fillOpacity: 0.7,
      weight: 1
    }
  } else if (feature.properties.avgViolationCount3YearsBeforeSale >= 6) {
    return {
      color: 'white',
      fillColor: '#005a32',
      opacity: 0.5,
      fillOpacity: 0.7,
      weight: 1
    }
  } else if (feature.properties.avgViolationCount3YearsBeforeSale >= 5) {
    return {
      color: 'white',
      fillColor: '#238443',
      opacity: 0.5,
      fillOpacity: 0.7,
      weight: 1
    }
  } else if (feature.properties.avgViolationCount3YearsBeforeSale >= 4) {
    return {
      color: 'white',
      fillColor: '#41ab5d',
      opacity: 1,
      fillOpacity: 0.7,
      weight: 1
    }
  } else if (feature.properties.avgViolationCount3YearsBeforeSale >= 3) {
    return {
      color: 'white',
      fillColor: '#addd8e',
      opacity: 1,
      fillOpacity: 0.7,
      weight: 1
    }
  } else if (feature.properties.avgViolationCount3YearsBeforeSale >= 2) {
    return {
      color: 'white',
      fillColor: '#d9f0a3',
      opacity: 1,
      fillOpacity: 0.7,
      weight: 1
    }
  } else if (feature.properties.avgViolationCount3YearsBeforeSale >= 1) {
    return {
      color: 'white',
      fillColor: '#ffffcc',
      opacity: 1,
      fillOpacity: 0.7,
      weight: 1
    }
  } else {
    return {
      color: 'white',
      fillColor: '#edf8e9',
      opacity: 1,
      fillOpacity: 0.7,
      weight: 1
    }
  }
}
