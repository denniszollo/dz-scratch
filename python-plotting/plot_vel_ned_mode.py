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
subdf = df[[u'GPS TOW [s]', u'Vert Vel [m/s]', u'SOG [m/s]', u'Pos Mode', 'SVs Used']]
print subdf.describe()
m1 = subdf[subdf['Pos Mode'] == 1]
m2 = subdf[subdf['Pos Mode'] == 2]
m3 = subdf[subdf['Pos Mode'] == 3]
m4 = subdf[subdf['Pos Mode'] == 4]

dfs = [m1, m2, m3, m4]
labels = ["spp", "dgps", 'float', 'fixed']
colors = ["rx", "cx", "bx", "gx"]

plt.figure(figsize=[20,8])
plt.subplot(2,1,1)
for i,each in enumerate(dfs): 
  plt.plot(each[u'GPS TOW [s]'], each[u'SOG [m/s]'], colors[i])
plt.ylabel("SOG(m/s)")
plt.legend(labels)  
plt.subplot(2,1,2)
for i,each in enumerate(dfs): 
  plt.plot(each[u'GPS TOW [s]'], each[u'Vert Vel [m/s]'], colors[i])
plt.ylabel("vertical velocity")
plt.show()

