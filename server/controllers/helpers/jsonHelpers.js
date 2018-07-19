module.exports = {
  constructCensusTractJson: (data, boroughData) => {
    return {
      features: data.map(row => {
        return {
          type: 'Feature',
          geometry: JSON.parse(row.geometry),
          properties: {
            id: { label: '', value: row.id },
            name: { label: 'Number', value: row.name },
            parentBoundaryName: { label: 'Neighborhood', value: row.neighborhood.name },
            topParentBoundaryName: {
              label: 'Borough',
              value: boroughData.find(borough => borough.id === row.borough_id).name
            },
            // churnPercent: parseFloat((row.total_sales / row.total_buildings) * 100),
            incomeMedian2017: {
              label: 'Median Income (2017)',
              value: parseFloat((row.income || {}).median_income_2017)
            },
            incomeChange20112017: {
              label: 'Income Change',
              value: parseFloat((row.income || {}).median_income_change_2011_2017)
            },
            rentMedian2017: { label: 'Median Rent (2017)', value: parseFloat((row.rent || {}).median_rent_2017) },
            rentChange20112017: {
              label: 'Rent Change',
              value: parseFloat((row.rent || {}).median_rent_change_2011_2017)
            },
            racePercentWhite2010: {
              label: 'White Population (2010)',
              value: (row.racial_makeup || {}).percent_white_2010
            },
            buildingsTotal: { label: 'Total Buildings', value: parseFloat(row.total_buildings) },
            salesTotal: { label: 'Total Sales', value: parseFloat(row.total_sales) },
            permitsTotal: { label: 'Total New Building Permits', value: parseFloat(row.total_permits) },
            serviceCallsTotal: { label: 'Total 311 Calls', value: parseFloat(row.total_service_calls) },
            serviceCallsPercentOpenOneMonth: {
              label: '311 Calls Open ( > 1 Month)',
              value: parseFloat((row.total_service_calls_open_over_month / row.total_service_calls) * 100).toFixed(2)
            },
            // serviceCallsPercentWithViolation: parseFloat(
            //   ((row.total_service_calls_with_violation_result / row.total_service_calls) * 100).toFixed(2)
            // ),
            // serviceCallsPercentNoAction: parseFloat(
            //   ((row.total_service_calls_with_no_action_result / row.total_service_calls) * 100).toFixed(2)
            // ),
            // serviceCallsPercentUnresolved: parseFloat(
            //   ((row.total_service_calls_unresolved_result / row.total_service_calls) * 100).toFixed(2)
            // ),
            // salesTotalPriorViolations: parseFloat(row.total_sales_prior_violations),
            // salesPercentPriorViolations: parseFloat(
            //   ((row.total_sales_prior_violations / row.total_sales) * 100).toFixed(2)
            // ),
            // violationsAverageBeforeSalePerBuilding: parseFloat(row.avg_violation_count_3years_before_sale),
            violationsTotal: { label: 'Total Violations', value: parseFloat(row.total_violations) },
            violationsPerBuilding: {
              label: 'Violations per Building',
              value: parseFloat((row.total_violations / row.total_buildings).toFixed(2))
            },
            representativePoint: JSON.parse(row.representativePoint)
            // violationsNonCommunityPerBuilding: parseFloat(
            //   ((row.total_violations - row.total_service_calls_with_violation_result) / row.total_buildings).toFixed(2)
            // ),
            // violationsPercentNonCommunity: parseFloat(
            //   (row.total_service_calls_with_violation_result / row.total_violations).toFixed(2) * 100
            // )
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
            id: { label: 'Id', value: row.id },
            name: { label: 'Address', value: row.address },
            parentBoundaryName: { label: 'Neighborhood', value: row.neighborhood.name },
            topParentBoundaryName: { label: 'Borough', value: row.borough.name },
            yearBuild: { label: 'Year Build', value: row.yearBuilt },
            violationsTotal: { label: 'Total Violations', value: row.totalViolations },
            salesTotal: { label: 'Total Sales', value: row.totalSales },
            serviceCallsTotal: { label: 'Total 311 Calls', value: row.totalServiceCalls },
            serviceCallsPercentOpenOneMonth: {
              label: '311 Calls Open ( > 1 Month)',
              value: row.totalServiceCallsOpenOverMonth
            }
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
            date: { label: 'Date', value: row.date },
            description: { label: 'Description', value: row.description },
            resolutionViolation: { label: 'Resulted in violation', value: row.resolution_violation },
            resolutionNoAction: { label: 'Resulted in no action', value: row.resolution_no_action },
            resolutionUnableToInvestigate: { label: 'Unable to investigate', value: row.unable_to_investigate },
            openOverMonth: { label: 'Open for over 1 month', value: row.open_over_month }
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
            name: { label: 'Id', value: row.unique_key },
            parentBoundaryName: { label: 'Address', value: row.building.address },
            date: { label: 'Date', value: row.date },
            price: { label: 'Price', value: row.price },
            address: { label: 'Address', value: row.building.address }
          }
        }
      })
    }
  }
}
