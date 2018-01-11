import pandas as pd
from datetime import datetime
import os
OOT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_data_file(path= OOT_DIR + "/../data/orders.csv"):
    return pd.read_csv(path,sep=",",header=0)


def max_num_items(dataset):
    # Max number of items in one order: if a customer has more than one order, take the one with more items
    dataset_max_num_items = dataset.groupby(['customer_id','order_id'])['num_items'].max()
    dataset = dataset.join(dataset_max_num_items, ['customer_id','order_id'], rsuffix="_sum")
    return dataset

def max_revenue(dataset):
    # Max revenue in one order: if a customer has more than one order, take the one with largest revenue
    dataset_max_revenue = dataset.groupby(['customer_id','order_id'])['revenue'].max()
    dataset=dataset.join(dataset_max_revenue,['customer_id','order_id'], rsuffix="_max")
    return dataset

def total_revenue(dataset):
    # Total revenue of a customer: including all orders
    total_revenue_each_costumer = dataset.groupby('customer_id')['revenue'].sum()
    dataset = dataset.join(total_revenue_each_costumer,['customer_id'],rsuffix='_total')
    return dataset


def total_orders(dataset):
    # Total number of orders
    frequency_order_each_costumer = dataset.groupby(['customer_id'])['order_id'].count()
    dataset = dataset.join(frequency_order_each_costumer, ['customer_id'],rsuffix="_total")
    return dataset

def day_since_last_order(dataset):
    # Days since last order: number of days from the last order until 2017-10-17
    def get_gap_data(data):     
        gap_date = abs(datetime.strptime("2017-10-17", '%Y-%m-%d') - datetime.strptime(data, '%Y-%m-%d'))
        data=gap_date.days
        return data

    longest_date_each_costumer = dataset.groupby(['customer_id'])['created_at_date'].max()
    longest_date_each_costumer = longest_date_each_costumer.apply(get_gap_data)
    dataset  = dataset.join(longest_date_each_costumer, ['customer_id'],rsuffix="_day")
    dataset.rename(columns={'created_at_date_day':'day_since_last_order'}, inplace=True)
    return dataset

def two_consecutive_order(dataset):
    # The longest interal between two consecutive orders(in unit of days). 
    def get_date_interval(data):
        return data.days 

    def calculate_single_order(dataset):
        avg_long_day = dataset['gap_days'].mean()
        idx = dataset['gap_days'] == 0
        dataset.loc[idx,'gap_days'] = avg_long_day + dataset.loc[idx,'day_since_last_order'] 
        return dataset

    longest_date_interval = dataset.groupby(['customer_id']).agg({'created_at_date':['min','max']})
    longest_date_interval['min'] = pd.to_datetime(longest_date_interval['created_at_date']['min'])
    longest_date_interval['max'] = pd.to_datetime(longest_date_interval['created_at_date']['max'])
    longest_date_interval['gap_days'] = longest_date_interval['max'] - longest_date_interval['min']
    longest_date_interval['gap_days'] = longest_date_interval['gap_days'].apply(get_date_interval)
    longest_date_interval.drop(['created_at_date','min','max'],axis=1,inplace=True)
    longest_date_interval = longest_date_interval.reset_index()
    longest_date_interval.columns = longest_date_interval.columns.remove_unused_levels().droplevel(level=1)
    longest_date_interval = longest_date_interval.set_index('customer_id')
    dataset = dataset.join(longest_date_interval,['customer_id'])
    dataset = calculate_single_order(dataset)
    return dataset

#if __name__ == '__main__':
#    main_process()
