module.exports = function(sequelize, DataTypes) {
  return sequelize.define(
    'income',
    {
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
      median_income_2011: {
        type: DataTypes.FLOAT,
        field: 'median_income_2011'
      },
      median_income_2017: {
        type: DataTypes.FLOAT,
        field: 'median_income_2017'
      },
      median_income_change_2011_2017: {
        type: DataTypes.FLOAT,
        field: 'median_income_change_2011_2017'
      }
    },
    {
      tableName: 'incomes'
    }
  )
}
