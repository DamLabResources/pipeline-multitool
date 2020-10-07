# pipeline-multitool

Repo designed to hold wrappers and utils for flexible pipeline design. Current tools include:

nni_automation:
* Wrapper designed to automate mulitple model hyperparameter optimization. Creates experiemnt configs and model search spaces derived from snakemake config, runs nni experiments, and exports hyperparameter combination outputs to csv. 
