import torch
import torch.nn as nn
import time


class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size,
                            hidden_size,
                            num_layers,
                            batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size) #.requires_grad_()
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size) #.requires_grad_()
        out, (hn, cn) = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

    
class TrainLSTM:
    def __init__(self, debug=False):
        self.model_type = 'lstm'
        self.model = None
        self.debug = debug
        self.input_size = 24
        self.hidden_size = 64
        self.num_layers = 2
        self.output_size = 15
        self.train_loss = []
        self.valid_loss = []
        self.num_epochs = 10
    
    def update_pramas(self, **kwargs):
        self.input_size = kwargs.get('input_size', self.input_size)
        self.hidden_size = kwargs.get('hidden_size', self.hidden_size)
        self.number_layers = kwargs.get('num_layers', self.num_layers)
        self.output_size = kwargs.get('output_size', self.output_size)
        self.num_epochs = kwargs.get('num_epochs', self.num_epochs)
        
    def train(self, train_dataloader, valid_dataloader):
        params = {
            'input_size': self.input_size,
            'hidden_size': self.hidden_size,
            'num_layers': self.num_layers,
            'output_size': self.output_size,
        }
        model = LSTMModel(**params)
        criterion = nn.MSELoss()
        optimizer = torch.optim.AdamW(model.parameters())
        self.train_loss = []
        self.valid_loss = []
        if self.debug:
            print('--------------------start training-------------------')
        for epoch in range(self.num_epochs):
            start_time = time.time()
            loss_0 = 0.0
            num_samples = 0.0
            for i, (inputs, labels) in enumerate(train_dataloader):
                model.train()
                optimizer.zero_grad()
                output = model(inputs)
                loss = criterion(output, labels.squeeze())
                loss.backward()
                optimizer.step()
                loss_0 += loss.item() * len(inputs)
                num_samples += len(inputs)
            self.train_loss.append(loss_0/num_samples)
            loss_1 = 0.0
            num_samples = 0.0
            for i, (inputs, labels) in enumerate(valid_dataloader):
                model.eval()
                output = model(inputs)
                loss = criterion(output, labels.squeeze())
                loss_1 += loss.item() * len(inputs)
                num_samples += len(inputs)
            self.valid_loss.append(loss_1/num_samples)
            if self.debug:
                end_time = time.time()
                total_seconds = end_time - start_time
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                t = f"{hours}h {minutes}m"
                print('epoch:'+str(epoch)\
                      +' spend time:'+t\
                      +' training loss(mse): ' + str(loss_0/num_samples)\
                      +' validation loss(mse): ' + str(loss_1/num_samples)
                    )
        if self.debug:
            print('--------------end train-------------')
        self.model = model
    
    def get_train_loss(self):
        return self.train_loss, self.valid_loss
    
    def save_model(self, model_path, model = None):
        self.model = model or self.model
        torch.save(self.model.state_dict(), model_path)
        self.model.save(model_path)
        return model_path