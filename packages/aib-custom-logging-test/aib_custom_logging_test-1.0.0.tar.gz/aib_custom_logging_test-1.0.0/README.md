# aib_custom_logger

This serves as the official documentation for the PyPi package developed by the AIB MLOPS team called "aib-custom-logger".

## Introduction
The "aib-custom-logger" pypi pkg offers the abilty to throw logs that contains meaningful metadata, which can be used in both debugging and monitoring.


![](imgs/intro.png)



## Usage
The pkg exists in the aib-mirror, once you install the pkg using "pip install aib-custom-logger", you can proceed to use it as follows:

```
 from aib_custom_logger_tst.aib_custom_logger import aib_logger
 
 my_logger=aib_logger(project_id,pipeline_name="{{$.pipeline_job_name}}")
 
 my_logger.log(
  f"Batch prediction job output info: {job.output_info}",
  category=aib_logger.Categories.DATA,
  action=aib_logger.Actions.CREATE,
  extra_labels=['batch_prediction','automl']
 )
```


### 1.init()
After you import the pkg you need to initialise an object of the aib_logger class. The constructor takes the following params:

- **project (str):** Required. The project id of to add to the google cloud client for logging.
- **pipeline_name (str):** Optional. The pipeline run name that this log was thrown from. This can be achieved by passing the placeholder "{{$.pipeline_job_name}}" which will be replaced by the run_name at run time. Default is empty string "".
- **logger_name (str):** Optional. The name of the custom logger which you can then query by. Default is "aib_custom_logger".

### 2.Log()
the log function takes the following params:

- **msg (str):** Required. The content you wish to log.
- **category (aib_logger.Categories):** Optional. An enum to choose from relating the category of the log. Default is "Other".
- **action (aib_logger.Actions):** Optional. An enum to choose from relating the action of the log. Default is "Other".
- **severity (aib_logger.Severities):** Optional. An enum to choose from relating the level of severity of the log. Default is "Info".
- **extra_labels (list):** Optional. Extra custom labels to add to the log.
- **object (dict):** Optional. An extra custom dictionary to be added.

### 3.Categories
The following are the available categories (key=value) defined in the aib_logger.Categories enum:

MODEL = "Model"<br/>
DATA = "Data"<br/>
METRIC = "Metric"<br/>
OTHER = "Other"<br/>

### 4.Actions
The following are the available actions (key=value) defined in the aib_logger.Actions enum:

CREATE="Create"<br/>
UPDATE="Update"<br/>
DELETE="Delete"<br/>
UPLOAD="Upload"<br/>
OTHER="Other"<br/>

### 5.Severities
The following are the available severities (key=value) defined in the aib_logger.Severities enum:

INFO="INFO"<br/>
WARNING="WARNING"<br/>
ERROR="ERROR"<br/>


## Querying
In order to see the logs being produced by your pipeline, you need to navigate to the logging page in GCP and start querying.

**logname:** you can query for all the logs that were produced by a specific custom logger name.

![](imgs/q1.png)



**jsonpayload:** the jsonpayload holds the content of your logs and the metadata. It is a key value object as seen below.

![](imgs/q2.png)





## Limitations
Currently the custom logs yielded by this pkg can only appear in the logging page, and not the logs section in the vertex pipelines UI.

 
