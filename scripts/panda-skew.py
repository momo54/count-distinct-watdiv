import pandas as pd
import seaborn as sns

df_s = pd.read_csv('subject_freq.txt')
print(df_s.head())

print(f"skew on S:{df_s.skew()}")

df_p = pd.read_csv('predicat_freq.txt')
print(df_p.head())

print(f"skew on P:{df_p.skew()}")

df_o = pd.read_csv('object_freq.txt')
print(df_o.head())

print(f"skew on O:{df_o.skew()}")



import matplotlib.pyplot as plt


fig, axs = plt.subplots(3, 2)  # 2 rows, 2 columns

sns.kdeplot(df_s,ax=axs[0,0], color='blue', fill=True)
sns.kdeplot(df_p,ax=axs[1,0], color='red', fill=True)
sns.kdeplot(df_o,ax=axs[2,0], color='green', fill=True)

axs[0,1].hist(df_s, bins=10, alpha=0.75, color='blue')
axs[0,1].set_title('Histogram of DF_S')
axs[0,1].set_xlabel('Value')
axs[0,1].set_ylabel('Frequency')
axs[0,1].set_yscale('log')


axs[1,1].hist(df_p, bins=10, alpha=0.75, color='blue')
axs[1,1].set_title('Histogram of DF_p')
axs[1,1].set_xlabel('Value')
axs[1,1].set_ylabel('Frequency')
axs[1,1].set_yscale('log')

axs[2,1].hist(df_o, bins=10, alpha=0.75, color='blue')
axs[2,1].set_title('Histogram of DF_O')
axs[2,1].set_xlabel('Value')
axs[2,1].set_ylabel('Frequency')
axs[2,1].set_yscale('log')

plt.tight_layout()

plt.show()
