import torch
import torch.nn as nn
import torch.optim as optim
import os
import pandas as pd
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LinearRegressionModel(nn.Module):
    def __init__(self, input_dim):
        super(LinearRegressionModel, self).__init__()
        self.linear = nn.Linear(input_dim, 1)

    def forward(self, x):
        return self.linear(x)
    
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, default=1)
    parser.add_argument('--learning_rate', type=float, default=0.005) 
    parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR', '/opt/ml/model'))
    parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAIN', '/opt/ml/input/data/train'))

    return parser.parse_known_args()[0]

def main():
    args = parse_args()

    try:
        train_file = os.path.join(args.train, 'train.csv')
        df = pd.read_csv(train_file)

        X = df.iloc[:, :-1].values
        y = df.iloc[:, -1].values

        X_tensor = torch.tensor(X, dtype=torch.float32)
        y_tensor = torch.tensor(y, dtype=torch.float32).view(-1,1)
    
    except Exception as e:
        logger.error(e)

# instantiate the model
    input_dim = X_tensor.shape[1]
    model = LinearRegressionModel(input_dim)

    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=args.learning_rate)


    model.train()

    for epoch in range(args.epochs):
        optimizer.zero_grad()
        y_pred = model(X_tensor)
        loss = criterion(y_pred, y_tensor)
        loss.backward()
        optimizer.step()

    # save the model
    os.makedirs(args.model_dir, exist_ok=True)
    model_path =  os.path.join(args.model_dir, 'model.pth')
    torch.save(model.state_dict(), model_path)

if __name__ == '__main__':
    main()