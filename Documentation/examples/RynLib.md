
The first thing we have to do is actually install the package and build it out. All changes live on GitHub, so we'll start by cloning the repository

```shell
git clone https://github.com/McCoyGroup/RynLib.git RynLib
```

### Installing

`RynLib` is distributed as a containerized application through [DockerHub](https://hub.docker.com/repository/docker/mccoygroup/rynlib).
We make use of this to install RynLib. 

You can find some more details [here](RynLib/Installing.md).

### The rynlib CLI

As a containerized application intended for use in an HPC environment, `RynLib` is mostly run as a command-line tool. At a later date, this might be distributed in a `module`-like way, but for now these tools are stored in `RynLib/setup/env.sh`, which you'll load in via the [`source`](https://linuxize.com/post/bash-source-command/) command (or its alias `.`)

```shell
. RynLib/setup/env.sh
```

This will define the bash function `rynlib` which should be able to determine your HPC environment and work accordingly. 
More documentation on this can be found [here](RynLib/CommandLineInterface.md).

### Building

We currently distribute RynLib building off of Ubuntu and CentOS, with OpenMPI and MPICH as the MPI implementations.
If you want to build `RynLib` with a different underlying OS or different OS, you can can look at `RynLib/setup/build` and the various `Dockerfile` setups we have there.

## Components

### Config Files

Most of the parts of the package (i.e. the simulations, potentials, and importance samplers) are set up using configuration files. 
There is a standardized configuration format for these files, which is a weird JSON-like python file. 
It's simple enough that I'm disinclined to change it, unless someone has a very strong opinion.

You can find more info [here](RynLib/ConfigFiles.md)

### Potentials

One of the big benefits of RynLib is simplifying the process of using compiled potentials. 
Many potentials have already been made accessible, but it's still worth knowing how the system works.

Potentials are generally stored in `/config/potentials` and you load them using the `PotentialManager` class in `PlzNumbers`.
Once loaded, a potential can be called just like any other callable object in python.

More info is [here](RynLib/Potentials.md)

### Simulations

Managing simulations is much simpler than managing potentials. 
To get a simulation set up, we just create a `config.py` file inside a directory and use

```shell
rynlib sim add NAME SRC
```

and everything in that directory will get copied into the container's managed space.

Once we have our simulation added, we can start to work with it. 
Details on that are [here](RynLib/Simulations.md).

### Setting up Importance Sampling

An implementation of importance sampling is baked into the package, but this requires a user-side function to evaluate the trial wavefunction (and optionally derivatives). 
Details are [here](RynLib/ImportanceSampling.md)

## Running on HPCs

A core use case for all of this is High-Performance Computing (HPC) environments, but happily due to the containerization most things that "just work" locally "just work" on the HPC.

### Writing an SBATCH file

Both NeRSC and the local University of Washington cluster use the SLURM scheduler for jobs, so I can only detail how this works with `sbatch`, not sure about other schedulers.

Some sample scripts are [here](RynLib/SubmittingWithSBatch.md)
