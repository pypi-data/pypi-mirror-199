"""
Package for working with Cypress Creek Renewables Dashboard process
"""
import warnings

from pandas.errors import PerformanceWarning
warnings.simplefilter(action='ignore', category=(FutureWarning, PerformanceWarning)) # type: ignore
warnings.filterwarnings(action='ignore', message='divide by zero')

from collections import namedtuple


# Create namedtuple instances to store information to pass between modules
Colmap = namedtuple('Colmap', ['col_list', 'col_avg'])


print('Importing DashboardSession')
from ccrenew import (
    all_df_keys,
    cloud_data
)
from ccrenew.dashboard.utils.dashboard_utils import func_timer
from ccrenew.data_determination import daylight
from ccrenew.dashboard.plotting.plots import Plotter
from ccrenew.dashboard.session import DashboardSession
from ccrenew.dashboard.project import Project
from ccrenew.dashboard.utils.project_neighbors import (
    find_nearby_projects,
    find_nearby_similar_projects,
    find_similar_projects
)


# Helper functions
class Helpers:
    def __init__(self):
        self.df_keys = all_df_keys
        self.find_nearby_projects = find_nearby_projects
        self.find_nearby_similar_projects = find_nearby_similar_projects
        self.find_similar_projects = find_similar_projects
        self.get_sat_weather = cloud_data.get_sat_weather
        self.daylight = daylight

helpers = Helpers()