# 1 "/Users/dzollo/source/dz-scratch/python-plotting/plot_error_mode.py"
# 1 "<built-in>" 1
# 1 "<built-in>" 3
# 340 "<built-in>" 3
# 1 "<command line>" 1
# 1 "<built-in>" 2
# 1 "/Users/dzollo/source/dz-scratch/python-plotting/plot_error_mode.py" 2
import sys
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv(sys.argv[1])
print df.columns
subdf = df[[u'tow', u'n', u'e', 'd', 'flags']]
print subdf.describe()
m1 = subdf[subdf['flags'] == 1]
m2 = subdf[subdf['flags'] == 2]
m3 = subdf[subdf['flags'] == 3]
m4 = subdf[subdf['flags'] == 4]

dfs = [m1, m2, m3, m4]
labels = ["spp", "dgps", 'float', 'fixed']
colors = ["rx", "cx", "bx", "gx"]

plt.figure(figsize=[20,8])
plt.subplot(2,1,1)
for i,each in enumerate(dfs): 
  plt.plot(each[u'tow'], each[u'n'], colors[i])
  plt.plot(each[u'tow'], each[u'e'], colors[i])
plt.subplot(2,1,2)
for i,each in enumerate(dfs): 
  plt.plot(each[u'tow'], each[u'd'], colors[i])
plt.show()

