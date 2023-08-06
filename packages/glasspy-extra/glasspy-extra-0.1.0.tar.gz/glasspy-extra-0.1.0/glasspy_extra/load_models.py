import os
from pathlib import Path

import joblib

_BASEMODELPATH = Path(os.path.dirname(__file__)) / "models"

LZMA_MODELS = [
    "Tg",
    "Density293K",
    "CTEbelowTg",
]


def load_rf_model(name):
    """Loads a Random Forest model.

    Args:
      name: name of the model.

    Returns:
      scikit-learn RandomForestRegressor model.

    """
    if name in LZMA_MODELS:
        model = joblib.load(_BASEMODELPATH / f"RF_{name}.lzma")
    else:
        model = joblib.load(_BASEMODELPATH / f"RF_{name}.gz")
    return model
