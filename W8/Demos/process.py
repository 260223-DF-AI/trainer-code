import os
import pandas as pd
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Process started")

    logger.info("Generating data")
    X, y = make_regression(n_samples=1000, n_features=3, noise=0.1, random_state=42) # generate the data for X and Y vars

    logger.info("Transforming data")
    df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(X.shape[1])])
    df['target'] = y

    logger.info("Splitting data")
    train_df, eval_df = train_test_split(df, test_size=0.3, random_state=42)

    logger.info("Saving data")
    base_dir = "/opt/ml/processing"
    train_path = os.path.join(base_dir, "train")
    eval_path = os.path.join(base_dir, "eval")

    os.makedirs(train_path, exist_ok=True)
    os.makedirs(eval_path, exist_ok=True)

    train_df.to_csv(os.path.join(train_path, 'train.csv'), index=False)
    eval_df.to_csv(os.path.join(eval_path, 'eval.csv'), index=False)

    logger.info("Process completed")

if __name__ == "__main__":
    main()