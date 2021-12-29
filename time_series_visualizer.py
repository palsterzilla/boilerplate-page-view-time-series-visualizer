import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'],index_col='date')

# Clean data
df = df[
  (df['value'] >= df['value'].quantile(0.025)) &
  (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(df.index, df['value'], 'r', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    '''
    df_bar = df.copy()
    df['month'] = df.index.month
    df['year'] = df.index.year
    df_bar = df.groupby(['year', 'month'])['value'].mean()
    df_bar = df_bar.unstack()
    '''
    df_clean = df.copy()
    df_clean = df_clean.reset_index()
    df_clean['month'] = df_clean["date"].apply(lambda x: x.month_name())
    df_clean['month_num'] = df_clean["date"].apply(lambda x: x.month)
    df_clean['year'] = df_clean["date"].apply(lambda x: x.year)
    
    df_clean = df_clean.sort_values(by = ["year","month_num"])
    df_group = df_clean.groupby(['month','month_num','year', ]).value.agg(['mean'])
    data = df_group.reset_index().sort_values(by='month_num')
    
    sns.set_theme(style="white", context="talk")

    fig, ax = plt.subplots(figsize=(35, 15))

    sns.barplot(
        x='year', 
        y='mean',
        hue = 'month',
        data=data,
        ax = ax,
    )

    sns.despine(ax=ax, left=True)
    ax.set_ylabel("Average Page Views")
    ax.set_xlabel("Years")
    l = ax.legend(loc='upper left')
    l.set_title('Months')

    df_bar = data 
    '''
    # Draw bar plot
    fig = df_bar.plot.bar(legend=True, figsize=(8,7), xlabel="Years", ylabel="Average #Page Views").figure   
    plt.legend(['January', 'February', 'March', 'April', 'May', 'June', 'July', #'August', 'September', 'October', 'November', 'December'], title='Months')

    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    '''
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_clean = df.copy()
    df_clean = df_clean.reset_index()
    df_clean['month'] = df_clean["date"].apply(lambda x: x.month_name()[0:3])
    df_clean['month_num'] = df_clean["date"].apply(lambda x: x.month)
    df_clean['year'] = df_clean["date"].apply(lambda x: x.year)

    # Draw box plots (using Seaborn)
    df_group = df_clean.groupby(['year']).apply(lambda x: x)
    bx1 = df_group

    df_group = df_clean.groupby(['month']).apply(lambda x: x)
    bx2 = df_group.sort_values(by='month_num')
    sns.set_theme(style="white", context="talk", font_scale=2.80)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(80, 50))

    sns.boxplot(
        x='year', 
        y='value',
        data=bx1,
        ax = ax1,
    )

    sns.boxplot(
        x='month', 
        y='value',
        data=bx2,
        ax = ax2,
    )

    sns.despine(ax=ax1)
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_ylabel("Page Views")
    ax1.set_xlabel("Year")

    sns.despine(ax=ax2)
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_ylabel("Page Views")
    ax2.set_xlabel("Month")

    df_box = df_clean.copy()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
