# dtw-sofar

[![License](https://img.shields.io/github/license/egeozguroglu/dtw-sofar.svg)](https://github.com/egeozguroglu/dtw-sofar)
![GitHub issues](https://img.shields.io/github/issues/egeozguroglu/dtw-sofar) [![Build Status](https://github.com/egeozguroglu/dtw-sofar/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/egeozguroglu/dtw-sofar/actions?query=workflow%3A%22Build+Status%22) [![codecov](https://codecov.io/gh/egeozguroglu/dtw-sofar/branch/main/graph/badge.svg)](https://codecov.io/gh/egeozguroglu/dtw-sofar)


# Overview

This library implements the "Dynamic Time Warping Algorithm" for multimodal research in a way it can warp the time series received "so far." In other words, it modifies the dynamic time warping algorithm to be compatible with 'iterative stimuli' (when future points in the time series are received one by one). 

One motivating application is aligning natural language annotations and video frames for research on Visual Language Models (e.g. [CLIP by OpenAI](https://openai.com/blog/clip/)), when the latter's embeddings are received frame by frame (e.g. we're making observations and don't have access to future frames). With "dtw-sofar," we can predict optimally matching annotations to new video frames on the fly - by relying on temporal information available "so far."

## Development and Contributions
For development details and contribution instructions, please refer to the [contribution guidelines](https://github.com/egeozguroglu/dtw-sofar/blob/main/CONTRIBUTING.md).


# Installation: 
First, install Python 3.7 (or later) and numpy, and then install this repo as a Python package. 

```bash
$ pip install numpy
$ pip install dtw-sofar
```

# Quick Start Examples:
Below is a sample use-case for quick start:
    
```python
import importlib
import numpy as np
dtwsofar = importlib.import_module('dtw-sofar.dtw_sofar')

video_features = np.load('CLIP_video_embeddings_path')
text_features = np.load('CLIP_text_embeddings_path')

# iterates over each RGB frame's CLIP embeddings and classifies matching text embeddings on-the-fly:
final_path, dtw_matrix, onthefly_predictions, onthefly_path = dtwsofar.dtw_onthefly_classification(video_features, text_features)
```
This use case demonstrates performing dynamic time warping so-far on image and natural language embeddings from Open AI's CLIP Model, so as to align them. See the overview for relevance. 

This library can also be used for simpler time-series:
```python
# time-series to be aligned with dynamic time warping "so far":
time_series_a = np.random.rand(100, 1)
time_series_b = np.random.rand(35,1)

final_path, dtw_matrix, onthefly_alignment, onthefly_path = dtwsofar.dtw_onthefly_classification(time_series_a, time_series_b)
```