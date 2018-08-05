module.exports = {
  constructNeighborhoodJson: data => {
    return {
      features: data.map(row => {
        return {
          type: 'Feature',
          geometry: JSON.parse(row.geometry),
          properties: {
            id: row.id,
            name: row.name,
            parentBoundaryName: row.borough_name, //boroughData.find(borough => borough.id === row.borough_id).name,
            incomeMedian2017: parseFloat(row.incomeMedian2017).toFixed(2),
            rentMedian2017: parseFloat(row.rentMedian2017).toFixed(2),
            rentChange20112017: parseFloat(row.rentChange20112017).toFixed(2),
            racePercentWhite2010: parseFloat(row.racePercentWhite2010).toFixed(2),
            buildingsTotal: parseFloat(row.total_buildings),
            residentialBuildingsTotal: parseFloat(row.total_residential_buildings),
            serviceCallsTotal: parseFloat(row.total_service_calls),
            serviceCallsPercentOpenOneMonth: parseFloat(
              (row.total_service_calls_open_over_month / row.total_service_calls) * 100
            ).toFixed(2),
            averageDaysToResolveServiceCalls: parseFloat(row.service_calls_average_days_to_resolve).toFixed(2),
            violationsTotal: parseFloat(row.total_violations),
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
            rentChange20112017: parseFloat((row.rent || {}).median_rent_change_2011_2017).toFixed(2),
            racePercentWhite2010: (row.racial_makeup || {}).percent_white_2010,
            buildingsTotal: parseFloat(row.totalBuildings),
            residentialBuildingsTotal: parseFloat(row.totalResidentialBuildings),
            serviceCallsTotal: parseFloat(row.totalServiceCalls),
            serviceCallsPerBuilding: String((row.totalServiceCalls / row.totalBuildings).toFixed(2)),
            serviceCallsPercentOpenOneMonth: parseFloat(
              (row.totalServiceCallsOpenOverMonth / row.totalServiceCalls) * 100
            ).toFixed(2),
            averageDaysToResolveServiceCalls: parseFloat(row.averageDaysToResolveServiceCalls).toFixed(2),
            violationsTotal: parseFloat(row.totalViolations),
            violationsPerBuilding: String((row.totalViolations / row.totalBuildings).toFixed(2)),
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
            residentialUnits: row.residentialUnits,
            isResidential: row.isResidential,
            representativePoint: JSON.parse(row.representativePoint),
            buildingClass: row.buildingClass,
            violationsTotal: row.totalViolations,
            serviceCallsTotal: row.totalServiceCalls,
            serviceCallsPercentOpenOneMonth: parseFloat(
              (row.totalServiceCallsOpenOverMonth / row.totalServiceCalls) * 100
            ).toFixed(2),
            averageDaysToResolveServiceCalls: parseFloat(row.averageDaysToResolveServiceCalls).toFixed(2),
            boroCode: row.boroCode,
            block: row.block,
            lot: row.lot
          }
        }
      })
    }
  },
  constructBuildingSearchJson: data => {
    return {
      results: data.map(row => {
        return {
          id: row.id,
          address: row.address,
          boroughName: row.borough.name,
          representativePoint: JSON.parse(row.representativePoint)
        }
      })
    }
  },
  constructUpdateJson: data => {
    return {
      rows: data.map(row => {
        return {
          date: row.date,
          newViolations: row.newViolations,
          newServiceCalls: row.newServiceCalls,
          resolvedViolations: row.resolvedViolations,
          resolvedServiceCalls: row.resolvedServiceCalls
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
            code: row.code,
            status: row.status,
            statusDescription: row.statusDescription
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
            closedDate: row.closedDate,
            complaintType: row.complaintType
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
