#!/usr/bin/python

import urllib.request
import re

# Current count of profiles @ Demagog site
POLITICIAN_COUNT=432

politician={}

# Get data from Demagog.cz site
for i in range(1, POLITICIAN_COUNT+1):
    # remove non-politician profiles (Demagog team etc.)
    if i in (17, 28, 29):
        continue

    for line in urllib.request.urlopen('http://demagog.cz/politici/'+str(i)+'/').readlines():
        w = line.strip().decode('utf-8')
        politician_name = re.match(r"<title>Demagog.cz &mdash; (.*)</title>", w)
        if politician_name:
            name = politician_name.group(1)
        elif 'politicianStats' in w:
            stats = re.match(r".*numberIs(\d*).*numberIs(\d*).*numberIs(\d*).*numberIs(\d*).*", w)
            if stats:
                politician[name] = {'truth': stats.group(1), 'lie': stats.group(2), 'misleading': stats.group(3), 'nonverifiable': stats.group(4)}
                all_statements_count = int(stats.group(1)) + int(stats.group(2)) + int(stats.group(3)) + int(stats.group(4))
                politician[name]['lie_rate'] = 0.0 if all_statements_count == 0 else float(stats.group(2))/all_statements_count



# Print all politicians sorted by most lie_statement/all_statements ratio
lie_rates={}
for name, stats in politician.items():
    lie_rates[name] = stats['lie_rate']
for name in sorted(lie_rates, key=lie_rates.get, reverse=True):
    print("{0};{1}".format(name, lie_rates[name]))




## print all politician stats
#for name, stats in politician.items():
#    print("{0};{1};{2};{3};{4};{5}".format(name, stats['truth'], stats['lie'], stats['misleading'], stats['nonverifiable'], stats['lie_rate']))
