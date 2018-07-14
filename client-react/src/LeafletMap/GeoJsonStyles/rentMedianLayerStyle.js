const rentMedianLayerStyle = (value, thresholdValue) => {
  if (!value || thresholdValue < 55) {
    return {
      color: 'white',
      fillColor: '#252525',
      opacity: 1,
      fillOpacity: 0.3,
      weight: 1
    }
  } else if (value >= 2000) {
    return {
      color: 'white',
      fillColor: '#005a32',
      opacity: 0.5,
      fillOpacity: 0.7,
      weight: 1
    }
  } else if (value >= 1800) {
    return {
      color: 'white',
      fillColor: '#238b45',
      opacity: 0.5,
      fillOpacity: 0.7,
      weight: 1
    }
  } else if (value >= 1600) {
    return {
      color: 'white',
      fillColor: '#41ab5d',
      opacity: 1,
      fillOpacity: 0.7,
      weight: 1
    }
  } else if (value >= 1400) {
    return {
      color: 'white',
      fillColor: '#74c476',
      opacity: 1,
      fillOpacity: 0.7,
      weight: 1
    }
  } else if (value >= 1200) {
    return {
      color: 'white',
      fillColor: '#a1d99b',
      opacity: 1,
      fillOpacity: 0.7,
      weight: 1
    }
  } else if (value >= 1000) {
    return {
      color: 'white',
      fillColor: '#c7e9c0',
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

export default rentMedianLayerStyle
