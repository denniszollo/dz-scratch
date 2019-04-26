import pandas as pd
import matplotlib.pyplot as plt
fig = plt.figure(figsize=[20,10])
df = pd.read_csv('out.csv')
plt.subplot(3,1,1)
plt.plot(df["tow (ms)"], df["tow (ms)"].diff())
plt.ylabel(['tow period (milliseconds)'])
ax = plt.subplot(3,1,2)
df["tow (ms)"].diff().hist(ax=ax)
fig.savefig('tow_diff.png')

