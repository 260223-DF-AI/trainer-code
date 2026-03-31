import numpy as np
import torch # pytorch - the library of ML tools that we'll need!
import torch.nn as nn # the standard neural network modules (linear, conv2d) - and the loss function!
import torch.optim as optim # the standard optimizers (SGD, Adam, etc.)


x = torch.tensor([[1],[2],[3],[4],[5]]).float()
y = torch.tensor([[40],[60],[80],[100],[120]]).float()
# y = wx+b
# w = 20, b = 20



def tensor_ops():
    print()
    print("-- Numpy Array --")
    # NumPy array
    np_array = np.array([[1, 2],[3, 4],[5,6]]) # rows of data
    print(np_array)

    print()
    print("-- PyTorch Tensor --")
    # convert to pytorch tensor
    tensor = torch.from_numpy(np_array)
    tensor = tensor.float() # convention is to set tensors to floats for the sake of precision

    print(tensor)
    print({'type': tensor.dtype, 'shape': tensor.shape})
    # the shape [3,2] is 3 rows, 2 columns

    print()
    print("-- PyTorch Tensor Operations --")

    tensor_a = torch.tensor([1, 2, 3, 4, 5, 6, 7, 8])
    tensor_b = torch.tensor([9, 10, 11, 12, 13, 14, 15, 16])

    summed_tensor = tensor_a + tensor_b
    print({'summed_tensor': summed_tensor})

    dot_prod = torch.dot(tensor_a, tensor_b)
    print({'dot_prod': dot_prod})

    #cross_prod = torch.linalg.cross(tensor_a, tensor_b,dim=0)
    #print({'cross_prod': cross_prod})

    print()
    print("-- PyTorch Tensor Hardware --")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # check if GPU is available
    print(device)

    tensor_gpu = tensor_a.to(device) # move tensor to GPU
    print(tensor_gpu.device)

    # when you move tensors to the GPU - all operations are done on the GPU.
    # SO MOVE ALL THE TENSORS! - if you don't move everything, the non-GPU tensors will cuase issues wih calculations.

    print()
    print("-- PyTorch Tensor Autograd --")

    # the gradient let's the model "learn"

    x = torch.tensor([2.0], requires_grad=True)
    w = torch.tensor([3.0], requires_grad=True)
    b = torch.tensor([1.0], requires_grad=True)

    # forward pass
    y = w * x + b
    print(y)
    # backward pass - computes the gradient
    # tells pytorch to look at y, and calculate how much of w, x, b contributed to that result
    y.backward()

    print({'wgrad: ':w.grad.item()})
    print({'xgrad: ':x.grad.item()})
    print({'bgrad: ':b.grad.item()})

class LinearRegressionModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(LinearRegressionModel, self).__init__()

        # nn.Linear represents a fully connected layer (y = wx+b) 
        # puthorch will initialize the weights and bias
        self.linear = nn.Linear(input_dim, output_dim)

    def forward(self, x):
        # we do need to define how the inormation will flow through the NN,
        # when you call model(x), it will call the forward function
        return self.linear(x)

def train_model():
    print("-- Intialize Linear Regression Model --")

    input_dim = 1
    output_dim = 1

    model = LinearRegressionModel(input_dim, output_dim)

    print({'intial parameters': model.parameters()})
    print({'initial weights:' : model.linear.weight.item()})
    print({'initial bias:' : model.linear.bias.item()})

    print()
    print("-- Loss Function --")
    criterion = nn.MSELoss() # mean squared error
    
    print()
    print("-- Optimizer --")
    optimizer = optim.Adam(model.parameters(), lr=2.5)

    print()
    print("-- Epochs --")
    epochs = 100

    print("-- Training Loop --")

    for epoch in range(epochs):
        model.train() # Step 0 - tell the model to be ready to learn!
        prediction = model(x) # Step 1 - forward pass, and collect the prediction
        loss = criterion(prediction, y) # Step 2 - calculate the loss based on the predcition and the expected result
        optimizer.zero_grad() # Step 3 - zero the gradients
        loss.backward() # Step 4 - calculate the gradients
        optimizer.step() # Step 5 - update the weights

   #     if epoch % 10 == 0:
        print({'epoch': epoch + 1, 'loss': loss.item()})
        
    print()
    print("-- Finished Training --")
    print("-- Model Parameters --")
    print({'final weights:' : model.linear.weight.item()})
    print({'final bias:' : model.linear.bias.item()})


    print()
    print("-- Testing --")
    model.eval() # exitn the learning mode 
    test_input = torch.tensor([[6]]).float() # create a test input
    with torch.no_grad():
        prediction = model(test_input) # run the model
        print({'prediction': prediction.item()})

if __name__ == "__main__":
    #tensor_ops()
    train_model()