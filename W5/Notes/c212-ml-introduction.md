# Introduction to Machine Learning

## Learning Objectives

- Define Machine Learning and distinguish it from traditional programming
- Identify the three major types of ML: supervised, unsupervised, and reinforcement learning
- Understand the basic ML workflow from data to prediction
- Recognize where ML fits in the data pipeline

## Why This Matters

Machine Learning is the engine behind most modern AI applications. As data engineers, the pipelines you build feed directly into ML systems. Understanding how ML works helps you design better data infrastructure -- you will know what data scientists need, how they use it, and why data quality matters so much in this context.

## The Concept

### Traditional Programming vs Machine Learning

In traditional programming, a developer writes explicit rules:

```
Input + Rules = Output
Example: IF temperature > 100 THEN alert = "overheating"
```

In Machine Learning, the approach is inverted:

```
Input + Output = Rules (learned automatically)
Example: Given thousands of temperature readings labeled "normal" or "overheating",
         the system learns the threshold on its own.
```

This distinction is fundamental. ML systems discover patterns from data rather than following hand-coded logic.

### Types of Machine Learning

#### Supervised Learning

The model learns from labeled examples -- data where the correct answer is already known.

| Task Type | Description | Example |
| --------- | ----------- | ------- |
| Classification | Predict a category | Spam vs. Not Spam |
| Regression | Predict a number | House price prediction |

**How it works:**

1. Provide training data with inputs and correct outputs
2. The model finds patterns that map inputs to outputs
3. Apply the trained model to new, unseen data

#### Unsupervised Learning

The model finds patterns in data without labeled examples.

| Task Type | Description | Example |
| --------- | ----------- | ------- |
| Clustering | Group similar items | Customer segmentation |
| Dimensionality Reduction | Simplify complex data | Feature extraction |
| Anomaly Detection | Find unusual patterns | Fraud detection |

#### Reinforcement Learning

The model learns by interacting with an environment and receiving rewards or penalties.

- **Example**: A game-playing AI that learns winning strategies through trial and error
- **Real-world use**: Robotics, autonomous vehicles, recommendation optimization

### The ML Workflow

```
Raw Data --> Data Preparation --> Feature Engineering --> Model Training --> Evaluation --> Deployment
   |              |                     |                     |               |              |
   v              v                     v                     v               v              v
Collect      Clean, transform     Select/create          Train model     Measure       Serve
from         missing values,      relevant               with algorithm  accuracy,     predictions
sources      normalize            variables                              precision
```

This workflow shows where data engineering (the first three steps) directly supports ML. The quality of data preparation determines the quality of the model.

### Key ML Concepts

- **Features**: The input variables a model uses to make predictions (columns in your data)
- **Labels**: The correct answers used during training (supervised learning)
- **Training Set**: Data used to teach the model
- **Test Set**: Data held back to evaluate model performance
- **Overfitting**: When a model memorizes training data but fails on new data
- **Underfitting**: When a model is too simple to capture the underlying pattern

### The Connection to Data Engineering

Data engineers play a critical role in ML success:

1. **Data Collection**: Building pipelines that gather and consolidate raw data
2. **Data Quality**: Ensuring accuracy, completeness, and consistency
3. **Feature Stores**: Managing reusable, pre-computed features
4. **Model Serving**: Deploying models via APIs and monitoring performance
5. **Data Versioning**: Tracking which data was used to train which model

## Key Takeaways

- Machine Learning is about learning patterns from data rather than writing explicit rules
- Supervised learning uses labeled data; unsupervised learning finds patterns without labels
- Data quality and preparation are the most time-consuming and impactful parts of ML
- Data engineers are essential partners in building successful ML systems

## Additional Resources

- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/user_guide.html)
- [AWS Machine Learning Concepts](https://aws.amazon.com/what-is/machine-learning/)
