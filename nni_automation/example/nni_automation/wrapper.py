from generate_nni_experiments_and_search_spaces import *
from start_nni_experiments import *
import os

if __name__ == '__main__':
    
    ##############################################
    ## Create experiment and search space files 
    ##############################################
    experiment_file_generator   = ModelExperimentGenerator(snakemake.config)
    search_space_file_generator = ModelSearchSpaceGenerator(snakemake.config)

    generate_experiment_files_and_search_spaces(experiment_file_generator,
                                                search_space_file_generator,
                                                snakemake.config['NNI_MODEL_PARAMS'].keys(),
                                                snakemake.output)

    ##############################################
    ## Run experiments
    ##############################################
    PORT = snakemake.config["NNI_PORT"]
        
    exporter = HyperParameterExporter()
    run_experiments(exporter, snakemake.output, PORT)