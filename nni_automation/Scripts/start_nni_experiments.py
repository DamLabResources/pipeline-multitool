from nnicli import Experiment
import numpy as np
import pandas as pd
import subprocess

def release_port(port):
    subprocess.run(f"fuser -k {port}/tcp", shell=True)

def wait_until_experiment_completes():
    while exp.get_experiment_status()['status'] == 'RUNNING': pass

class HyperParameterExporter:
    """
    
    """
            
    def get_final_metric_data(self, experiment):
        
        metric_data = list()
        
        for trial in experiment.list_trial_jobs():
            try:
                metric_data.append([trial.finalMetricData[0].data])
            except:
                metric_data.append([None])
        
        return np.array(metric_data)
    
    def isolate_hyperparemter_names(self, experiment):
        """
        
        """
        trial                = experiment.list_trial_jobs()[0]
        hyperparameter_names = list(trial.hyperParameters[0].parameters.keys())
        return hyperparameter_names
    
    def isolate_hyperparameter_values(self, experiment):
        """
        
        
        """
        return np.array([list(trial.hyperParameters[0].parameters.values()) 
                         for trial in experiment.list_trial_jobs()])
    
    def isolate_experiment_names(self, experiment):
        return [trial.trialJobId for trial in experiment.list_trial_jobs()]
    
    def export_experiment_results(self, experiment, outfile):
        """

        """
        
        # Isolate data
        hyperparam_data  = self.isolate_hyperparameter_values(experiment)
        final_metrics    = self.get_final_metric_data(experiment)
        data             = np.append(hyperparam_data, final_metrics, axis=1)
        
        # Isolate column names and index
        hyperparam_names = self.isolate_hyperparemter_names(experiment)
        experiment_names = self.isolate_experiment_names(experiment)
        
        results = pd.DataFrame(data, columns = hyperparam_names + ['final_metric'], 
                               index = experiment_names)
        
        results.to_csv(outfile)
        
if __name__ == '__main__':
    
    PORT = list(snakemake.params.port)[0]
    
    exporter = HyperParameterExporter()
    
    for experiment, outfile in zip(snakemake.input.experiment, snakemake.output.result_csv):

        exp = Experiment()
        
        exp.start_experiment(experiment, port = PORT)
        
        wait_until_experiment_completes()
        
        exporter.export_experiment_results(exp, outfile)
        
        release_port(PORT)