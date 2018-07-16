'use strict';

module.exports = function (sequelize, DataTypes) {
  return sequelize.define('racial_makeup', {
    id: {
      type: DataTypes.INTEGER,
      field: 'id',
      primaryKey: true
    },
    borough_id: {
      type: DataTypes.INTEGER,
      field: 'borough_id'
    },
    community_district_id: {
      type: DataTypes.INTEGER,
      field: 'community_district_id'
    },
    neighborhood_id: {
      type: DataTypes.INTEGER,
      field: 'neighborhood_id'
    },
    census_tract_id: {
      type: DataTypes.INTEGER,
      field: 'census_tract_id'
    },
    percent_white_2010: {
      type: DataTypes.FLOAT,
      field: 'percent_white_2010'
    }
  }, {
    tableName: 'racial_makeups'
  });
};