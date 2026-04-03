import torch 
import torch.nn as nn
import torch.optim as optim

from torch.utils.tensorboard import SummaryWriter

class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(10, 5)
        self.fc2 = nn.Linear(5, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.fc1(x)
        x = torch.relu(x)
        x = self.fc2(x)
        return self.sigmoid(x)
    

def main():
    # The SummaryWriter class is used to write data to TensorBoard
    writer = SummaryWriter(log_dir='runs/metrics')
    model = SimpleModel()

    dummy_data = torch.randn(1, 10, dtype=torch.float)
    writer.add_graph(model, dummy_data)

    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    x_train = torch.randn(100, 10, dtype=torch.float)
    y_train = torch.randn(100, 1, dtype=torch.float)

    x_test = torch.randn(20, 10, dtype=torch.float)
    y_test = torch.randn(20, 1, dtype=torch.float)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print("running on: ", device)
    x_train = x_train.to(device)
    y_train = y_train.to(device)
    x_test = x_test.to(device)
    y_test = y_test.to(device)

    epochs = 10000

    print("--- Training ---")
    for epoch in range(epochs):
        # set the model to train
        model.train()
        # forward pass
        preds = model(x_train)
        # zero the optimizer
        optimizer.zero_grad()
        # calculate the loss
        loss = criterion(preds, y_train)
        # backward pass
        loss.backward()
        # update the weights
        optimizer.step()

        # eval the epoch of training
        model.eval()
        with torch.no_grad():
            preds = model(x_test)
            loss = criterion(preds, y_test)
            writer.add_scalar("Loss/test", loss.item(), epoch)

        # Log the loss and epoch to show how the model is learning
        writer.add_scalar("Loss/train", loss.item(), epoch)

        if epoch % 100 == 0:
            print(f"Epoch: {epoch} Loss: {loss.item()}")
    
if __name__ == "__main__":
    main()

# Don't forget to install tensorboard: pip install tensorboard
# Run tensorboard with: tensorboard --logdir=runs
# Run the training and watch the metrics be plotted!