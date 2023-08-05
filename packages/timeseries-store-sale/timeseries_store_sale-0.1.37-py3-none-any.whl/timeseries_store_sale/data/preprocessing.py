import pandas as pd
import numpy as np


class PreprocessData:
    def __init__(self):
        self.row_data = {}
        self.index_column = 'date'
        self.target_label = 'sales'
        self.family_dict = None
        self.store_arr = []
        self.family_arr = []
        self.localte_dict = {}
        self.state_dict = {}
        self.store_city_map = {}
        self.store_state_map = {}
        self.store_cluster = {}
        self.store_type_dict = {}
        self.type_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
        self.raw_df = {}
        self.data_path = {
            'main': './train.csv',
            'oil': './oil.csv',
            'holiday': './holidays_events.csv',
            'transaction': './transactions.csv',
            'store': './stores.csv'
        }
    
    def update_param(self, **kwargs):
        self.index_column = kwargs.get('index_column', self.index_column)
        self.target_label = kwargs.get('target_label', self.target_label)
        self.data_path = kwargs.get('data_path', self.data_path)
    
    def load_data(self, data_path=None, index_column=None):
        if index_column is None:
            df = pd.read_csv(data_path)
        else:
            df = pd.read_csv(data_path, parse_dates=[index_column], index_col=index_column)
        return df
    
    def get_unique_dict(self, df, unique_column):
        dict_ = {v:k for k, v in enumerate(df[unique_column].unique())}
        return dict_
    
    def prepare_dataframe(self, data_path=None):
        if data_path:
            self.update_param(data_path=data_path)
        df = self.load_data(self.data_path['main'])
        self.family_dict = self.get_unique_dict(df, 'family')
        df['family'] = df['family'].apply(lambda x: self.family_dict[x])
        self.store_arr = df['store_nbr'].unique()
        self.family_arr = df['family'].unique()
        self.raw_df['main'] = df
        df = self.load_data(self.data_path['oil'], self.index_column)
        self.raw_df['oil'] = df
        df = self.load_data(self.data_path['holiday'], self.index_column)
        self.raw_df['holiday'] = df
        arr_1 = df.locale_name.unique()
        df = self.load_data(self.data_path['transaction'], self.index_column)
        self.raw_df['transaction'] = df
        df = self.load_data(self.data_path['store'])
        self.raw_df['store'] = df
        arr_2 = df.city.unique()
        cities_arr = np.concatenate((arr_1, arr_2), axis=0)
        self.localte_dict = {v: k for k, v in enumerate(list(set(cities_arr)))}
        self.localte_dict[np.nan] = -1
        self.store_city_map = df.set_index('store_nbr')['city'].to_dict()
        self.store_state_map = df.set_index('store_nbr')['state'].to_dict()
        self.state_dict = self.get_unique_dict(df, 'state')
        self.store_type_dict = df.set_index('store_nbr')['type'].to_dict()
        self.store_cluster = df.set_index('store_nbr')['cluster'].to_dict()
        return self.raw_df

    
    def get_time_features(self, df):
        df['DAY'] = df[self.index_column].dt.day
        df['MONTH'] = df[self.index_column].dt.month
        df['YEAR'] = df[self.index_column].dt.year
        df['WEEK'] = df[self.index_column].dt.dayofweek
        df['WYEAR'] = df[self.index_column].dt.weekofyear
        return df
    
    def set_column_order(self, df, target_label):
        column_order = [col for col in df.columns if col != target_label] + [target_label]
        df = df.reindex(columns=column_order)
        return df
    
    def time_sequence_data(self, store_id=None, family_id=None, raw_df={}):
        data = raw_df['main']
        df = data[(data['store_nbr'] == store_id) & (data['family'] == family_id)]
        df[self.index_column] = pd.to_datetime(df[self.index_column])
        df = self.get_time_features(df)
        df.set_index(self.index_column, inplace=True)
        # add transcatioin information
        df_t = raw_df['transaction']
        df['transactions'] = df_t[df_t['store_nbr'] == store_id]['transactions']
        df.fillna(0)
        # add oil price information
        df_oil = raw_df['oil']
        df = df.merge(df_oil['dcoilwtico'], left_on=self.index_column, right_on=self.index_column, how='left')
        df = df.fillna(0)
        # add dummies of type of holiday
        df_h = raw_df['holiday']
        df_h_type = pd.get_dummies(df_h.type)
        df = df.merge(df_h_type, left_on=self.index_column, right_on=self.index_column, how='left')
        # add dummies of type of holiday
        df_h_locale = pd.get_dummies(df_h.locale)
        df = df.merge(df_h_locale, left_on=self.index_column, right_on=self.index_column, how='left')
        df = df.fillna(0.0)
        # add locale_name and transferred
        df = df.merge(df_h[['locale_name', 'transferred']], left_on=self.index_column, right_on=self.index_column, how='left')
        df['transferred'] = df['transferred'].apply(lambda x: 1 if x == True else 0)
        df['locale_name'] = df['locale_name'].apply(lambda x: self.localte_dict[x])
        # add the city
        df['city'] = df['store_nbr'].apply(lambda x: self.store_city_map[x])
        df['city'] = df['city'].apply(lambda x: self.localte_dict[x])
        df['state'] = df['store_nbr'].apply(lambda x: self.store_state_map[x])
        df['state'] = df['state'].apply(lambda x: self.state_dict[x])
        df['type'] = df['store_nbr'].apply(lambda x: self.type_dict[self.store_type_dict[x]])
        df['cluster'] = df['store_nbr'].apply(lambda x: self.store_cluster[x])
        # drop id columns and set column order
        df.drop(columns=['id'], inplace=True)
        df[self.index_column] = df.index
        self.df = self.set_column_order(df, self.target_label)
        return self.df




        