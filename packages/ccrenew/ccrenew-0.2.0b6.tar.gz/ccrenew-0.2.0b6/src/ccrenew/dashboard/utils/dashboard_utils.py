"""Utilities for running Dashboard process"""

from __future__ import annotations

from datetime import (
    date,
    datetime,
    timedelta
)
import functools
import logging
import os
from pandas import (
    DataFrame,
    read_csv,
    read_excel
)
import re
import sys
from time import time

from ccrenew import all_df_keys


# logger = logging.getLogger(__name__)
df_keys = all_df_keys


class project_dict(dict):
    def __repr__(self):
        print_str = ''
        for key, value in self.items():
            if value.processed:
                proc = ': Processed'
            else:
                proc = ': Unprocessed'
            print_str = print_str + key + proc + '\n'

        return print_str


def dict_insert(dict_, key, value):
    """Checks if a key already exists in dict, creates new key if not.
    Prevents overwriting of existing dictionary entries.

    Args:
        dict_ (dict): Dictionary to update.
        key (str): Key to check.
        value (str): Value to update if key doesn't exist.

    Returns:
        dict: Updated dictionary.
    """
    if key in dict_:
        pass
    else:
        dict_[key] = value
    return dict_

def picklefy_project_name(project_name):
    """Modifies the project name for pickling.

    Args:
        project_name (str): The "official" project name with spaces, commas, apostrophe's, and all that fun stuff
        year (int): The year to save for the pickle. Defaults to the current year.

    Returns:
        str: The picklefied project name.
    """
    project_name = re.sub(r"(,\s)|[,\s]", "_", project_name)
    project_name = re.sub(r"[']", "", project_name)

    return project_name

def get_snow_df(dashboard_folder, data_source, file_format):
    """Pulls snow data & returns a dataframe. Temporary fix for now, need to
    update path references

    Returns:
        DataFrame: Snow data
    """
    if file_format == 'xlsx':
        snow_file = os.path.join(dashboard_folder, 'Python_Functions', 'Snow Losses', '{}Operating-States-snowfall.xlsx'.format(data_source))
        raw_snow_df = read_excel(snow_file, index_col=0)
    else:
        snow_file = os.path.join(dashboard_folder, 'Python_Functions', 'Snow Losses', '{}Operating-States-snowfall.csv'.format(data_source))
        raw_snow_df = read_csv(snow_file, index_col=0)

    return raw_snow_df, snow_file

def retrieve_s3_df(bucket, key):
# helper function to get data from s3
    path = "s3://{b}/{k}".format(b=bucket, k=key)
    try:
        df = read_csv(path, index_col=0, parse_dates=True)
        df = df.loc[~df.index.duplicated(), :]
    except IOError:
        return DataFrame()
    return df

# Decorator function for timing the execution of functions
def func_timer(func):
    """Decorator for timing the execution of functions.

    Args:
        func (function): Function to time.
    """
    # Initiate logger
    logger = logging.getLogger('timer')

    @functools.wraps(func)
    def timer(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        elapsed = time() - start

        # Build custom message for the logger so it doesn't just show that each
        # call came from the `timer()` function
        # Python 2 compatibility
        # Python 2 compatibility
        if sys.version_info.major == 3:
            file_str = 'File: {}'.format(os.path.basename(func.__code__.co_filename))
            line_str = 'Line: {}'.format(func.__code__.co_firstlineno)
        else:
            file_str = 'File: {}'.format(os.path.basename(func.func_code.co_filename))
            line_str = 'Line: {}'.format(func.func_code.co_firstlineno)

        log_msg = {
            'file': file_str,
            'module': 'Module: {}'.format(func.__module__),
            'function': 'Function: {}'.format(func.__name__),
            'line_no': line_str,
            'func_name': func.__name__,
            'elapsed': elapsed
        }
        # Check if the function call comes from a project, if so we'll add the project name to the log message
        try:
            log_msg['project_name'] = args[0].project_name
            message = '{file}\t{module}\t{function}\t{line_no}\tFunction call `{func_name}` for {project_name} complete. Total time: {elapsed:7.3f}s'.format(**log_msg)
        except AttributeError:
            message = '{file}\t{module}\t{function}\t{line_no}\tFunction call `{func_name}` complete. Total time: {elapsed:7.3f}s'.format(**log_msg)
        logger.debug(message)

        return result
    return timer

def update_config(func):
    """Decorator to update the config file if necessary before running a function.

    Args:
        func (function): Function that will need an updated config file.
    """
    @functools.wraps(func)
    def check_config(self, *args, **kwargs):
        if self.last_update_config != os.path.getmtime(self.config_filepath):
            self._parse_config_file()
        return func(self, *args, **kwargs)
    return check_config
