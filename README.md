# Analysis of Road Representations in Search-Based Testing of Autonomous Driving Systems

## Description
Validating Autonomous Driving Systems (ADSs) is essential to ensure that the ADS meets the necessary requirements to be widely accepted. Simulation-based testing is one of the main validation approaches, in which the ADS is run in a simulated environment over different scenarios. In this context, search-based testing (SBT) is used to generate scenarios that possibly expose particular failures of the ADS under test. Most SBT approaches search for behaviors of other traffic participants, but usually fix the map of the scenario in advance. Recently, the SBT community started to investigate the search for road structures, which is particularly useful when testing specific components of the ADS, such as the lane-keeping component. However, roads can be represented in multiple ways and the impact of using a particular representation on the effectiveness of SBT is unclear. To fill this gap, this paper investigates the usage of six road representations for SBT. As a representative SBT approach, we test the lane-keeping component of an ADS in the BeamNG.tech simulator, aiming to generate roads in which the autonomous vehicle drives off the lane. We study the effectiveness of each road representation in terms of triggered failures and also diversity of the generated roads.

## Structure of the repository
* Folder *experiments* contains the experimental results

## How to reproduce the experimental results
