# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 11:14:32 2020

@author: Martín Carlos Araya <martinaraya@gmail.com>
"""

__version__ = '0.80.6'
__release__ = 20230218
__all__ = ['concat', 'merge']

from simpandas.frame import SimDataFrame
from simpandas.series import SimSeries
import pandas as pd
import logging


def concat(objs, axis=0, join='outer', ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False,
           sort=False, copy=True, squeeze=True):
    """
    wrapper of pandas.concat enhanced with units support

    Return:
        SimDataFrame
    """
    if type(objs) is not list:
        raise TypeError("objs must be a list of DataFrames or SimDataFrames")
    if len(objs) == 1:
        logging.warning("Only 1 DataFrame received.")
        return [objs][0]

    sim_objs = [ob for ob in objs if type(ob) in (SimDataFrame, SimSeries)]
    if len(sim_objs) == 0:
        merged_units = None
        merged_params_ = {}
    elif len(sim_objs) == 1:
        merged_units = sim_objs[0].get_units()
        merged_params_ = sim_objs[0].params_
    else:
        merged_units = merge_units(sim_objs)
        merged_params_ = merge_SimParameters(sim_objs)

    index_units = None
    for ob in objs:
        if hasattr(ob, 'index_units') and type(ob.index_units) is str and len(ob.index_units) > 0:
            index_units = ob.index_units
            break

    if index_units is None:
        df_objs = [(ob.to(merged_units).as_pandas()
                    if type(ob) in (SimSeries, SimDataFrame) else ob)
                   for ob in objs]
    else:
        df_objs = [(ob.index_to(index_units).to(merged_units).as_pandas()
                    if type(ob) in (SimSeries, SimDataFrame) else ob)
                   for ob in objs]

    if 'units' in merged_params_:
        del merged_params_['units']

    sdf = pd.concat(df_objs, axis=axis, join=join, ignore_index=ignore_index, keys=keys, levels=levels, names=names,
                    verify_integrity=verify_integrity, sort=sort, copy=copy)
    if len(sim_objs) > 0:
        sdf = SimDataFrame(data=sdf, units=merged_units, **merged_params_)

    if squeeze:
        return sdf.squeeze()
    else:
        return sdf


def merge_index(left, right, how='outer', *, drop_duplicates=True, keep='first'):
    """
    returns a left and right Frames or Series reindex with a common index.

    Parameters
    ----------
    left : Series, SimSeries, DataFrame or SimDataFrame
        The left frame to merge
    right : Series, SimSeries, DataFrame or SimDataFrame
        The right frame to merge
    how : str, optional
        The merge method to be used.
        The default is 'outer'.
    drop_duplicates : boo, optional
        If True, drop lines with duplicated indexes to avoid reindexing error due to repeated index.
        If False, will drop the lines of duplicated indexes to avoid error and then put back line.
    keep : str
        if `drop_duplicates` is True, indicates witch row to keep when the item is duplicated,
    Raises
    ------
    ValueError
        If how parameter is not valid.

    Returns
    -------
    Series, SimSeries, DataFrame or SimDataFrame reindex to the merged index.

    """

    def merge_append(frame, new_index):
        if type(frame) is SimSeries:
            frame = frame.sdf
        elif type(frame) is pd.Series:
            frame = SimDataFrame(frame)
        if frame.index.duplicated('first').sum() > 0:
            dup_frame = frame[frame.index.duplicated('first')]
            temp = frame[~frame.index.duplicated('first')].reindex(index=new_index)
            new_frame = None
            for dup in range(len(dup_frame.index)):
                if new_frame is None:
                    new_frame = temp.iloc[0:list(temp.index).index(dup_frame.index[dup]) + 1].append(
                        dup_frame.iloc[dup])
                else:
                    new_frame = new_frame.append(
                        [temp.iloc[list(temp.index).index(dup - 1):list(temp.index).index(dup)], dup_frame.iloc[dup]])
            new_frame = new_frame.append(temp.iloc[list(temp.index).index(dup_frame.index[dup]) + 1:])
        else:
            new_frame = frame.reindex(index=new_index)
        return SimDataFrame(new_frame, **frame.params_)

    if how not in ('outer', 'inner', 'left', 'right', 'cross'):
        raise ValueError("how must be 'outer', 'iner', 'left', 'right' or 'cross'")

    # if both indexes are equal
    if len(left.index) == len(right.index) and (left.index == right.index).all():
        return left, right

    # if are different, extract a Series according to the type of input
    else:
        if type(left) is SimDataFrame:
            i_left = left.to_pandas().iloc[:, 0]
        elif type(left) is SimSeries:
            i_left = left.to_pandas()
        elif type(left) is pd.DataFrame:
            i_left = left.iloc[:, 0]
        elif type(left) is pd.Series:
            i_left = left

        # checking right
        if type(right) is SimDataFrame:
            i_right = right.to_pandas().iloc[:, 0]
        elif type(right) is SimSeries:
            i_right = right.to_pandas()
        elif type(right) is pd.DataFrame:
            i_right = right.iloc[:, 0]
        elif type(right) is pd.Series:
            i_right = right

        # merge the indexes
        new_index = pd.merge(i_left, i_right, how=how, left_index=True, right_index=True).index
        # return original dataframes reindex to the merged index
        if bool(drop_duplicates):
            return left[~left.index.duplicated(keep)].reindex(index=new_index), right[
                ~right.index.duplicated(keep)].reindex(index=new_index)
            # return left.drop_duplicates().reindex(index=new_index), right.drop_duplicates().reindex(index=new_index)
        else:
            return merge_append(left, new_index), merge_append(right, new_index)


def merge_units(left, right=None, suffixes=('_x', '_y')):
    """
    return a dictionary with the units of both SimDataFrames merged, corresponding to the merged DataFrame.

    Parameters
    ----------
    left : SimDataFrame
    right : SimDataFrame
    suffixes : tuple of str, optional
        tuple indicating the suffixes to be used for repeated column names. The default is ('_x', '_y').

    Returns
    -------
    dict of units
    """
    if type(left) in (list, tuple) and len(left) > 1 and right is None:
        merged = left[0]
        for i in range(1, len(left)):
            merged = merge_units(merged, left[i])
        return merged

    merged = {}
    if type(left) in [SimDataFrame, SimSeries] and type(right) in [SimDataFrame, SimSeries]:
        for col in left.columns:
            if col in right.columns:
                merged[col + suffixes[0]] = left.get_units(col)[col]
            else:
                merged[col] = left.get_units(col)[col]
        for col in right.columns:
            if col in left.columns:
                merged[col + suffixes[1]] = right.get_units(col)[col]
            else:
                merged[col] = right.get_units(col)[col]

    elif type(left) in [SimDataFrame, SimSeries] and type(right) not in [SimDataFrame, SimSeries]:

        if isinstance(right, pd.DataFrame):
            columns = right.columns
        elif isinstance(right, pd.Series) and type(right.name) is str and len(right.name.strip()) > 0:
            columns = [right.name]
        else:
            columns = []

        for col in left.columns:
            if col in columns:
                merged[col + suffixes[0]] = left.get_units(col)[col]
            else:
                merged[col] = left.get_units(col)[col]
        for col in columns:
            if col in left.columns:
                merged[col + suffixes[1]] = 'UNDEFINED'
            else:
                merged[col] = 'UNDEFINED'

    elif type(left) not in [SimDataFrame, SimSeries] and type(right) in [SimDataFrame, SimSeries]:

        if isinstance(left, pd.DataFrame):
            columns = left.columns
        elif isinstance(left, pd.Series) and type(left.name) is str and len(left.name.strip()) > 0:
            columns = [left.name]
        else:
            columns = []

        for col in right.columns:
            if col in columns:
                merged[col + suffixes[0]] = right.get_units(col)[col]
            else:
                merged[col] = right.get_units(col)[col]
        for col in columns:
            if col in right.columns:
                merged[col + suffixes[1]] = 'UNDEFINED'
            else:
                merged[col] = 'UNDEFINED'

    else:
        raise TypeError("'left' and 'right' parameters most be SimDataFrame or SimSeries")

    return merged


def merge_SimParameters(left, right=None):
    """
    return a dictionary with the SimParameters of both SimDataFrames merged, corresponding to the merged DataFrame.

    Parameters
    ----------
    left : SimDataFrame
    right : SimDataFrame

    Returns
    -------
    dict of SimParameters
    """
    if type(left) in (list, tuple) and len(left) > 1 and right is None:
        merged = left[0]
        for i in range(1, len(left)):
            merged = merge_SimParameters(merged, left[i])
        return merged

    merged = {}
    if type(left) in [SimDataFrame, SimSeries] and type(right) in [SimDataFrame, SimSeries]:
        merged['verbose'] = bool(int(left.verbose) + int(right.verbose))
        if left.index.name == right.index.name:
            merged['index_name'] = left.index.name
        else:
            merged['index_name'] = (str(left.index.name) if left.index.name is not None else ''
                                                                                             +
                                                                                             str(right.index.name) if right.index.name is not None else '')
        if left.index_units == right.index_units:
            merged['index_units'] = left.index_units
        else:
            # what to do if index units are different? should convert index if possible...
            merged['index_units'] = left.index_units

        rename_separator_right = False
        rename_separator_left = False
        if left.name_separator == right.name_separator:
            merged['name_separator'] = left.name_separator
        else:
            if left.name_separator in ' '.join(list(left.columns)) and right.name_separator in ' '.join(
                    list(right.columns)):
                if left.name_separator not in ' '.join(list(right.columns)):
                    merged['name_separator'] = left.name_separator
                    # must rename right to use left nameSeparator
                    rename_separator_right = True
                elif right.name_separator not in ' '.join(list(left.columns)):
                    merged['name_separator'] = right.name_separator
                    # must rename right to use left nameSeparator
                    rename_separator_left = True
                else:
                    # should look for a new common name separator
                    merged['name_separator'] = left.name_separator + right.name_separator
                    rename_separator_left = True
                    rename_separator_right = True

        rename_intersection_right = False
        rename_intersection_left = False
        if left.intersection_character == right.intersection_character:
            merged['intersection_character'] = left.intersection_character
        else:
            if left.intersection_character in ' '.join(list(left.columns)) and right.intersection_character in ' '.join(
                    list(right.columns)):
                if left.intersection_character not in ' '.join(list(right.columns)):
                    merged['intersection_character'] = left.intersection_character
                    # must rename right to use left intersectionCharacter
                    rename_intersection_right = True
                elif right.intersection_character not in ' '.join(list(left.columns)):
                    merged['intersection_character'] = right.intersection_character
                    # must rename right to use left intersectionCharacter
                    rename_intersection_left = True
                else:
                    # should look for a new common name separator
                    merged['intersection_character'] = left.intersection_character + right.intersection_character
                    rename_intersection_left = True
                    rename_intersection_right = True

        merged['auto_append'] = bool(int(left._auto_append_) + int(right._auto_append_))

        merged['operate_per_name'] = left._operate_per_name_ if hasattr(left, '_operate_per_name_') else \
            left.operate_per_name if hasattr(left, 'operate_per_name') else False \
                                                                            + right._operate_per_name_ if hasattr(right,
                                                                                                                  '_operate_per_name_') else \
                right.operate_per_name if hasattr(right, 'operate_per_name') else False

        merged['transposed'] = (left._transposed_ if hasattr(left, '_transposed_') else
                                left.transposed if hasattr(left, 'transposed') else False,
                                left._transposed_ if hasattr(left, '_transposed_') else
                                left.transposed if hasattr(left, 'transposed') else False)
        if merged['transposed'][0] is not None and merged['transposed'][1] is not None:
            if merged['transposed'][0] != merged['transposed'][1]:
                logging.warning("concatenating one transposed SimDataFrame with one not-transposed SimDataFrame")
        merged['transposed'] = False
        merged['meta'] = {'left': left.meta if hasattr(left, 'meta') else False,
                          'right': right.meta if hasattr(right, 'meta') else False}
        merged['source'] = {'left': left.source_path if hasattr(left, 'source_path') else None,
                            'right': right.source_path if hasattr(right, 'source_path') else None}

    elif type(left) in [SimDataFrame, SimSeries] and type(right) not in [SimDataFrame, SimSeries]:
        merged = left.params_.copy()

    elif type(left) not in [SimDataFrame, SimSeries] and type(right) in [SimDataFrame, SimSeries]:
        merged = right.params_.copy()

    else:
        raise TypeError("'left' and 'right' parameters most be SimDataFrame or SimSeries")

    return merged


def merge(left, right, how='inner', on=None,
          left_on=None, right_on=None,
          left_index=False, right_index=False,
          sort=False, suffixes=('_x', '_y'),
          copy=True, indicator=False, validate=None):
    """
    Wrapper of Pandas merge, to merge also the units dictionary.
    Merge SimDataFrame, DataFrame or named SimSeries or Series objects with a database-style join.

    The join is done on columns or indexes. If joining columns on columns, the DataFrame indexes will be ignored. Otherwise if joining indexes on indexes or indexes on a column or columns, the index will be passed on. When performing a cross merge, no column specifications to merge on are allowed.

    Parameters
    ----------
    left : SimDataFrame or DataFrame or named SimSeries or Series
        Object to merge
    right : SimDataFrame or DataFrame or named SimSeries or Series
        Object to merge with.
    how : {‘left’, ‘right’, ‘outer’, ‘inner’, ‘cross’}, default ‘inner’
        Type of merge to be performed.
        · left: use only keys from left frame, similar to a SQL left outer join; preserve key order.
        · right: use only keys from right frame, similar to a SQL right outer join; preserve key order.
        · outer: use union of keys from both frames, similar to a SQL full outer join; sort keys lexicographically.
        · inner: use intersection of keys from both frames, similar to a SQL inner join; preserve the order of the left keys.
        · cross: creates the cartesian product from both frames, preserves the order of the left keys.
    on : label or list
        Column or index level names to join on. These must be found in both DataFrames.
        If on is None and not merging on indexes then this defaults to the intersection of the columns in both DataFrames.
    left_on : label or list, or array-like
        Column or index level names to join on in the left DataFrame. Can also be an array or list of arrays of the length of the left DataFrame. These arrays are treated as if they are columns.
    right_on : label or list, or array-like
        Column or index level names to join on in the right DataFrame. Can also be an array or list of arrays of the length of the right DataFrame. These arrays are treated as if they are columns.
    left_index : bool, default False
        Use the index from the left DataFrame as the join key(s). If it is a MultiIndex, the number of keys in the other DataFrame (either the index or a number of columns) must match the number of levels.
    right_index : bool, default False
        Use the index from the right DataFrame as the join key. Same caveats as left_index.
    sort : bool, default False
        Sort the join keys lexicographically in the result DataFrame. If False, the order of the join keys depends on the join type (how keyword).
    suffixes : list-like, default is (“_x”, “_y”)
        A length-2 sequence where each element is optionally a string indicating the suffix to add to overlapping column names in left and right respectively. Pass a value of None instead of a string to indicate that the column name from left or right should be left as-is, with no suffix. At least one of the values must not be None.
    copy : bool, default True
        If False, avoid copy if possible.
    indicator : bool or str, default False
        If True, adds a column to the output DataFrame called “_merge” with information on the source of each row. The column can be given a different name by providing a string argument. The column will have a Categorical type with the value of “left_only” for observations whose merge key only appears in the left DataFrame, “right_only” for observations whose merge key only appears in the right DataFrame, and “both” if the observation’s merge key is found in both DataFrames.
    validate : str, optional
        If specified, checks if merge is of specified type.
        · “one_to_one” or “1:1”: check if merge keys are unique in both left and right datasets.
        · “one_to_many” or “1:m”: check if merge keys are unique in left dataset.
        · “many_to_one” or “m:1”: check if merge keys are unique in right dataset.
        · “many_to_many” or “m:m”: allowed, but does not result in checks.

    Returns
    -------
    SimDataFrame
        A SimDataFrame of the two merged objects.
    """
    params = {}

    # checking right
    if type(right) is SimDataFrame:
        iright = right.DF
        params = right._SimParameters
    elif type(right) is SimSeries:
        iright = right.S
        params = right._SimParameters
    elif type(right) is pd.DataFrame:
        iright = right
    elif type(right) is pd.Series:
        iright = right

    # checking left
    if type(left) is SimDataFrame:
        ileft = left.DF
        if type(right) in [SimDataFrame, SimSeries]:
            params = merge_SimParameters(left, right)
        else:
            params = left._SimParameters
    elif type(left) is SimSeries:
        ileft = left.S
        params = left._SimParameters
    elif type(left) is pd.DataFrame:
        ileft = left
    elif type(left) is pd.Series:
        ileft = left

    mergeddata = pd.merge(ileft, iright, how=how, on=on, left_on=left_on, right_on=right_on, left_index=left_index,
                          right_index=right_index, sort=sort, suffixes=suffixes, copy=copy, indicator=indicator,
                          validate=validate)
    params['units'] = merge_units(left, right, suffixes=suffixes)
    return SimDataFrame(data=mergeddata, **params)
