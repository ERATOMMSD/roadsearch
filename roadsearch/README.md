# Running RoadSearch

To perform a search task with RoadSearch, run the following script. 

```
python search.py --executor beamng 
                 --beamng-home BEAMNG_HOME 
                 --beamng-user BEAMNG_USER 
                 --map-size MAP_SIZE
                 --time-budget TIME_BUDGET
                 --module-name MODULE_NAME 
                 --generator-name GENERATOR_NAME
                 --log-to LOGFILE
```

`BEAMNG_HOME` and `BEAMNG_USER` should point to the directories where BeamNG.tech is installed.

In the experiments the `MAP_SIZE=200` and `TIME_BUDGET=18000` (5 hour).

`MODULE_NAME` should point to a file where the intended generator is located, and `GENERATOR_NAME` to the class defining the generator. 
The generators used in the experiments are located in `generators/samples/tuned.py'. 

The output will be a .csv file with the performance of each evaluated configuration. 

## BeamNG Simulator

A free version of the BeamNG simulator for research purposes can be obtained by registering at https://register.beamng.tech.
Please follow the installation steps included in their README.

