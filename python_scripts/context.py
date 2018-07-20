import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from seeds import boroughs_seeds
from seeds import community_districts_seeds
from seeds import neighborhoods_seeds
from seeds import census_tracts_seeds
from seeds import buildings_seeds
from seeds import incomes_seeds
from seeds import rents_seeds
from seeds import racial_makeup_seeds
from seeds import violations_seeds
from seeds import sales_seeds
from seeds import permits_seeds
from seeds import permit_clusters_seeds
from seeds import conversions_seeds
from seeds import evictions_seeds
from seeds import service_calls_seeds
from seeds import building_events_seeds

from helpers import csv_helpers