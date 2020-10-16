from nnicli import Experiment
import numpy as np
import pandas as pd
import subprocess

def release_port(port):
    subprocess.run(f"fuser -k {port}/tcp", shell=True)

def wait_until_experiment_completes(exp):
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

def run_experiments(hyperparameter_exporter, snk_output, port):
    """
    
    """
    
    for experiment, outfile in zip(snk_output.experiment, snk_output.experiment_results):

        exp = Experiment()
        
        # Here just in case an error occured in a previous use of this
        # wrapper. If no other process is running on this port, it'll
        # just skip this step
        release_port(port)
        
        exp.start_experiment(experiment, port = port)
        
        wait_until_experiment_completes(exp)
        
        hyperparameter_exporter.export_experiment_results(exp, outfile)
        
        release_port(port)
    
if __name__ == '__main__':
    
    PORT = snakemake.config["NNI_PORT"][0]
    
    exporter = HyperParameterExporter()
    
    run_experiments(exporter, snakemake.output, PORT)