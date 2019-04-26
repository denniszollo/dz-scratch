import pandas as pd
import matplotlib.pyplot as plt
import sys

dates = ['pc_time', 'pc_time_dt', 'piksi_time']
df = pd.read_csv(sys.argv[1],parse_dates=dates)
cols =  df.columns
print(cols)
fig = plt.figure(figsize=[20,15])
for i, each in enumerate(cols):
    print each
    if i == 0:
        break
        continue
    plt.subplot(4,1,i)
    plt.plot(df['index'], df[each])
    plt.ylabel(each)
fig.savefig(sys.argv[1] + 'time_plot.png')


PERCENTILES = [0.01, 0.05, 0.25, 0.5, 0.68, 0.95, 0.99]                                                       

fig2= plt.figure(figsize=[20,15])
ax1 = plt.subplot(3, 1, 1)
plt.plot(df['index'], df['time_diff'], marker='x')
labels = [item.get_text() for item in ax1.get_xticklabels()]
ax2 = plt.subplot(3, 1, 2)
df['time_diff'].hist(ax=ax2)
plt.xlabel("{0}".format('time_diff'))
plt.ylabel("Number")
plt.subplot(3,1,3)
plt.figtext(0.25,0.1, "Statistics\n " + str(df['time_diff'].describe(percentiles=PERCENTILES)))

fig2.savefig(sys.argv[1] + "diff_plot.png")
