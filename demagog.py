#!/usr/bin/python

import argparse
import urllib.request
import re

# Current count of profiles @ Demagog site
POLITICIAN_COUNT=20
#TODO find out the actual number dynamically

# global structure containing parsed information about politician
politician={}

# default order for sorting (from biggest value to lowest)
descending_order=True

# print politicians with more than minimum_statement_count statements
minimum_statement_count = None


# Get data from Demagog.cz site
def get_data():
    for i in range(1, POLITICIAN_COUNT+1):
        # remove non-politician profiles (Demagog team etc.)
        if i in (17, 28, 29, 204):
            continue

        name = None # because I don't like the Python way of variable scoping
        for line in urllib.request.urlopen('http://demagog.cz/politici/'+str(i)+'/').readlines():
            w = line.strip().decode('utf-8')
            politician_name = re.match(r"<title>Demagog.cz &mdash; (.*)</title>", w)
            # parse politician name
            if politician_name:
                name = re.sub(' +', ' ', politician_name.group(1))  # remove multiple spaces
                party = ''

            # parse stats about politician
            elif name and 'politicianStats' in w:
                stats = re.match(r".*numberIs(\d*).*numberIs(\d*).*numberIs(\d*).*numberIs(\d*).*", w)
                if stats:
                    politician[name] = {'truth': stats.group(1), 'lie': stats.group(2), 'misleading': stats.group(3), 'nonverifiable': stats.group(4)}
                    all_statements_count = int(stats.group(1)) + int(stats.group(2)) + int(stats.group(3)) + int(stats.group(4))
                    politician[name]['party'] = party   # we already have this data

                    # remove politician from stats if he does not have a minimum count of statements
                    if (minimum_statement_count and all_statements_count < minimum_statement_count):
                        politician.pop(name)
                        continue

                    politician[name]['truth_rate'] = 0.0 if all_statements_count == 0 else float(stats.group(1))/all_statements_count
                    politician[name]['lie_rate'] = 0.0 if all_statements_count == 0 else float(stats.group(2))/all_statements_count
                    politician[name]['misleading_rate'] = 0.0 if all_statements_count == 0 else float(stats.group(3))/all_statements_count
                    politician[name]['nonverifiable_rate'] = 0.0 if all_statements_count == 0 else float(stats.group(4))/all_statements_count

            # parse politician party (if exists)
            elif name and name in re.sub(' +', ' ', w) and re.match(r".*\((.*)\)", w):
                party_name = re.match(r".*\((.*)\)$", w)
                if party_name:
                    party = party_name.group(1)


# Print all politician stats
def all_stats():
    print('jméno,strana,pravda,nepravda,zavádějící,neověřitelné,míra nepravdivosti')   # hlavička pro CSV
    for name, stats in sorted(politician.items()):  # we do not use sort ordering here
        print("{0},{1},{2},{3},{4},{5},{6}".format(name, stats['party'], stats['truth'], stats['lie'], stats['misleading'], stats['nonverifiable'], stats['lie_rate']))


# Template method for calculating of truth/lie/misleading/nonverifiable rate
def most_rate(rate_name):
    assert(rate_name in ('truth_rate', 'lie_rate', 'misleading_rate', 'nonverifiable_rate'))
    name_rate = {'truth_rate': 'míra pravdivosti',
                 'lie_rate': 'míra nepravdivosti',
                 'misleading_rate': 'míra zavádějícnosti',
                 'nonverifiable_rate': 'míra neověřitelnosti'}
    rates={}
    parties={}
    for name, stats in politician.items():
        rates[name] = stats[rate_name]
        parties[name] = stats['party']
    print('jméno,strana,{0}'.format(name_rate[rate_name])) # hlavička pro CSV
    for name in sorted(rates, key=rates.get, reverse=descending_order):
        print("{0},{1},{2}".format(name, parties[name], rates[name]))


# Print all politicians sorted by most lie_statements/all_statements ratio
def most_lying():
    most_rate('lie_rate')


# Print all politicians sorted by most true_statements/all_statements ratio
def most_truth():
    most_rate('truth_rate')


# Print all politicians sorted by most misleading_statements/all_statements ratio
def most_misleading():
    most_rate('misleading_rate')


# Print all politicians sorted by most nonverifiable_statements/all_statements ratio
def most_nonverifiable():
    most_rate('nonverifiable_rate')



if __name__ == "__main__":
    # define map of parameters binded to specific functions
    # note that '-' character is translated to '_' by argparse, so we need to keep that in mind when getting the correct key
    function_map = {'all': [all_stats, 'Print list of all stats (unsorted)'],
                    'most-lying': [most_lying,'Print list of politicians sorted by most lie_statements/all_statements ratio'],
                    'most-truth': [most_truth, 'Print list of politicians sorted by most truth_statemets/all_statements ratio'],
                    'most-misleading': [most_misleading, 'Print list of politicians sorted by most misleading_statemets/all_statements ratio'],
                    'most-nonverifiable': [most_nonverifiable, 'Print list of politicians sorted by most nonverifiable_statemets/all_statements ratio'],
                    }

    #parse command line argument fist
    parser = argparse.ArgumentParser(description='Get data from Demagog.cz website and process them')
    group = parser.add_mutually_exclusive_group()
    for key, value in function_map.items():
        group.add_argument('--'+key, help=value[1], action='store_true')
    # sorting order
    order_group = parser.add_mutually_exclusive_group()
    order_group.add_argument('--ascending', '-a', help='Results are sorted in ascending order', action='store_true')
    order_group.add_argument('--descending', help='Results are sorted in descending order (default behavior)', action='store_true')
    # minimum desired statement count
    parser.add_argument('--min-statement-count', '-m', help='Minimum statement count needed for including into stats')
    args = parser.parse_args()

    # set sorting order of result
    if (args.ascending):
        descending_order = False

    # set minimum statement count
    if (args.min_statement_count):
        minimum_statement_count = int(args.min_statement_count)

    # download and parse data from demagog.cz
    get_data()

    # call appropriate function according to parameters
    # use only those which have appropriate function in function_map
    # do not forget we need to replace '_' to '-' to search correct method in function map (argparse modifies it)
    myargs = [k.replace("_", "-") for (k, v) in vars(args).items() if v and k.replace('_', '-') in function_map]
    assert(len(myargs) <= 1)    # max one choice is allowed
    if (len(myargs) is 0):  # default behavior with no arguments provided
        function_map['all'][0]()
    else:
        function_map[myargs[0]][0]()

