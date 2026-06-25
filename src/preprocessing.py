"""Preprocessing pipeline.

The whole point of wrapping preprocessing in a scikit-learn ``Pipeline`` /
``ColumnTransformer`` is to prevent data leakage: scalers and encoders are fit
*inside* each cross-validation fold on the training portion only, never on the
held-out data. This is the single biggest correctness fix over the original
course notebook, which fed raw, unscaled features straight into SVM and MLP.
"""
from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from . import config


def build_preprocessor() -> ColumnTransformer:
    """Numeric -> median impute + standardise; categorical -> mode impute + one-hot."""
    numeric = Pipeline(
        steps=[
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]
    )
    categorical = Pipeline(
        steps=[
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("num", numeric, config.NUMERIC_FEATURES),
            ("cat", categorical, config.CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )


def feature_names_out(preprocessor: ColumnTransformer) -> list[str]:
    """Readable names for the transformed feature matrix (post one-hot)."""
    return list(preprocessor.get_feature_names_out())
