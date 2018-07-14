import L from '../../../engines/leaflet/leaflet'

import Store from '../../../store'

export const onCensusTractFeatureEach = (feature, layer) => {
  layer.on({
    click: onCensusTractClick,
    mouseover: onCensusTrackMouseover
  })
}

const onCensusTrackMouseover = e => {
  e.target
    .bindTooltip(
      'Neighborhood: ' + e.target.feature.properties.neighborhood,
      { permanent: false, interactive: false, sticky: false, offset: [0, -50], direction: 'top' },
      e.target
    )
    .openTooltip()
}

const onCensusTractClick = e => {
  // console.log(e.target.feature)

  L.tooltip({ permanent: false, interactive: true, sticky: false }, e.target)
    .setLatLng(e.latlng)
    .setContent(
      'Census Tract: ' +
        e.target.feature.properties.name +
        '<br/>' +
        'Neighborhood: ' +
        e.target.feature.properties.neighborhood +
        '<br/>' +
        'Median Income 2011: ' +
        e.target.feature.properties.medianIncome2011 +
        '<br/>' +
        'Median Income 2017: ' +
        e.target.feature.properties.medianIncome2017 +
        '<br/>' +
        'Median Income Change, 2011 - 2017 ' +
        e.target.feature.properties.medianIncomeChange20112017 +
        '<br/>' +
        'Median Rent 2011: ' +
        e.target.feature.properties.medianRent2011 +
        '<br/>' +
        'Median Rent 2017: ' +
        e.target.feature.properties.medianRent2017 +
        '<br/>' +
        'Median Rent Change 2011 - 2017: ' +
        e.target.feature.properties.medianRentChange20112017 +
        '<br/>' +
        'Total Buildings: ' +
        e.target.feature.properties['totalBuildings'] +
        '<br/>' +
        'Violation Per Bldg: ' +
        e.target.feature.properties['violationsPerBuilding'] +
        '<br/>' +
        'Total Sales: ' +
        e.target.feature.properties['totalSales'] +
        '<br/>' +
        'Total Sales with prior violations: ' +
        e.target.feature.properties['totalSalesPriorViolations'] +
        '<br/>' +
        'Average Sales w Prior Violations: ' +
        e.target.feature.properties['avgSalesPriorViolations'] +
        '%' +
        '<br/>' +
        'Total Permits: ' +
        e.target.feature.properties['totalPermits'] +
        '<br/>' +
        'Avg violation over 3 years before sale: ' +
        e.target.feature.properties['avgViolationCount3YearsBeforeSale'] +
        '<br/>' +
        'Total service calls: ' +
        e.target.feature.properties['totalServiceCalls'] +
        '<br/>' +
        '% service calls resulting in violation: ' +
        e.target.feature.properties['percentServiceCallsWithViolation'] +
        '%'
    )
    .addTo(Store.map)
}
