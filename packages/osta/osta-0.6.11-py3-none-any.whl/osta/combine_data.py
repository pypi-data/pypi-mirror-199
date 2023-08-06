#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import osta.__utils as utils
import pandas as pd
import warnings
from os import listdir
from os.path import isfile, isdir, join
import sys


def combine_data(
        df_list, save_file=None, log_file=False, verbose=True, **args):
    """
    This function merges datasets into one.

    Arguments:
        `df_list`: A list of pandas.DataFrames or paths to files.

        `save_file`: None or a single character value specifying a file path
        where result will be stored. When None, result is not stored to file.
        (By default: save_file=None)

        `log_file`: A boolean value or a single character value for specifying
        where log file will be stored. If True, all the messages are stored to
        a log file that can be found from osta direcotry that is located
        in devices default temporary directory. When False, messages are
        printed to screen and log file is not created.
        (By default: log_file=False)

        'verbose': A boolean value specifying whteher to show a progress bar.
        (By default: verbose=True)

    Details:
        This function can be used to merge multiple datasets into one.
        In detail, the function utilies pd.concat function to merge the data.
        The value of the function comes from the functionality that allows
        user to specify just a directory containing input data, and function
        automatically reads the data and merges individual datasets into one.

    Examples:
        ```
        combine_data("path/to/the/file.csv")

        ```

    Output:
        A pandas.DataFrame

    """
    # INPUT CHECK
    if not (isinstance(df_list, list) or isinstance(df_list, str)):
        raise Exception(
            "'df_list' must be a list of pd.DataFrames or paths to files."
            )
    if not (isinstance(save_file, str) or save_file is None):
        raise Exception(
            "'save_file' must be None or string specifying directory to ",
            "where result files will be stored."
            )
    if not (isinstance(log_file, str) or isinstance(log_file, bool)):
        raise Exception(
            "'log_file' must be a boolean value or a string specifying a path."
            )
    if not isinstance(verbose, bool):
        raise Exception(
            "'verbose' must be True or False."
            )
    # If df_list is directory, check that it is correct directory
    if isinstance(df_list, str) and not isdir(df_list):
        raise Exception(
            "Directory specified by 'df_list' not found."
            )
    elif isinstance(df_list, str) and isdir(df_list):
        # If it is directory, get all the files inside it
        df_list = [join(df_list, f) for f in listdir(df_list)
                   if isfile(join(df_list, f))]
    # INPUT CHECK END
    # If user wants to create a logger file
    if log_file:
        # Create a logger with file
        logger = utils.__start_logging(__name__, log_file)

    # For progress bar, specify the width of it
    progress_bar_width = 50
    # Loop over list elements
    dfs = []
    for i, x in enumerate(df_list):
        # Update the progress bar
        if verbose:
            percent = 100*((i+1)/len(df_list))
            sys.stdout.write('\r')
            sys.stdout.write("Completed: [{:{}}] {:>3}%"
                             .format('='*int(
                                 percent/(100/progress_bar_width)),
                                     progress_bar_width, int(percent)))
            sys.stdout.flush()
        # Check if it is pd.DataFrame. Otherwise try to load it as a local file
        if not isinstance(x, pd.DataFrame):
            # Try to load it
            try:
                df = utils.__detect_format_and_open_file(x, **args)
            except Exception:
                msg = x if isinstance(x, str) else ("element " + str(i))
                warnings.warn(
                    message=f"Failed to open the file {msg}.",
                    category=UserWarning
                    )
        else:
            df = x
        # Convert to list if it is not already
        # (there can be excel file with multiple sheets)
        if not isinstance(df, list):
            df = [df]
        # Add to list
        dfs.extend(df)
    # Combine data to one DF
    df = pd.concat(dfs, ignore_index=True)
    # Check if there are duplicated values
    df = utils.__check_duplicated(df, log_file=log_file, **args)
    # Reset index
    df = df.reset_index(drop=True)
    # Stop progress bar
    if verbose:
        sys.stdout.write("\n")
    # Save file if specified
    if save_file is not None:
        df.to_csv(save_file, index=False)
    # Reset logging; do not capture warnings anymore
    if log_file:
        utils.__stop_logging(logger)
    return df
