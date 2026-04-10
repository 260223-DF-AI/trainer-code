import os
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
import shutil

class LinearModel(nn.Module):
    def __init__(self):
        super(LinearModel, self).__init__()
        self.linear = nn.Linear(1, 1)

    def forward(self, x):
        return self.linear(x)

def train():
    # accept the hyperparameters as args?
    parser = argparse.ArgumentParser()

    #hyperparameters
    parser.add_argument('--epochs', type=int, default=1)
    parser.add_argument('--learning_rate', type=float, default=0.005) 

    #SageMaker specific args
    parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR', './model'))

    args, _ = parser.parse_known_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"running on {device}")

    # set up the training objects like we always do!
    model = LinearModel().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=args.learning_rate)

    print("Prepping the training data...")
    # y = 356.732 x + 145.8126
    # bigX = list(range(100))
    # eq = lambda z: 356.732*z + 145.8126
    # y = [eq(x) for x in bigX]

    x = torch.randn(100, 1).to(device)
    y = torch.tensor(356.732 * x + 145.8126).to(device)
    
    print("Start the training loop...")

    model.train()
    for i in range(args.epochs):
        optimizer.zero_grad()
        pred = model(x)
        loss = criterion(pred, y)
        loss.backward()
        optimizer.step()

    # SageMaker expects the model to be at SM_MODEL_DIR
    model_path = os.path.join(args.model_dir, 'model.pth')
    print(f"Saving model to: {model_path}")

    torch.save(model.state_dict(), model_path)

    code_dir = os.path.join(args.model_dir, 'code')
    os.makedirs(code_dir, exist_ok=True)

    if os.path.exists('inference.py'):
        shutil.copy('inference.py', os.path.join(code_dir, 'inference.py'))
    
if __name__=='__main__':
    train()