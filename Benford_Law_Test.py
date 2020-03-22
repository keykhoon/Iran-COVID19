import numpy as np 
import pandas as pd
import seaborn as sns
import scipy as sc
import matplotlib.pyplot as plt

#print descriptive stats and plot histogram 
def show_dist(df, col):
    print('Descriptive stats for {}'.format(col),'≥ 10')
    print('-'*(len(col)+22))
    print(df[col].describe())
    bins = np.arange(df[col].min(), df[col].max() + 1,(df[col].max() + 1-df[col].min())/60)
    sns.distplot(df[col],kde=False,bins=bins,color='navy')
    plt.title('Confirmed COVID19 cases ≥ 10 in Iran provinces', fontsize=16)
    plt.xlabel('Cases', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.xticks(np.arange(0, 350, 50))
    plt.savefig('Iran_Ostani_Hist.png', dpi=300,bbox_inches='tight',pad_inches=0.1)
    
#combining all numerical columns (daily province reported cases) into one column
def combine_all_columns(df,start_col,end_col):
    col_num=start_col
    temp_list=[]
    for key, value in df.iteritems():
        if col_num>start_col and col_num<end_col:
            temp_list.append(value.tolist())
        col_num += 1
    flattened=[]
    for sublist in temp_list:
        for val in sublist:
            flattened.append(val)
    return flattened

# Find the first digit 
def FindFirstDigit(n) :    
    if n>9:
        # Find total number of digits - 1 
        digits = int(np.log10(n)) 
        # Find first digit 
        n = int(n / np.power(10, digits))  
    else:
        n=n
    # Return first digit 
    return n

#read the csv file into pandas df
df=pd.read_csv('Iran-Ostani.csv')
#combining all numerical columns (daily province reported cases) into one column
all_data_df = pd.DataFrame(combine_all_columns(df,1,33))
#rename column label
all_data_df.rename(columns={0:"Cases"},inplace=True)

#remove all values <10
all_data_df[all_data_df<10]=np.nan
all_data_df.dropna(inplace=True)
show_dist (all_data_df,'Cases')
sample_count=len(all_data_df.index)
print ('Number of reports that reported confirmed cases ≥ 10 is ',sample_count)

#calculate Benford expected count for each digit category
digits=list(range(1,10,1))
Benford_expected_digit_count=list(map(lambda x:np.log10((1+x)/x)*sample_count,digits))

#create a list of the first digits of the reported cases ≥ 10
first_digits_list=list(map(lambda x:FindFirstDigit(x),all_data_df['Cases']))
actual_digit_count=[]
for digit in range(1,10):
    actual_digit_count.append(sum(1 for x in first_digits_list if x==digit))

#create a df from actual and expected counts of the first digit categories
df_digit_counts = pd.DataFrame(list(zip(str(digits),Benford_expected_digit_count, actual_digit_count)),columns =['Digit','Expected', 'Actual'])

#plot expected and actual counts of the first digit categories
ax = df_digit_counts.plot(kind='bar',rot=0)
ax.set_xticklabels(digits)
ax.set_xlabel('First Digit')
ax.set_ylabel('Frequency')
ax.figure.savefig('Iran_Ostani_FirstDigit.png', dpi=300,bbox_inches='tight',pad_inches=0.1)

#calculate Chi-square stat and p-value
p_value_chi_test=sc.stats.chisquare (actual_digit_count,Benford_expected_digit_count)
print (p_value_chi_test)
