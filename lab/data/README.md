# Obtaining experimental data

The folder data contains the following two folders:
- [summary](https://mmm-www-videos.s3.ap-northeast-1.amazonaws.com/roadsearch/summary.zip): contains a summary of the experimental data, which is enough to run the notebooks
- [raw](https://mmm-www-videos.s3.ap-northeast-1.amazonaws.com/roadsearch/raw.zip): contains all the experimental data

Please download the files in the folder data. The final structure should be as follows:

```
.
+-- lab
  +-- data
  |   +-- summary
  |     +-- data.json
  |     +-- alterations.json
  |     +-- crossover.json
  |     +-- similarity.json
  |     +-- similarity_failures.json
  |   +-- raw
  |     +-- simulations: contains 30 experiments per representation
  |     +-- similarities: contains the results about the diversity of the simulations
  |     +-- alterations: contains the results of applying alterations 
  |     +-- crossover: contains the results of applying crossover 
  +-- src
  +-- figures
```

All the results can be reproduced from the files inside the folder `simulations`.
