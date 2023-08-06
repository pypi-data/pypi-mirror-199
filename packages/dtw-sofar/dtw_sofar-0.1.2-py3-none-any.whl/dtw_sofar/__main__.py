from .dtw_sofar import dtw_onthefly_classification
from numpy import random

if __name__ == "__main__":
    image_features = random.rand(
        512,
    )
    text_features = random.rand(
        15,
    )
    (
        dtw_final_path,
        cost_matrix,
        onthefly_predictions,
        onthefly_path,
    ) = dtw_onthefly_classification(image_features, text_features)
