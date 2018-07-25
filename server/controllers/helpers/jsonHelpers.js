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
            name: row.uniqueId,
            parentBoundaryName: row.building.address,
            source: row.source,
            date: row.date,
            description: row.description,
            penalty: row.penaltyImposed,
            code: row.code
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
            name: row.uniqueId,
            parentBoundaryName: row.building.address,
            source: row.source,
            status: row.status,
            date: row.date,
            description: row.description,
            resolutionDescription: row.resolutionDescription,
            resolutionViolation: row.resolutionViolation,
            resolutionNoAction: row.resolutionNoAction,
            resolutionUnableToInvestigate: row.unableToInvestigate,
            openOverMonth: row.openOverMonth,
            daysToResolve: row.daysToClose,
            closedDate: row.closedDate
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
