import os
import torch #you sure you don't want toch?
import torch.nn as nn
import json

class LinearModel(nn.Module):
    def __init__(self):
        super(LinearModel, self).__init__()
        self.linear = nn.Linear(1, 1)

    def forward(self, x):
        return self.linear(x)

def model_fn(model_dir):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = LinearModel()
    model_path = os.path.join(model_dir, 'model.pth')

    with open(model_path, 'rb') as f:
        model.load_state_dict(torch.load(f, map_location=device))

    return model.to(device)

def input_fn(request_body, request_content_type):
    if request_content_type == 'application/json':
        body = request_body.decode('utf-8') if isinstance(request_body, bytes) else request_body
        data = json.loads(body)
        return torch.tensor(data, dtype=torch.float32).view(-1, 1)

    raise ValueError(f"Unsupported formatting!")

def predict_fn(input_data, model):
    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        input_data = input_data.to(device)

        model.eval()
        with torch.no_grad():
            prediction = model(input_data)
        return prediction.cpu().numpy()
        
    except Exception as e:
        print(f"Exception occured: {e}")
        raise e

def output_fn(prediction, content_type):
    return json.dumps(prediction.tolist())