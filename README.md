# star-formation-methods
A few independednt methods to explore the star formation requirements and behaviors within AMR grid magnetohydrodynamics and N-body software suite Torch.

## JeansCalculator
Used to determine the gas density corresponding to the length scale of the smallest resolvable Jeans Length (Jeans 1902) adhering to the Truelove Criterion (Truelove+97). Written by SCL.

## SinkGasStatus
Test code to isolate sink particles and encompassed grid cells to determine gas mass contained within. Uses hdf5 data processing python package yt (yt-project.org). Written by SCL; work in progress.

## StarPlacement
Contains methods used for placing star particles onto the simulation grid. Originally written by JW; augmented and repurposed by SCL. Also contains a simple example of a Monte Carlo method with the intention of repurposing to examine boundness likelihood of stars placed randomly inside a star forming region. - SCL; work in progress.