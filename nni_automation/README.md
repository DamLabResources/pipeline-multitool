# nni pipeline automation tool

This tool is a collection of scripts and rules designed to generate an experiment config file and search space and start the model hyperparameter search. Once complete, it outputs the investigated hyperparameter combinations and their final scoring metric for ease of acquisition. 

All created files are stored in a generated directory called ```nni```, which has the following tree structure:
```
nni/
├── experiment_results
│   └── <Model>.csv
├── <Model>_experiments.yaml
├── Search_space
│   └── <Model>_search_space.json
└── Train_scripts
    └── <Model>.py
```

To exemplify this, an end-to-end snakemake pipeline is included that optimzes the hyperparameters for XGBoost and RandomForest models on the diabetes dataset and exports the data to their corresponding csvs. To run, type the following:

```$ snakemake --use-conda --cores 4```

## Snakemake config organization

Search space and experiment config files are generated based on the following entires in the snakemake config:

1. NNI_PORT
    * The port assigned to all nni expiments
2. MODELS
    * The list of model names used for each experiment
3. COMMON_NNI_EXPERIMENT_CONFIG_ARGS
    * Parameters shared by all experimental config files
4. NNI_MODEL_PARAMS
    * Model-specific parameters used in the experiment config and the model's search space.
    * Organized by creating subsections in NNI_MODEL_PARAMS that correspond with the models listed in MODELS
    * Each model subsection has two sub sections: search_space and experimental_config. The former specifies the search space you want investigated and the latter specifying parameters that are specific to that model (e.g. training script location, experiment name)
    * For the search space, list each hyperparameter and assign a list to it. The 1st entry in the list corresponds to the method used to gererate the search space. The 2nd is another list that holds values associated with that 1st entry's search parameter.
    
Here's an example of how it should be formatted:
```
NNI_PORT: 9999

MODELS: ["XGBoost","RandomForest"]

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
        codeDir: .
        
NNI_MODEL_PARAMS:
    XGBoost:

        search_space:
            n_estimators: [choice, [111, 222, 333]]
            
        experiment_config:
            searchSpacePath: Search_space/XGBoost_search_space.json
            experimentName: XGB_hyperparam_opt
            trial:
                command: python3 Scripts/Train_scripts/xgb_opt.py
                
    RandomForest:
        search_space:
            n_estimators: [choice, [100, 200, 300]]
            max_depth: [choice, [4,5,6]]
            
        experiment_config:
            searchSpacePath: Search_space/RandomForest_search_space.json
            experimentName: RandomForest_hyperparam_opt
            trial:
                command: python3 Scripts/Train_scripts/xgb_opt.py
```

## Prerequisites:

* In the snakemake directory, put your training scripts in a directory called ```nni```. Once there, you can put them in any subdirectory of your choice. In this example, they are in a directory called ```Train_scripts```

## TODO:
* Circumvent the above prerequisite by generating an explicit path to training script location
* Output a complete xml of data to a location of the user's choice. The issue is that it needs to be created first, and snakemake is giving issues
* Have model-specific parameters overwrite common parameters