import torch
import torch.nn as nn
import torch.optim as optim
import os

# Fake data, CHECK!
x_train = torch.randn(100, 10, dtype=torch.float) # generate 100 inputs, each with 10 features
y_train = torch.randint(0,2,(100,1), dtype=torch.float) # generate 100 labels, either 0 or 1

x_val = torch.randn(20, 10, dtype=torch.float) # generate 20 inputs, each with 10 features
y_val = torch.randint(0,2,(20,1), dtype=torch.float) # generate 20 labels, either 0 or 1

x_test = torch.randn(20, 10, dtype=torch.float) # generate 20 inputs, each with 10 features

class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):  # constructor
        super(MLP, self).__init__()

        # nn.Linear(input_dim, output_dim)
        self.fcl1 = nn.Linear(input_dim, hidden_dim ) # "fully connected layer 1"
        
        # activation function: ReLU (Rectified Linear Unit) to introduce non-linearity
        # without this, we're just building a big linear regression model
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.3)

        self.fcl2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = self.fcl1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fcl2(x)
        return x
    
def train(epochs=500):
    print()
    print("--- Instantiate Model ---")
    features = 10
    hidden = 64
    out = 2
    best_loss = float('inf')

    model = MLP(input_dim=features, hidden_dim=hidden, output_dim=out)

    print()
    print("--- Optimizer and Loss Function ---")

    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    print()
    print("--- Training Loop ---")
    for epoch in range(epochs):
        model = train_one_epoch(model, criterion, optimizer)
        loss = eval(model, criterion, epoch)

        if loss < best_loss:
            best_loss = loss

            print("New best model found! Loss: ", loss, " Saving...")
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': loss,
            }, "model.pth")

def train_one_epoch(model, criterion, optimizer):
        #training mode
        model.train()

        #forward pass
        pred = model(x_train)

        #loss
        loss = criterion(pred, y_train)

        #backward pass
        loss.backward()

        #update weights
        optimizer.step()

        #zero gradients
        optimizer.zero_grad()

        return model
       
def eval(model, criterion, epoch):
    #evaluation mode
    model.eval()

    with torch.no_grad():
        pred = model(x_val)
        loss = criterion(pred, y_val)

    return loss

def main():
    train(500)
    # print(model.state_dict())
    # torch.save(model, "model.pth")

if __name__ == "__main__":
    main()