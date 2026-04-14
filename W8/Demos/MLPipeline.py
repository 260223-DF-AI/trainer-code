# define the training data
# define the model
# train the model
# save the model
# deploy the model

import sagemaker
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.workflow.steps import ProcessingStep
from sagemaker.sklearn.processing import SKLearnProcessor

pipeline_session = PipelineSession()

try:
    role = sagemaker.get_execution_role()
except ValueError:
    role = "ARN"

processor = SKLearnProcessor(
    framework_version="1.2-1",
    role=role,
    instance_count=1,
    instance_type="ml.m5.xlarge",
    sagemaker_session=pipeline_session
)

step_process = ProcessingStep(
    name="CleanData",
    processor = processor,
    inputs = [],
    outputs = [],
    code = "process.py"
)

pipeline = Pipeline(
    name = "MLPipeline",
    steps = [step_process],
    sagemaker_session = pipeline_session
)

pipeline.upsert(role_arn = role)