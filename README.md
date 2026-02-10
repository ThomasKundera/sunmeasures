# Sun observations and analysis

## Generalities

Lets ensure Sun appparent disk size is constant over a day of careful measures.

## Assumptions

- Decently reliable camera setup
- Sun behavior on two consecutive days about same (data semples are from 2025-08-28 and 2025-08-29).

## Setup and methods

From a location at Saint-Jean-Cap-Ferrat, Sun was picture during sunrise (some pictures still not exploited) and shortly after (in the next hour). Then along the day from close to that location, as well as the following day at various hours.

Camera used:
- Canon EOS 500D

Lens used:
- Rubinar 1000mm f/10 lens
- A 13mm extender ring had been used (needed to accomodate for camera body shape)

A standard photographic Sun filter was used.

Overexposed images (more than 20% of Sun disk image pixels saturated) are rejected from analysis.

## How to use

- git clone the repo. *WARNING*: git-lfs is required. Otherwise images data are not downloaded. 
- run the script: `code/bash/run_analysis.sh`

It should create directory `output` at the root of the repo. In it will create a python venv in it, install what's needed and process the data. It should end by displaying a plot of the Sun disk size over time of the day.

## Data analysis

- Fix time delta with reference images - ✅
- Measure Sun disk size - ✅
- Plot it against time - ✅
