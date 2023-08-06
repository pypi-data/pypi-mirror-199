from dtw_sofar import *
from unittest.mock import patch
import numpy as np
import pickle


def test_dtwcost():
    features_a = np.random.rand(10)
    features_b = features_a
    cost = dtw_cost(features_a, features_b)
    assert np.isclose(0, cost)


def test_backpointers():
    frame_features = np.random.rand(10)
    text_features = np.random.rand(5)
    cost_matrix, backpointers = get_initial_matrices(frame_features, text_features)
    backpointers_expected = np.zeros((frame_features.shape[0], text_features.shape[0]))
    assert np.array_equal(backpointers, backpointers_expected)


def test_get_initial_matrices_costmatrix():
    frame_features = np.random.rand(20)
    text_features = np.random.rand(10)
    cost_matrix, backpointers = get_initial_matrices(frame_features, text_features)
    n = frame_features.shape[0]
    m = text_features.shape[0]

    cost_matrix_expected = np.zeros((n + 1, m + 1))
    for i in range(1, n + 1):
        cost_matrix_expected[i, 0] = np.inf
    for i in range(1, m + 1):
        cost_matrix_expected[0, i] = np.inf
    assert np.array_equal(cost_matrix_expected, cost_matrix)


@patch('dtw_sofar.dtw_cost', return_value=0.5)
def test_dtw(dtw):
    frame_features = np.zeros((5, 1))
    text_features = np.zeros((10, 1))
    alignment_path, dtw_matrix = dtw_sofar.dtw(frame_features, text_features, lambda a, b: np.linalg.norm(a - b))
    expected = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]
    assert alignment_path == expected


@patch('dtw_sofar.dtw_cost', return_value=0)
def test_dtw_sofar(dtwdtw_sofar):
    frame_features = np.zeros((5, 1))
    text_features = np.zeros((10, 1))
    n = frame_features.shape[0]
    m = text_features.shape[0]
    backpointers = np.zeros((n, m))

    cost_matrix = np.zeros((n + 1, m + 1))
    for i in range(1, n + 1):
        cost_matrix[i, 0] = np.inf
    for i in range(1, m + 1):
        cost_matrix[0, i] = np.inf

    expected_path = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    for i in range(len(frame_features)):
        path_sofar, cost_matrix, backpointers, current_predicted_idx = dtw_sofar.dtw_sofar(
            frame_features[i], text_features, i, cost_matrix, backpointers, lambda a, b: np.linalg.norm(a - b)
        )
        assert current_predicted_idx == 0
        assert len(path_sofar) == i + 1
        assert path_sofar[i] == expected_path[i]


# sanity check
def test_always_passes():
    assert True


# integration test: dtw_onthefly_classification is where the "units"
# test above come together:
def save_processed_data(unserialized_data, file_name):
    with open(file_name, 'wb') as handle:
        pickle.dump(unserialized_data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def read_processed_data(file_name):
    with open(file_name, 'rb') as handle:
        unserialized_data = pickle.load(handle)
    return unserialized_data


def test_integ_dtwclassification():
    for i in range(10):
        frame_features = np.random.rand(10)
        text_features = np.random.rand(5)
        final_path, cost_matrix, onthefly_predictions, onthefly_path = dtw_onthefly_classification(
            frame_features, text_features
        )

        expected_final_path = read_processed_data('dtw_sofar/tests/expected_final_path.pickle')
        assert final_path == expected_final_path

        expected_onthefly_path = read_processed_data('dtw_sofar/tests/expected_otf_path.pickle')
        assert onthefly_path == expected_onthefly_path

        expected_preds = read_processed_data('dtw_sofar/tests/expected_preds.pickle')
        assert expected_preds == onthefly_predictions
