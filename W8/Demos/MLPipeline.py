# define the training data
# define the model
# train the model
# save the model
# deploy the model

import sagemaker
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.workflow.model_step import ModelStep
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.processing import ProcessingOutput
from sagemaker.pytorch import PyTorch
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.workflow.parameters import ParameterInteger, ParameterFloat
from sagemaker.inputs import TrainingInput
from sagemaker.model import Model

def main():
    pipeline_session = PipelineSession() # this allows us to prep the pipeline logic

    try:
        role = sagemaker.get_execution_role()
    except ValueError:
        role = "arn:aws:iam::407975137156:role/2371-SageMaker-ScriptingRole"
        # permissions!

    epochs = ParameterInteger(
        name="TrainingEpochs",
        default_value=100
    )

    learning_rate = ParameterFloat(
        name="LearningRate",
        default_value=0.01
    )

    # Prep the data
    processor = SKLearnProcessor(
        framework_version="1.2-1",
        role=role,
        instance_count=1,
        instance_type="ml.t3.medium", # smaller instance for the easier job
        sagemaker_session=pipeline_session,
        base_job_name="cleaning-data",
    )

    step_process = ProcessingStep(
        name="CleanData",
        processor = processor,
        inputs = [],
        outputs = [
            ProcessingOutput(output_name="train", source="/opt/ml/processing/train"),
            ProcessingOutput(output_name="eval", source="/opt/ml/processing/eval")
        ],
        code = "process.py"
    )

    # The Training
    pt_estimator = PyTorch(
        role = role,
        py_version= 'py310',
        framework_version='2.1',
        instance_count = 1,
        instance_type = 'ml.m5.large',
        hyperparameters = {
            'epochs': epochs,
            'learning_rate': learning_rate
        },
        sagemaker_session = pipeline_session,
        entry_point = "train.py"
    )

    step_train = TrainingStep(
        estimator = pt_estimator,
        name = "TrainLRModel",
        inputs = {
            "train": TrainingInput(
                step_process.properties.ProcessingOutputConfig.Outputs["train"].S3Output.S3Uri,
                content_type = 'text/csv'
            )
        }
    )

    # save the artifact - a versioned model
    model = Model(
        image_uri = pt_estimator.training_image_uri(),
        model_data = step_train.properties.ModelArtifacts.S3ModelArtifacts,
        sagemaker_session = pipeline_session,
        role = role
    )

    step_register = ModelStep(
        name="RegisterLRModel",
        step_args = model.register(
            content_types=["text/csv"],
            response_types=["text/csv"],
            inference_instances=["ml.t2.medium","ml.m5.xlarge"],
            transform_instances=["ml.m5.xlarge"],
            model_package_group_name="LRModelGoup",
            approval_status="PendingManualApproval"
        )
    )

    pipeline = Pipeline(
        name = "MLPipeline",
        parameters = [epochs, learning_rate],
        steps = [step_process, step_train, step_register],
        sagemaker_session = pipeline_session
    )

    pipeline.upsert(role_arn = role)

if __name__ == "__main__":
    main()