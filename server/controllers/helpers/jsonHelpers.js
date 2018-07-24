module.exports = {
  constructNeighborhoodJson: (data, boroughData) => {
    return {
      features: data.map(row => {
        return {
          type: 'Feature',
          geometry: JSON.parse(row.geometry),
          properties: {
            id: row.id,
            name: row.name,
            parentBoundaryName: row.borough_name, //boroughData.find(borough => borough.id === row.borough_id).name,
            incomeMedian2017: parseFloat(row.incomeMedian2017),
            rentMedian2017: parseFloat(row.rentMedian2017),
            rentChange20112017: parseFloat(row.rentChange20112017),
            racePercentWhite2010: row.racePercentWhite2010,
            buildingsTotal: parseFloat(row.total_buildings),
            serviceCallsPercentOpenOneMonth: parseFloat(
              (row.total_service_calls_open_over_month / row.total_service_calls) * 100
            ).toFixed(2),
            violationsPerBuilding: parseFloat((row.total_violations / row.total_buildings).toFixed(2)),
            representativePoint: JSON.parse(row.representative_point)
          }
        }
      })
    }
  },
  constructCensusTractJson: (data, boroughData) => {
    return {
      features: data.map(row => {
        return {
          type: 'Feature',
          geometry: JSON.parse(row.geometry),
          properties: {
            id: row.id,
            name: row.name,
            parentBoundaryName: row.neighborhood.name,
            topParentBoundaryName: boroughData.find(borough => borough.id === row.borough_id).name,
            incomeMedian2017: parseFloat((row.income || {}).median_income_2017),
            rentMedian2017: parseFloat((row.rent || {}).median_rent_2017),
            rentChange20112017: parseFloat((row.rent || {}).median_rent_change_2011_2017),
            racePercentWhite2010: (row.racial_makeup || {}).percent_white_2010,
            buildingsTotal: parseFloat(row.totalBuildings),
            serviceCallsPercentOpenOneMonth: parseFloat(
              (row.totalServiceCallsOpenOverMonth / row.totalServiceCalls) * 100
            ).toFixed(2),
            violationsPerBuilding: parseFloat((row.totalViolations / row.totalBuildings).toFixed(2)),
            representativePoint: JSON.parse(row.representativePoint)
          }
        }
      })
    }
  },
  constructBuildingJson: data => {
    return {
      features: data.map(row => {
        return {
          type: 'Feature',
          geometry: JSON.parse(row['geometry']),
          properties: {
            id: row.id,
            name: row.address,
            parentBoundaryName: row.neighborhood.name,
            topParentBoundaryName: row.borough.name,
            yearBuild: row.yearBuilt,
            violationsTotal: row.totalViolations,
            salesTotal: row.totalSales,
            serviceCallsTotal: row.totalServiceCalls,
            serviceCallsPercentOpenOneMonth: row.totalServiceCallsOpenOverMonth
          }
        }
      })
    }
  },
  constructViolationJson: data => {
    return {
      features: data.map(row => {
        return {
          type: 'Feature',
          properties: {
            name: { label: 'Id', value: row.unique_key },
            parentBoundaryName: { label: 'Address', value: row.building.address },
            source: { label: 'Source', value: row.source },
            date: { label: 'Date', value: row.date },
            description: { label: 'Description', value: row.description },
            penalty: { label: 'Penalty', value: row.penaltyImposed }
          }
        }
      })
    }
  },
  constructServiceCallJson: data => {
    return {
      features: data.map(row => {
        return {
          type: 'Feature',
          properties: {
            name: { label: 'Id', value: row.violation_id },
            parentBoundaryName: { label: 'Address', value: row.building.address },
            source: { label: 'Source', value: row.source },
            status: { label: 'Status', value: row.status },
            date: { label: 'Date', value: row.date },
            description: { label: 'Description', value: row.description },
            resolutionDescription: { label: 'Resolution Description', value: row.resolutionDescription },
            resolutionViolation: { label: 'Resulted in violation', value: row.resolutionViolation },
            resolutionNoAction: { label: 'Resulted in no action', value: row.resolutionNoAction },
            resolutionUnableToInvestigate: { label: 'Unable to investigate', value: row.unableToInvestigate },
            openOverMonth: { label: 'Open for over 1 month', value: row.openOverMonth },
            daysToResolve: { label: 'Days to Resolve', value: row.daysToClose }
          }
        }
      })
    }
  },
  constructSaleJson: data => {
    return {
      features: data.map(row => {
        return {
          type: 'Feature',
          properties: {
            name: { label: 'Id', value: row.building.address },
            date: { label: 'Date', value: row.date },
            price: { label: 'Price', value: row.price }
          }
        }
      })
    }
  }
}
