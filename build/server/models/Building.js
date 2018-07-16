'use strict';

module.exports = function (sequelize, DataTypes) {
  return sequelize.define('building', {
    id: {
      type: DataTypes.INTEGER,
      field: 'id',
      primaryKey: true
    },
    block: {
      type: DataTypes.STRING,
      field: 'block'
    },
    lot: {
      type: DataTypes.STRING,
      field: 'lot'
    },
    address: {
      type: DataTypes.STRING,
      field: 'address'
    },
    year_built: {
      type: DataTypes.STRING,
      field: 'year_built'
    },
    geometry: {
      type: DataTypes.JSON,
      field: 'geometry'
    },
    census_tract_id: {
      type: DataTypes.INTEGER,
      field: 'census_tract_id'
    },
    neighborhood_id: {
      type: DataTypes.INTEGER,
      field: 'neighborhood_id'
    }
  }, {
    tableName: 'buildings'
  });
};