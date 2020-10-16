import argparse
import yaml
from yaml import Loader, Dumper
import json
from deepmerge import always_merger

class ModelExperimentGenerator():
    """
    Designed to parse the snakemake config file and generate an nni
    experiment file for each model specified in the config. 
    """
    
    def __init__(self, config):
        self.data   = config
        
    def merge_arguments(self, common_args, model_args):
        return always_merger.merge(common_args, model_args)
    
    def save_yaml(self, data, outfile):
        
        with open(outfile,'w') as handle:
            yaml.dump(data, handle, 
                      default_flow_style=False, sort_keys=False,
                      Dumper = Dumper)
    
    def convert_config_to_experiment(self, model, outfile):
        
        common_args = self.data["COMMON_NNI_EXPERIMENT_CONFIG_ARGS"]
        model_args  = self.data['NNI_MODEL_PARAMS'][model]["experiment_config"]

        nni_experiment_config_data = self.merge_arguments(common_args, model_args)
        
        self.save_yaml(nni_experiment_config_data, outfile)

class ModelSearchSpaceGenerator():
    """
    Designed to parse the snakemake config file and generate an nni
    search space file for each model specified in the config. 
    """
    
    def __init__(self, config):
        self.data = config
        
    def generate_search_space_file_data(self, initial_search_space):
        return {key : dict(zip(["_type","_value"], values)) for key, values in initial_search_space.items()}
    
    def save_json(self, data, outpath):
        with open(outpath, 'w') as handle:
            json.dump(data, handle)
            
    def convert_config_to_search_space(self, model, outfile):
        
        model_search_space = self.data['NNI_MODEL_PARAMS'][model]["search_space"]

        search_space_file_data = self.generate_search_space_file_data(model_search_space)

        self.save_json(search_space_file_data, outfile)

def generate_experiment_files_and_search_spaces(experiment_file_generator, search_space_file_generator, models, params):
    """
    
    """
        
    grouped_params = zip(models, params.experiment, params.search_space)
    
    for model, model_experiments, model_search_space in grouped_params:
                
        experiment_file_generator.convert_config_to_experiment(model, model_experiments)
        search_space_file_generator.convert_config_to_search_space(model, model_search_space)
        
if __name__ == '__main__':
    
    experiment_file_generator   = ModelExperimentGenerator(snakemake.config)
    search_space_file_generator = ModelSearchSpaceGenerator(snakemake.config)
    
    generate_experiment_files_and_search_spaces(experiment_file_generator,
                                                search_space_file_generator,
                                                config['NNI_MODEL_PARAMS'].keys(),
                                                snakemake.output)