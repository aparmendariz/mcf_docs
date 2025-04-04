"""
Provide functions for Black-Box allocations.

Created on Thu Aug  3 15:23:17 2023
# -*- coding: utf-8 -*-
@author: MLechner
"""
from itertools import combinations
from math import inf
import random

from numba import njit
import numpy as np
import ray

from mcf import mcf_general as mcf_gp
from mcf import mcf_print_stats_functions as ps
from mcf import optpolicy_pt_add_functions as opt_pt_add


def optimal_tree_eff_proc(optp_, data_df, seed=12345):
    """Build optimal policy tree."""
    gen_dic, pt_dic, int_dic = optp_.gen_dict, optp_.pt_dict, optp_.int_dict
    ot_dic = optp_.other_dict
    if gen_dic['with_output']:
        print('\nBuilding optimal policy / decision tree')
    (data_x, data_ps, data_ps_diff, name_x, type_x, values_x, values_comp_all
     ) = prepare_data_for_tree_building_eff(optp_, data_df, seed=seed)
    # All values_x are already sorted before this step
    optimal_tree, x_trees = None, []
    if int_dic['parallel_processing']:
        if not ray.is_initialized():
            ray.init(num_cpus=int_dic['mp_parallel'], include_dashboard=False)
        data_x_ref = ray.put(data_x)
        data_ps_ref = ray.put(data_ps)
        data_ps_diff_ref = ray.put(data_ps_diff)
        still_running = [ray_tree_search_eff_multip_single.remote(
            data_ps_ref, data_ps_diff_ref, data_x_ref, name_x, type_x,
            values_x, values_comp_all, gen_dic, pt_dic, ot_dic,
            pt_dic['depth'], m_i, int_dic['with_numba'], m_i**3)
            for m_i in range(len(type_x))]
        idx, x_trees = 0, [None] * len(type_x)
        while len(still_running) > 0:
            finished, still_running = ray.wait(still_running)
            finished_res = ray.get(finished)
            for ret_all_i in finished_res:
                if gen_dic['with_output']:
                    mcf_gp.share_completed(idx+1, len(type_x))
                x_trees[idx] = ret_all_i
                idx += 1
        optimal_reward = np.empty(len(type_x))
        for idx, tree in enumerate(x_trees):
            optimal_reward[idx] = tree[1]
        max_i = np.argmax(optimal_reward)
        optimal_reward = optimal_reward[max_i]
        optimal_tree, obs_total = x_trees[max_i][0], x_trees[max_i][2]
    else:
        (optimal_tree, optimal_reward, obs_total, values_comp_all
         ) = tree_search_eff(
            data_ps, data_ps_diff, data_x, name_x, type_x, values_x,
            values_comp_all, pt_dic, gen_dic, ot_dic, pt_dic['depth'],
            with_numba=int_dic['with_numba'], seed=seed)
    return optimal_tree, optimal_reward, obs_total


def tree_search_eff(data_ps, data_ps_diff, data_x, name_x, type_x, values_x,
                    values_comp_all, pt_dic, gen_dic, ot_dic, treedepth,
                    no_further_splits=False, with_numba=True, seed=12345):
    """Build tree EFF.

    Parameters
    ----------
    data_ps : Numpy array. Policy scores.
    data_ps_diff : Numpy array. Policy scores as differences.
    data_x : Numpy array. Policy variables.
    ind_sort_x : Numpy array. Sorted Indices with respect to cols. of x
    ind_leaf: Numpy array. Remaining data in leaf.
    name_x : List of strings. Name of policy variables.
    type_x : List of strings. Type of policy variable.
    values_x : List of sets. Values of x in initial dara.
    pt_dic, gen_dic : Dict's. Parameters.
    treedepth : Int. Current depth of tree.
    no_further_splits : Boolean.
        Further splits do not matter. Take next (1st) split as final. Default
        is False.

    Returns
    -------
    tree : List of lists. Current tree.
    reward : Float. Total reward that comes from this tree.
    no_by_treat : List of int. Number of treated by treatment state (0-...)
    values_comp_all : list of lists. Values and combinations - unordered vars.

    """
    if treedepth == 1:  # Evaluate tree
        tree, reward, no_by_treat = opt_pt_add.evaluate_leaf(
            data_ps, gen_dic, ot_dic, pt_dic, with_numba=with_numba)
    else:
        if not no_further_splits and (treedepth < pt_dic['depth']):
            no_further_splits = opt_pt_add.only_1st_tree_fct3(
                data_ps, pt_dic['cost_of_treat_restrict'])
        min_leaf_size = pt_dic['min_leaf_size'] * 2**(treedepth - 2)
        no_of_x, reward = len(type_x), -inf
        tree = no_by_treat = None
        for m_i in range(no_of_x):
            if gen_dic['with_output']:
                if treedepth == pt_dic['depth']:
                    txt = (f'{name_x[m_i]:20s}  {m_i / no_of_x * 100:4.1f}%'
                           ' of variables completed')
                    ps.print_mcf(gen_dic, txt, summary=False)
            values_x_to_check, values_comp_all[m_i] = get_val_to_check_eff(
                type_x[m_i], values_x[m_i][:], values_comp_all[m_i],
                data_x[:, m_i], data_ps_diff, pt_dic['no_of_evalupoints'],
                select_values_cat=pt_dic['select_values_cat'],
                eva_cat_mult=pt_dic['eva_cat_mult'], with_numba=with_numba,
                seed=seed)
            for val_x in values_x_to_check:
                if type_x[m_i] == 'unord':
                    left = np.isin(data_x[:, m_i], val_x)
                else:
                    left = data_x[:, m_i] <= (val_x + 1e-15)
                obs_left = np.count_nonzero(left)
                if not (min_leaf_size <= obs_left
                        <= (len(left) - min_leaf_size)):
                    continue
                right = np.invert(left)
                (tree_l, reward_l, no_by_treat_l, values_comp_all
                 ) = tree_search_eff(
                    data_ps[left, :], data_ps_diff[left, :], data_x[left, :],
                    name_x, type_x, values_x, values_comp_all, pt_dic, gen_dic,
                    ot_dic, treedepth-1, no_further_splits,
                    with_numba=with_numba, seed=seed+1)
                (tree_r, reward_r, no_by_treat_r, values_comp_all
                 ) = tree_search_eff(
                    data_ps[right, :], data_ps_diff[right, :],
                    data_x[right, :], name_x, type_x, values_x,
                    values_comp_all, pt_dic, gen_dic, ot_dic, treedepth-1,
                    no_further_splits, with_numba=with_numba, seed=seed+1)
                if ot_dic['restricted'] and pt_dic['enforce_restriction']:
                    reward_l, reward_r = opt_pt_add.adjust_reward(
                        no_by_treat_l, no_by_treat_r, reward_l, reward_r,
                        with_numba, ot_dic['max_by_treat'])
                if reward_l + reward_r > reward:
                    reward = reward_l + reward_r
                    no_by_treat = no_by_treat_l + no_by_treat_r
                    tree = merge_trees_eff(tree_l, tree_r, name_x[m_i],
                                           type_x[m_i], val_x, treedepth)
                if no_further_splits:
                    return tree, reward, no_by_treat, values_comp_all
    return tree, reward, no_by_treat, values_comp_all


def merge_trees_eff(tree_l, tree_r, name_x_m, type_x_m, val_x, treedepth):
    """Merge trees and add new split (optimized version-limited gain).

    0: Node identifier (INT: 0-...)
    1: Parent knot
    2: Child node left
    3: Child node right
    4: Type of node (1: Terminal node, no further splits
                    0: previous node that lead already to further splits)
    5: String: Name of variable used for decision of next split
    6: x_type of variable (policy categorisation, maybe different from MCF)
    7: If x_type = 'unordered': Set of values that goes to left daughter
    7: If x_type = 0: Cut-off value (larger goes to right daughter)
    8: List of Treatment state for both daughters [left, right]

    Parameters
    ----------
    tree_l : List of lists. Left tree.
    tree_r : List of lists. Right tree.
    name_x_m : String. Name of variables used for splitting.
    type_x_m : String. Type of variables used for splitting.
    val_x : Float, Int, or set of Int. Values used for splitting.
    treedepth : Int. Current level of tree. 1: final level.

    Returns
    -------
    new_tree : List of lists. The merged trees.

    """
    leaf = [None] * 9
    leaf[0], leaf[1] = random.randrange(100000), None
    leaf[5], leaf[6], leaf[7] = name_x_m, type_x_m, val_x

    if treedepth == 2:  # Final split (defines 2 final leaves)
        leaf[2], leaf[3], leaf[4] = None, None, 1
        leaf[8] = [tree_l, tree_r]  # For 1st tree --> treatment states
        new_tree = [leaf]
    else:
        leaf[2], leaf[3], leaf[4] = tree_l[0][0], tree_r[0][0], 0
        tree_l[0][1], tree_r[0][1] = leaf[0], leaf[0]
        new_tree = [None] * (1 + 2 * len(tree_l))
        new_tree[0] = leaf
        tree = tree_l[:]
        tree.extend(tree_r[:])
        new_tree[1:] = tree
    return new_tree


@ray.remote
def ray_tree_search_eff_multip_single(
        data_ps, data_ps_diff, data_x, name_x, type_x, values_x,
        values_comp_all, gen_dic, pt_dic, ot_dic, treedepth, m_i,
        with_numba=True, seed=123456):
    """Prepare function for Ray."""
    return tree_search_eff_multip_single(
        data_ps, data_ps_diff, data_x, name_x, type_x, values_x,
        values_comp_all, gen_dic, pt_dic, ot_dic, treedepth, m_i,
        with_numba=with_numba, seed=seed)


def tree_search_eff_multip_single(
        data_ps, data_ps_diff, data_x, name_x, type_x, values_x,
        values_comp_all, gen_dic, pt_dic, ot_dic, treedepth, m_i,
        with_numba=True, seed=12345):
    """Build tree. Only first level. For multiprocessing only.

    Parameters
    ----------
    data_ps : Numpy array. Policy scores.
    data_ps_diff : Numpy array. Policy scores relative to reference category.
    data_x : Numpy array. Policy variables.
    ind_sort_x : Numpy array. Sorted Indices with respect to cols. of x
    ind_leaf: Numpy array. Remaining data in leaf.
    name_x : List of strings. Name of policy variables.
    type_x : List of strings. Type of policy variable.
    values_x : List of sets. Values of x for non-continuous variables.
    pt_dic : Dict. Parameters.
    gen_dic : Dict. Parameters.
    treedepth : Int. Current depth of tree.
    seed: Int. Seed for combinatorical.

    Returns
    -------
    tree : List of lists. Current tree.
    reward : Float. Total reward that comes from this tree.
    no_by_treat : List of int. Number of treated by treatment state (0-...)

    """
    assert treedepth != 1, 'This should not happen in Multiprocessing.'
    reward, tree, no_by_treat = -inf, None, None

    values_x_to_check, values_comp_all[m_i] = get_val_to_check_eff(
        type_x[m_i], values_x[m_i][:], values_comp_all[m_i], data_x[:, m_i],
        data_ps_diff, pt_dic['no_of_evalupoints'],
        select_values_cat=pt_dic['select_values_cat'],
        eva_cat_mult=pt_dic['eva_cat_mult'], with_numba=with_numba, seed=seed)

    for val_x in values_x_to_check:
        if type_x[m_i] == 'unord':
            left = np.isin(data_x[:, m_i], val_x)
        else:
            left = data_x[:, m_i] <= (val_x + 1e-15)
        obs_left = np.count_nonzero(left)
        if not (pt_dic['min_leaf_size'] <= obs_left
                <= (len(left)-pt_dic['min_leaf_size'])):
            continue
        right = np.invert(left)
        tree_l, reward_l, no_by_treat_l, values_comp_all = tree_search_eff(
            data_ps[left, :], data_ps_diff[left, :], data_x[left, :],
            name_x, type_x, values_x, values_comp_all, pt_dic, gen_dic, ot_dic,
            treedepth - 1, with_numba=with_numba, seed=seed+1)
        tree_r, reward_r, no_by_treat_r, values_comp_all = tree_search_eff(
            data_ps[right, :], data_ps_diff[right, :], data_x[right, :],
            name_x, type_x, values_x, values_comp_all, pt_dic, gen_dic, ot_dic,
            treedepth - 1, with_numba=with_numba, seed=seed+1)
        if ot_dic['restricted'] and pt_dic['enforce_restriction']:
            reward_l, reward_r = opt_pt_add.adjust_reward(
                no_by_treat_l, no_by_treat_r, reward_l, reward_r,
                with_numba, ot_dic['max_by_treat'])
        if reward_l + reward_r > reward:
            reward = reward_l + reward_r
            no_by_treat = no_by_treat_l + no_by_treat_r
            tree = merge_trees_eff(tree_l, tree_r, name_x[m_i],
                                   type_x[m_i], val_x, treedepth)
    return tree, reward, no_by_treat


def get_val_to_check_eff(type_x_m_i, values_x_m_i, values_comp_all_m_i,
                         data_x_m_i, data_ps_diff, no_of_evalupoints,
                         select_values_cat=False, eva_cat_mult=1,
                         with_numba=True, seed=1234):
    """Get the values to check for next splits of leaf."""
    if type_x_m_i in ('cont', 'disc'):
        values_x_to_check = get_values_cont_ord_x_eff(data_x_m_i, values_x_m_i)
    elif type_x_m_i == 'unord':
        # Take the pre-computed values of the splitting points that fall into
        # the range of the data
        values_x_to_check, values_comp_all_m_i = combinations_categorical_eff(
            data_x_m_i, data_ps_diff, values_comp_all_m_i, no_of_evalupoints,
            select_values=select_values_cat, factor=eva_cat_mult,
            with_numba=with_numba, seed=seed)
    else:
        raise ValueError('Wrong data type')
    return values_x_to_check, values_comp_all_m_i


def combinations_categorical_eff(single_x_np, ps_np_diff, values_comp_all,
                                 no_of_evalupoints, select_values=False,
                                 factor=1, with_numba=True, seed=123456):
    """Create all possible combinations of list elements, w/o complements."""
    values = np.unique(single_x_np)
    no_of_values = len(values)
    no_eva_point = int(no_of_evalupoints * factor)
    if values_comp_all is not None:
        for hist in values_comp_all:
            if len(hist[0]) == len(values) and np.all(hist[0] == values):
                return hist[1], values_comp_all  # No need to compute new

    if with_numba:
        no_of_combinations = total_sample_splits_categorical_eff(no_of_values)
    else:
        no_of_combinations = opt_pt_add.total_sample_splits_categorical(
            no_of_values)
    if no_of_combinations < no_eva_point:
        combinations_new = all_combinations_no_complements_eff(values)
    else:
        if select_values:
            no_of_evalupoints_new = round(find_evapoints_cat(
                len(values), no_eva_point, with_numba=with_numba))
            # * 1.1 to be more conservative
            rng = np.random.default_rng(seed=seed)
            indx = rng.choice(range(len(values)), size=no_of_evalupoints_new,
                              replace=False)
            values_rnd = values[indx]
            combinations_new = all_combinations_no_complements_eff(values_rnd)
        else:
            # Sort values according to policy score differences
            values_sorted, no_of_ps = opt_pt_add.get_values_ordered(
                single_x_np, ps_np_diff, values, no_of_values,
                with_numba=with_numba)
            combinations_t = sorted_values_into_combinations_eff(
                values_sorted, no_of_ps, no_of_values)
            combinations_ = drop_complements_eff(combinations_t, values,
                                                 sublist=False)
            len_c = len(combinations_)
            if len_c > no_eva_point:
                rng = np.random.default_rng(seed=seed)
                indx = rng.choice(range(len_c), size=no_eva_point,
                                  replace=False).tolist()
                combinations_new = [combinations_[i] for i in indx]
            elif len_c < no_eva_point:
                # Fill with some random combinations previously omitted.
                # This case can happen because of the ordering used above.
                combinations_new = add_combis(combinations_, values_sorted,
                                              no_eva_point)
            else:
                combinations_new = combinations_
    if values_comp_all is None:
        values_comp_all = []
    values_comp_all.append((values, combinations_new))
    return combinations_new, values_comp_all


def add_combis(combinations_, values_sorted, no_values_to_add):
    """Add combinations."""
    if no_values_to_add > len(values_sorted)/2:
        no_values_to_add = int(len(values_sorted)/2)
    values = values_sorted[:no_values_to_add]
    combinations_add = [tuple(vals) for vals in values]
    combinations_.extend(combinations_add)
    return combinations_


def find_evapoints_cat(no_values, no_of_evalupoints, with_numba=True):
    """Find number of categories that find to no_of_evaluation points."""
    if no_values < 6:
        return no_values
    for vals in range(6, no_values):
        if with_numba:
            no_of_combinations = total_sample_splits_categorical_eff(vals)
        else:
            no_of_combinations = opt_pt_add.total_sample_splits_categorical(
                vals)
        if no_of_combinations > no_of_evalupoints:
            no_values = vals
            break
    return no_values


@njit
def total_sample_splits_categorical_eff(no_of_values):
    """
    Compute total number of sample splits that can generated by categoricals.

    Parameters
    ----------
    no_of_values : Int.

    Returns
    -------
    no_of_splits: Int.

    """
    no_of_splits = 0
    for i in range(1, no_of_values):
        no_of_splits += (np_factorial(no_of_values)
                         / (np_factorial(no_of_values-i) * np_factorial(i)))
    no_of_splits_ret = no_of_splits / 2
    return no_of_splits_ret  # no complements


@njit
def np_factorial(val):
    """Compute factorial with Numpy function."""
    if val == 0:
        return 1
    # Result too large for int
    return np.prod(np.arange(1, val + 1, dtype=np.float64))


def all_combinations_no_complements_eff(values):
    """Create all possible combinations of list elements, removing complements.

    Parameters
    ----------
    values : List. Elements to be combined.

    Returns
    -------
    list_without_complements : List of tuples.

    """
    # This returns a list with tuples of all possible combinations of tuples
    list_all = [combinations(values, length) for length
                in range(1, len(values))]
    # Next, the complements to each list will be removed
    list_wo_compl = drop_complements_eff(list_all, values)
    return list_wo_compl


def drop_complements_eff(list_all, values, sublist=True):
    """
    Identify and remove complements.

    Parameters
    ----------
    list_all : List of tuples. Tuples with combinations.
    values : List. All relevant values.

    Returns
    -------
    list_wo_compl : List of Tuples. List_all with complements removed.

    """
    list_w_compl, list_wo_compl = [], []
    if sublist:
        for sub1 in list_all:
            for i_i in sub1:
                i = tuple(i_i)
                if i not in list_w_compl:
                    list_wo_compl.append(i)
                    compl_of_i = [x for x in values if x not in i]
                    list_w_compl.append(tuple(compl_of_i))
    else:
        for i in list_all:
            if i not in list_w_compl:
                list_wo_compl.append(i)
                compl_of_i = [x for x in values if x not in i]
                list_w_compl.append(tuple(compl_of_i))
    return list_wo_compl


def sorted_values_into_combinations_eff(values_sorted, no_of_ps, no_of_values):
    """
    Transfrom sorted values into unique combinations of values.

    Parameters
    ----------
    values_sorted : 2D numpy array. Sorted values for each policy score
    no_of_ps : Int. Number of policy scores.
    no_of_values : Int. Number of values.

    Returns
    -------
    unique_combinations : Unique Tuples to be used for sample splitting.

    """
    # value_idx = np.arange(no_of_values-1)
    # unique_combinations = {
    #     tuple(values_sorted[value_idx[:i+1], j])
    #     for j in range(no_of_ps)
    #     for i in value_idx
    #     }
    # Chat-GPT 3.5 optimized version
    unique_combinations = set()

    for j in range(no_of_ps):
        for i in range(no_of_values - 1):
            unique_combinations.add(tuple(values_sorted[:i + 1, j]))

    return list(unique_combinations)


def prepare_data_for_tree_building_eff(optp_, data_df, seed=123456):
    """Prepare data for tree building."""
    x_type, x_values = optp_.var_x_type, optp_.var_x_values
    # x_values is numpy array
    data_ps = data_df[optp_.var_dict['polscore_name']].to_numpy()
    data_ps_diff = data_ps[:, 1:] - data_ps[:, 0, np.newaxis]
    no_of_x = len(x_type)
    name_x = [None] * no_of_x
    type_x, values_x = [None] * no_of_x, [None] * no_of_x
    values_comp_all = [None] * no_of_x
    for j, key in enumerate(x_type.keys()):
        name_x[j], type_x[j] = key, x_type[key]
        vals = np.array(x_values[key])  # Values are sorted - all vars
        if type_x[j] == 'cont':
            obs = len(vals)
            start = obs / optp_.pt_dict['no_of_evalupoints'] / 2
            stop = obs - 1 - start
            indi = np.linspace(start, stop,
                               num=optp_.pt_dict['no_of_evalupoints'],
                               dtype=np.int64)
            values_x[j] = vals[indi]
        else:
            values_x[j] = vals.copy()
    data_x = data_df[name_x].to_numpy()
    del data_df
    if optp_.gen_dict['x_unord_flag']:
        for m_i in range(no_of_x):
            if type_x[m_i] == 'unord':
                data_x[:, m_i] = np.round(data_x[:, m_i])
                (values_x[m_i], values_comp_all[m_i]
                 ) = combinations_categorical_eff(
                    data_x[:, m_i], data_ps_diff, None,
                    optp_.pt_dict['no_of_evalupoints'],
                    select_values=optp_.pt_dict['select_values_cat'],
                    factor=optp_.pt_dict['eva_cat_mult'],
                    with_numba=optp_.int_dict['with_numba'], seed=seed)
    return (data_x, data_ps, data_ps_diff, name_x, type_x, values_x,
            values_comp_all)


def get_values_cont_ord_x_eff(data_vector, x_values):
    """Get cut-off points for tree splitting for single continuous variables.

    Parameters
    ----------
    data_vector : Numpy-1D array. Sorted vector
    x_values : Numpy array. Potential cut-off points.

    Returns
    -------
    Numpy 1D-array. Sorted cut-off-points

    """
    if len(data_vector) < len(x_values) / 2:
        return np.unique(data_vector)

    min_x = np.min(data_vector)
    max_x = np.max(data_vector)

    split_values = (x_values >= min_x) & (x_values < max_x)

    no_vals = np.sum(split_values)
    if no_vals < 2:
        return [min_x + (max_x - min_x) / 2]

    if len(data_vector) < no_vals / 2:
        return np.unique(data_vector)

    return x_values[split_values]
