import React from 'react'

import './style.scss'

const SelectedLayer = props => {
  return (
    <div id="selectedLayer">
      {props.selectedLayer && (
        <div>
          <div className="headerBar">
            <div className="headerTitle">
              <h2>{props.selectedLayer.name}</h2>
            </div>
          </div>
          Neighborhood: {props.selectedLayer.neighborhood}
          <br />
          Median Income 2017: {props.selectedLayer.incomeMedian2017}
          <br />
          Median Rent 2017: {props.selectedLayer.rentMedian2017}
          <br />
          Median Rent Change 2011 - 2017: {props.selectedLayer.rentChange20112017}
          <br />
          % White 2010: {props.selectedLayer.racePercentWhite2010}
          <br />
          Total Buildings: {props.selectedLayer.buildingsTotal}
          <br />
          Violation Per Bldg: {props.selectedLayer.violationsPerBuilding}
          <br />
          Total Sales: {props.selectedLayer.salesTotal}
          <br />
          Total Permits: {props.selectedLayer.permitsTotal}
          <br />
          Service Calls Open after 1 month: {props.selectedLayer.serviceCallsPercentOpenOneMonth}
        </div>
      )}
    </div>
  )
}

export default SelectedLayer
