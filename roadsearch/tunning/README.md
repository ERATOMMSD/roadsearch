# Running the Hyper-parameter study

To run the hyper parameter study run the following script. 

```
python optimize.py --executor beamng 
                   --beamng-home BEAMNG_HOME 
                   --beamng-user BEAMNG_USER 
                   --map-size MAP_SIZE
                   --trials NUMBER_OF_TRIALS 
                   --time-budget BUDGET_PER_TRIAL 
                   --pruning-sample EARLY_PRUNNING 
                   --generator-name GENERATOR_NAME
                   --log-to LOGFILE
```

`BEAMNG_HOME` and `BEAMNG_USER` should point to the directories where BeamNG.tech is installed.

In the experiments the `MAP_SIZE=200`, `NUMBER_OF_TRIALS=100` and `BUDGET_PER_TRIAL=3600` (1 hour). An early pruning is done when a trial is not producing any valid results (`EARLY_PRUNNING=20`). 

As for the `GENERATOR_NAME`, it could be any of the following: `['kappa', 'kappa_step', 'theta', 'theta_step', 'catmull', 'bezier']`.

The output will be a .csv file with the performance of each evaluated configuration. 

