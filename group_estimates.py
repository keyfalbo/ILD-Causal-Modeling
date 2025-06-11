import pandas as pd
import os
import sys
from semopy import Model
import semopy as sem

#Input Directory
input_dir = r"Sample-Data"

# Read saved group graph and convert to lavaan format
path = (os.path.join(input_dir, "group_cpdag.txt"))
with open(path) as f:
    f.readline()
    f.readline()
    nodes = [node for node in f.readline()[:-1].split(';')]
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    edges = {node: [] for node in nodes}
    edge = f.readline()
    while edge != '\n':
        edge = edge[:-1].split()
        if edge[2] == '-->': edges[edge[3]].append(edge[1]) 
        if edge[2] == '<--': edges[edge[1]].append(edge[3]) 
        edge = f.readline()

model = ''
for node in nodes:
    if len(edges[node]):
        model += node + ' ~ ' + ' + '.join(edges[node]) + '\n'

# Read the appropriate csv file
df = pd.read_csv(os.path.join(input_dir, "group_data.csv"))

# Calculate estimates
model2 = Model(model)
model2.fit(df)
estimates = model2.inspect()
estimates.to_csv(os.path.join(input_dir, 'group_estimates.csv'), index=False, header=True)

# Calculate model fit statistics
stats = sem.calc_stats(model2)
stats.to_csv(os.path.join(input_dir, "group_fitstats.csv"), index=False, header=True)
