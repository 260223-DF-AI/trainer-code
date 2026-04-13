import os
import shutil
import sagemaker
import tarfile
import torch
import torch.nn as nn
import torch.optim as optim
from sagemaker.pytorch import PyTorch, PyTorchModel
from sagemaker.serializers import JSONSerializer
from sagemaker.deserializers import JSONDeserializer
from src.LinMod import LinearModel


# Credentials!!!
# Train the model

USE_GPU = False

TRAIN_DEVICE = 'ml.g4dn.xlarge' if USE_GPU else 'ml.m5.large'
DEPLOY_DEVICE = 'ml.m5.large'

print(f"Training on {TRAIN_DEVICE}")
print(f"Deploying on {DEPLOY_DEVICE}")

LOCAL_MODEL_DIR = 'local_model'
TAR_NAME = 'model.tar.gz'

EPOCHS = 10
LEARNING_RATE = 0.0005

## DON'T LEAVE YOUR CREDS IN YOUR CODE
ARN = "arn:aws:iam::407975137156:role/2371-SM-Execution-Test" 

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"running on {device}")

# set up the training objects like we always do!
model = LinearModel().to(device)
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=LEARNING_RATE)

print("Prepping the training data...")
# y = 356.732 x + 145.8126
# bigX = list(range(100))
# eq = lambda z: 356.732*z + 145.8126
# y = [eq(x) for x in bigX]

x = torch.randn(100, 1).to(device)
y = torch.tensor(356.732 * x + 145.8126).to(device)

print("Start the training loop...")

model.train()
for i in range(EPOCHS):
    optimizer.zero_grad()
    pred = model(x)
    loss = criterion(pred, y)
    loss.backward()
    optimizer.step()

os.makedirs(LOCAL_MODEL_DIR, exist_ok=True)
model_path = os.path.join(LOCAL_MODEL_DIR, 'model.pth')

torch.save(model.state_dict(), model_path)

code_dir = os.path.join(LOCAL_MODEL_DIR, 'code')
os.makedirs(code_dir, exist_ok=True)

if os.path.exists('src/inference.py'):
    shutil.copy('src/inference.py', os.path.join(code_dir, 'inference.py'))

with tarfile.open(TAR_NAME, "w:gz") as tar:
    tar.add(model_path, arcname='model.pth')
    tar.add(code_dir, arcname='code')

print(f"Saved model to {TAR_NAME}")

try:
    session = sagemaker.Session()
    try:
        role = sagemaker.get_execution_role()
    except (ValueError, RuntimeError): #if not running on SageMaker
        role = ARN
    bucket = session.default_bucket()
    print(f"Bucket: {bucket}")
except Exception as e:
    print(e)
    exit(1)

s3_prefix = 'LinModDemo'
s3_model_path = session.upload_data(path=TAR_NAME, bucket=bucket, key_prefix=s3_prefix)

print(f"Uploaded model to {s3_model_path}")

pytorch_model = PyTorchModel(
    model_data=s3_model_path,
    role=role,
    framework_version='2.0.0',
    py_version='py310',
    entry_point='inference.py',
    sagemaker_session=session
)

predictor = pytorch_model.deploy(
    initial_instance_count=1,
    instance_type=DEPLOY_DEVICE,
    serializer=JSONSerializer(),
    deserializer=JSONDeserializer()
)

test_input = [10, 20, -5]

response = predictor.predict(test_input)
print(response)

print(f"Endpoint Name: {predictor.endpoint_name}")

#predictor.delete_endpoint()