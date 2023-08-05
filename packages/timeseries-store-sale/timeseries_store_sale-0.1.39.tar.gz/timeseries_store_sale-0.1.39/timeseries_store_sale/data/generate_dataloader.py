import torch
from torch.utils.data import Dataset, ConcatDataset, DataLoader
import pandas as pd
from .preprocessing import PreprocessData


class TimeSeriesDataset(Dataset):
    def __init__(self,
                 df,
                 date_column,
                 input_steps,
                 output_steps,
                 start_date=None,
                 end_date=None,
                 normalize=False,
                 mean=None,
                 std=None):
        self.data = df
        self.date_column = date_column
        self.input_steps = input_steps
        self.output_steps = output_steps
        self.start_date = start_date
        self.end_date = end_date
        self.normalize = normalize
        self.mean = mean
        self.std = std

        # Filter data by date range
        if start_date is not None and end_date is not None:
            self.data = self.data[(self.data[self.date_column] >= start_date) & (self.data[self.date_column] <= end_date)]

        # Compute max index for input/output sequences
        self.max_input_index = len(self.data) - input_steps - output_steps

        # drop the date column
        self.data = self.data.drop(columns = [self.date_column])

    def get_mean_std(self):
        return self.mean, self.std

    def __len__(self):
        return self.max_input_index

    def num_features(self):
        return self.data.shape[1]

    def __getitem__(self, idx):
        # Get input and output sequences
        input_seq = self.data.iloc[idx:idx+self.input_steps, :].values.astype('float32')
        output_seq = self.data.iloc[idx+self.input_steps:idx+self.input_steps+self.output_steps, -1:].values.astype('float32')

        # Convert sequences to PyTorch tensors
        input_seq = torch.from_numpy(input_seq)  # Add batch dimension
        output_seq = torch.from_numpy(output_seq)  # Add batch dimension

        return input_seq, output_seq
    

class TimeSeriesDataLoader:
    def __init__(self):
        self.data_loader = {}
        self.n_in = 30
        self.n_out = 15
        self.batch_size = 128
        self.ds_arr = []
        self.ds = None
        self.subsize = 100
        self.data_loader = None
        self.store_arr = None
        self.family_arr = None
        self.data_path = None
    
    def update_param(self, **kwargs):
        self.n_in = kwargs.get('n_in', self.n_in)
        self.n_out = kwargs.get('n_out', self.n_out)
        self.subsize = kwargs.get('subsize', self.subsize)
        self.store_arr = kwargs.get('store_arr', self.store_arr)
        self.family_arr = kwargs.get('family_arr', self.family_arr)
        self.data_path = kwargs.get('data_path', self.data_path)
    
    def prepare_data(self):
        o = PreprocessData()
        self.row_data = o.prepare_dataframe(self.data_path or o.data_path)
        if self.store_arr is None:
            self.store_arr = o.store_arr
        if self.family_arr is None:
            self.family_arr = o.family_arr
    
    def get_datasets(self, start_date, end_data):
        o = PreprocessData()
        self.row_data = o.prepare_dataframe(self.data_path)
        self.ds_arr = []
        self.ds = None
        for i in self.store_arr:
            for j in self.family_arr:
                print('store: '+str(i)+' and family: '+str(j))
                ds = TimeSeriesDataset(
                    o.time_sequence_data(i, j, self.row_data),
                    o.index_column, 
                    self.n_in, 
                    self.n_out,
                    start_date, 
                    end_data
                )
                self.ds_arr.append(ds)
        self.ds = ConcatDataset(self.ds_arr)
    
    def get_data_loader(self, shuffle=False):
        self.data_loader = DataLoader(self.ds, self.batch_size, shuffle)
        return self.data_loader
        
        
