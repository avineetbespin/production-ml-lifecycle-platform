import pandas as pd
from sklearn.datasets import make_classification


def build_training_dataset(n_samples: int = 1000, random_state: int = 42) -> pd.DataFrame:
    X, y = make_classification(
        n_samples=n_samples,
        n_features=12,
        n_informative=8,
        n_redundant=2,
        random_state=random_state,
    )
    df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(X.shape[1])])
    df["target"] = y
    df["sensitive_group"] = (df["feature_0"] > 0).astype(int)
    return df


def load_reference_dataset(reference_path: str = None) -> pd.DataFrame:
    if reference_path:
        return pd.read_csv(reference_path)
    return build_training_dataset(n_samples=500, random_state=1)
