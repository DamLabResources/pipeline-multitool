# nni pipeline automation wrapper

A collection of scripts designed to generate an experiment config file and search space and start model hyperparameter optimization. Once complete, it outputs the investigated hyperparameter combinations and their final scoring metric for ease of acquisition. 

Wrapper application example:
```
MODELS = config["NNI_MODEL_PARAMS"].keys()

rule optimize_hyperparameters:
    output:
        experiment   = expand("nni/{model}_experiments.yaml", 
                               model = MODELS),
                                
        search_space = expand("nni/search_space/{model}_search_space.json",
                               model = MODELS),
                               
        experiment_results = expand("nni/experiment_results/{model}.csv", 
                                    model = MODELS)
    wrapper:
        "pipeline-multitool/tree/main/nni_automation"
```

All created files are stored in a generated directory called ```nni```, which has the following tree structure:
```
nni/
├── experiment_results
│   └── <Model>.csv
├── <Model>_experiments.yaml
└── search_space
    └── <Model>_search_space.json
```

## Snakemake config organization

Search space and experiment config files are generated based on the following entires in the snakemake config:

1. NNI_PORT
    * The port assigned to all nni expiments
2. COMMON_NNI_EXPERIMENT_CONFIG_ARGS
    * Parameters shared by all experimental config files
3. NNI_MODEL_PARAMS
    * Model-specific parameters used in the experiment config and the model's search space.
    * Organized by creating subsections in NNI_MODEL_PARAMS that correspond with the models listed in MODELS
    * Each model subsection has two sub sections: search_space and experimental_config. The former specifies the search space you want investigated and the latter specifying parameters that are specific to that model (e.g. training script location, experiment name)
    * For the search space, list each hyperparameter and assign a list to it. The 1st entry in the list corresponds to the method used to gererate the search space. The 2nd is another list that holds values associated with that 1st entry's search parameter.
    
Here's an example of how it should be formatted:
```
NNI_PORT: 9999

COMMON_NNI_EXPERIMENT_CONFIG_ARGS:
    authorName: Bobby Link
    trialConcurrency: 3
    maxExecDuration: 5m
    maxTrialNum: 10
    trainingServicePlatform: local
    useAnnotation: false
    
    assessor:
        builtinAssessorName: Medianstop
        classArgs:
          optimize_mode: minimize
    tuner:
      builtinTunerName: TPE
      classArgs:
          optimize_mode: minimize
    trial:
        codeDir: ../Train_scripts
        
NNI_MODEL_PARAMS:
    XGBoost:
        search_space:
            n_estimators: [choice, [111, 222, 333]]
            
        experiment_config:
            searchSpacePath: search_space/XGBoost_search_space.json
            experimentName: XGB_hyperparam_opt
            trial:
                command: python3 xgb_opt.py
                
    RandomForest:
        search_space:
            n_estimators: [choice, [100, 200, 300]]
            max_depth: [choice, [4,5,6]]
            
        experiment_config:
            searchSpacePath: search_space/RandomForest_search_space.json
            experimentName: RandomForest_hyperparam_opt
            trial:
                command: python3 rf_opt.py
```

## BUGS
* Conda env fails to install remotley on GitHub. Works when installed locally
* Specifying an nni logDir throws an error when generating experiment. 

## TODO
* Incorperate unit testing for wrapper scripts
* Add descriptions for individual classes/functions
* Have model-specific parameters overwrite common parameters
