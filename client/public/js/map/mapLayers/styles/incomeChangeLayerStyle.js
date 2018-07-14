import Store from '../../../store.js'

// http://colorbrewer2.org/#type=diverging&scheme=RdYlGn&n=7
export const styleIncomeChangeLayers = feature => {
  if (!feature.properties.medianIncomeChange20112017 || feature.properties.totalBuildings < Store.buildingThreshold) {
    return {
      color: 'white',
      fillColor: 'white',
      opacity: 1,
      fillOpacity: 0.8,
      weight: 1
    }
  } else if (feature.properties.medianIncomeChange20112017 >= 40000) {
    return {
      color: 'white',
      fillColor: '#005a32',
      opacity: 0.5,
      fillOpacity: 0.8,
      weight: 1
    }
  } else if (feature.properties.medianIncomeChange20112017 >= 30000) {
    return {
      color: 'white',
      fillColor: '#238b45',
      opacity: 0.5,
      fillOpacity: 0.8,
      weight: 1
    }
  } else if (feature.properties.medianIncomeChange20112017 >= 20000) {
    return {
      color: 'white',
      fillColor: '#41ab5d',
      opacity: 1,
      fillOpacity: 0.8,
      weight: 1
    }
  } else if (feature.properties.medianIncomeChange20112017 >= 10000) {
    return {
      color: 'white',
      fillColor: '#74c476',
      opacity: 1,
      fillOpacity: 0.8,
      weight: 1
    }
  } else if (feature.properties.medianIncomeChange20112017 >= 0) {
    return {
      color: 'white',
      fillColor: '#d9f0a3',
      opacity: 1,
      fillOpacity: 0.8,
      weight: 1
    }
  } else if (feature.properties.medianIncomeChange20112017 >= -20000) {
    return {
      color: 'white',
      fillColor: '#fc8d59',
      opacity: 1,
      fillOpacity: 0.8,
      weight: 1
    }
  } else if (feature.properties.medianIncomeChange20112017 < -20000) {
    return {
      color: 'white',
      fillColor: '#d73027',
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

export const weightFromIncome = income => {
  if (income >= 110000) {
    return 20
  } else if (income >= 90000) {
    return 16
  } else if (income >= 70000) {
    return 12
  } else if (income >= 50000) {
    return 8
  } else if (income >= 30000) {
    return 4
  } else if (income >= 10000) {
    return 2
  } else if (!income) {
    return 1
  } else {
    return 1
  }
}

