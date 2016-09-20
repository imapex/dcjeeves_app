# DCJeeves App
DCJeeves App is an adaptable datacenter middleware appliacation. Its goal is to make your life easier by providing an interactive interface through natural spoken language into actionable funcations in your datacenter.

Lets take a look at the basic plugin-n-play architecture:

![m'dcjeeves_app-overview](static/dcjeeves-app-overview.png)

## Backend Module
The code involved in this module is a certain set of workflows capable of being called by DCJeeves.  DCJeeves makes calls to UCSD in an automated fashion based on the command being issued.  UCSD workflows are named in such a way that DC Jeeves doesn't have to know about them up front.

#### DC Jeeves to UCSD Communication
A typical DC Jeeves supported command would something like the following:
`dcjeeves <COMMAND> on <ENVIRONMENT> at <CLOUD> where <KEY> equals <VALUE1>
`

**Configuring dcjeeves_app to be able to talk to UCSD**

Although this configured inside dcjeeves\_app its important to know how the app knows about UCSD.  The scrawl.yaml file supports a cloud of type *UCSD*.  For more information on this look at the dcjeeves_app documentation.

**Writing workflows to be auto discovered by DC Jeeves**

The underlying workflow inside UCSD would be named `DCJeeves-<COMMAND>` where `<COMMAND>` is included in the name of the workflow.  Any spaces in the command should be turned into `-` (hyphens).  Workflows written for DC Jeeves shoudld convert the COMMAND to all CAPS in order for them to stand out in the UCSD environment as part of this package.  

 
**Passing \<KEY> | \<VALUE> from dcjeeves\_app to UCSD**
 
The `<KEY> / <VALUE>` entered from DC Jeeves will map to to the *'params1'* element in a typical REST call to UCSD.  


**Putting it all together**

For example let's examine the following command:
`dcjeeves start vm on dev at Rosemont where vm name equals snoopy`

The underlying workflow that DC Jeeves will try and call shoudl be named `DCJeeves-START-VM` 

dcjeeves\_app will expect this workflow to exists as well require a workflow input called *'vm name'*.  

The REST API call for this workflow may look something like this:
` https://10.0.0.1/app/api/rest?formatType=json&opName=userAPISubmitWorkflowServiceRequest&opData={'param1': {'list': [{'name': 'vm name', 'value': 'snoopy'}]}, 'param0': 'DCJeeves-START-VM', 'param2': '-1'}`

Notice the workflow named passed in as *param0* and our key value pairs passed in as *param1*.


## Deploying the Module
To use the UCSD plugin, just imoprt the modlue into UCSD workflows.  

## Expanding the Module
Following the from the pervious section should make it quite easy to expand into other supported commands inside UCSD.  No code should need to be written inside dcjeeves\_app.

## Logging and Troubleshooting
Because the code for this is included inside UCSD workflows, all logging is done the way UCSD logs.  

The order in which to troubleshoot this modlue would look somethign like this.

* dcjeeves\_app makes a REST call to UCSD.  Verifying the actual REST call made can be found in the dcjeeves\_app system out logs.
* A successful call to UCSD will include a reponse back which includes a *SR#* inside UCSD.  This will be logged from dcjeeves\_app system out logs too.
* Look inside UCSD at the service request logged from our previous step.  As an administrator of UCSD, you should have access to the log tab for the workflow being called.  All workflow and custom tasks logs will be displayed here.








