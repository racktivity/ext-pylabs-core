@metadata title=PyApps Practical Information
@metadata order=25
@metadata tagstring=practical create pyapp

[introduction]: #/PyLabsApps/Introduction
[model]: #/PyLabsApps/Modeling


#PyApps Practical Information
In the [introduction][] you have learned the theoretical side of PyLabs Applications, such as the architecture and directory structure. 
In practice you will notice that the PyLabs framework automates many of the steps in creating a PyApp.

This section gives you an overview of the practical steps in creating a PyApp.


##Creating a PyApp
When you want to create a PyApp it is not necessary to create manually the complete PyApp directory structure as shown in the [introduction][].
You need to create **one** directory, the [model][] directory which must contain at least one model file:

	/opt/qbase5/pyapps/<yourpyapp>/interface/model/<pyappdomain>/<rootobject>.py
	
where:

	<yourpyapp>: the name of your PyApp
	<pyappdomain>: the domain of your PyApp
	<rootobject>: the name of a root object
	
Define the properties of the root object model file as explained on the [Modeling page][model]. Once you have finished these steps, you can install the PyApp.
By installing the PyApp (via the Q-Shell), most of the directory structure and some core objects (such as job, page, space, ...) are generated. 

	p.application.install('yourpyapp')

See below for the created structure when you have defined one root object model.


##Generated Directories and Files

	├── __init__.py
	└── <yourpyapp>
	    ├── cfg
	    │   ├── applicationserver.cfg
	    │   ├── applicationserverservice.cfg
	    │   └── wfe.cfg
	    ├── client
	    │   ├── action
	    │   │   ├── core
	    │   │   │   ├── __init__.py
	    │   │   │   ├── __init__.pyc
	    │   │   │   ├── job.py
	    │   │   │   └── job.pyc
	    │   │   ├── __init__.py
	    │   │   ├── __init__.pyc
	    │   │   └── ui
	    │   │       ├── __init__.py
	    │   │       ├── __init__.pyc
	    │   │       ├── page.py
	    │   │       ├── page.pyc
	    │   │       ├── space.py
	    │   │       └── space.pyc
	    │   ├── actor
	    │   │   ├── __init__.py
	    │   │   └── __init__.pyc
	    │   ├── __init__.py
	    │   └── __init__.pyc
	    ├── impl
	    │   ├── action
	    │   │   ├── core
	    │   │   │   └── job
	    │   │   │       ├── clear
	    │   │   │       │   ├── 1_job_clear.py
	    │   │   │       │   └── 1_job_clear.pyc
	    │   │   │       ├── create
	    │   │   │       │   ├── 1_job_create.py
	    │   │   │       │   └── 1_job_create.pyc
	    │   │   │       ├── delete
	    │   │   │       │   ├── 1_job_delete.py
	    │   │   │       │   └── 1_job_delete.pyc
	    │   │   │       ├── find
	    │   │   │       │   ├── 1_job_find.py
	    │   │   │       │   └── 1_job_find.pyc
	    │   │   │       ├── findLatestJob
	    │   │   │       ├── findLatestJobs
	    │   │   │       │   ├── 1_job_findLatestJobs.py
	    │   │   │       │   └── 1_job_findLatestJobs.pyc
	    │   │   │       ├── getJobtree
	    │   │   │       │   ├── 1_job_getJobTree.py
	    │   │   │       │   └── 1_job_getJobTree.pyc
	    │   │   │       ├── getJobTree
	    │   │   │       ├── getLogInfo
	    │   │   │       │   ├── 1_job_getLogInfo.py
	    │   │   │       │   └── 1_job_getLogInfo.pyc
	    │   │   │       ├── getLogoInfo
	    │   │   │       ├── getObject
	    │   │   │       │   ├── 1_job_getObject.py
	    │   │   │       │   └── 1_job_getObject.pyc
	    │   │   │       ├── getXML
	    │   │   │       │   ├── 1_job_getXML.py
	    │   │   │       │   └── 1_job_getXML.pyc
	    │   │   │       ├── getXMLSchema
	    │   │   │       │   ├── 1_job_getXMLSchema.py
	    │   │   │       │   └── 1_job_getXMLSchema.pyc
	    │   │   │       └── getYAML
	    │   │   │           ├── 1_job_getYAML.py
	    │   │   │           └── 1_job_getYAML.pyc
	    │   │   └── ui
	    │   │       ├── page
	    │   │       │   ├── create
	    │   │       │   │   ├── 1_page_create.py
	    │   │       │   │   └── 1_page_create.pyc
	    │   │       │   ├── delete
	    │   │       │   │   ├── 1_page_delete.py
	    │   │       │   │   └── 1_page_delete.pyc
	    │   │       │   ├── find
	    │   │       │   │   ├── 1_page_find.py
	    │   │       │   │   └── 1_page_find.pyc
	    │   │       │   ├── getObject
	    │   │       │   │   ├── 1_page_getObject.py
	    │   │       │   │   └── 1_page_getObject.pyc
	    │   │       │   └── update
	    │   │       │       ├── 1_page_update.py
	    │   │       │       └── 1_page_update.pyc
	    │   │       └── space
	    │   │           ├── create
	    │   │           │   ├── 1_space_create.py
	    │   │           │   └── 1_space_create.pyc
	    │   │           ├── delete
	    │   │           │   ├── 1_space_delete.py
	    │   │           │   └── 1_space_delete.pyc
	    │   │           ├── find
	    │   │           │   ├── 1_space_find.py
	    │   │           │   └── 1_space_find.pyc
	    │   │           ├── getObject
	    │   │           │   ├── 1_space_getObject.py
	    │   │           │   └── 1_space_getObject.pyc
	    │   │           └── update
	    │   │               ├── 1_space_update.py
	    │   │               └── 1_space_update.pyc
	    │   ├── actor
	    │   ├── authenticate
	    │   ├── authorize
	    │   ├── init
	    │   │   └── portal
	    │   │       ├── 7_populate_portal.py
	    │   │       └── 7_populate_portal.pyc
	    │   ├── osis
	    │   │   └── osis
	    │   │       ├── delete
	    │   │       │   ├── 1_job_delete.py
	    │   │       │   ├── 1_job_delete.pyc
	    │   │       │   ├── 1_object_delete.py
	    │   │       │   ├── 1_object_delete.pyc
	    │   │       │   ├── 3_object_generateevent_delete.py
	    │   │       │   ├── 3_object_generateevent_delete.pyc
	    │   │       │   ├── 3_page_delete.py
	    │   │       │   ├── 3_page_delete.pyc
	    │   │       │   ├── 3_space_delete.py
	    │   │       │   └── 3_space_delete.pyc
	    │   │       ├── findasview
	    │   │       │   ├── object_findasview.py
	    │   │       │   └── object_findasview.pyc
	    │   │       ├── findobject
	    │   │       │   ├── object_find.py
	    │   │       │   └── object_find.pyc
	    │   │       ├── get
	    │   │       │   ├── 1_object_get.py
	    │   │       │   └── 1_object_get.pyc
	    │   │       ├── query
	    │   │       │   ├── object_query.py
	    │   │       │   └── object_query.pyc
	    │   │       └── store
	    │   │           ├── 1_object_generateevent_store.py
	    │   │           ├── 1_object_generateevent_store.pyc
	    │   │           ├── 3_job_store.py
	    │   │           ├── 3_job_store.pyc
	    │   │           ├── 3_object_store.py
	    │   │           ├── 3_object_store.pyc
	    │   │           ├── 3_page_store.py
	    │   │           ├── 3_page_store.pyc
	    │   │           ├── 3_space_store.py
	    │   │           └── 3_space_store.pyc
	    │   ├── portal
	    │   │   └── jsmacros
	    │   ├── schedule
	    │   ├── service
	    │   │   ├── AgentSVC.py
	    │   │   ├── AgentSVC.pyc
	    │   │   ├── core
	    │   │   │   ├── job.py
	    │   │   │   └── job.pyc
	    │   │   ├── osissvc.py
	    │   │   ├── osissvc.pyc
	    │   │   ├── Scheduler.py
	    │   │   ├── Scheduler.pyc
	    │   │   └── ui
	    │   │       ├── page.py
	    │   │       ├── page.pyc
	    │   │       ├── portal.py
	    │   │       ├── portal.pyc
	    │   │       ├── space.py
	    │   │       ├── space.pyc
	    │   │       ├── wizard.py
	    │   │       └── wizard.pyc
	    │   ├── setup
	    │   │   └── osis
	    │   │       ├── job_view_list.py
	    │   │       ├── job_view_list.pyc
	    │   │       ├── job_view_parentlist.py
	    │   │       ├── job_view_parentlist.pyc
	    │   │       ├── page_view.py
	    │   │       ├── page_view.pyc
	    │   │       ├── page_view_tags.py
	    │   │       ├── page_view_tags.pyc
	    │   │       ├── space_view.py
	    │   │       ├── space_view.pyc
	    │   │       ├── space_view_tags.py
	    │   │       └── space_view_tags.pyc
	    │   └── ui
	    │       ├── form
	    │       └── wizard
	    ├── __init__.py
	    ├── interface
	    │   ├── action
	    │   │   ├── core
	    │   │   │   ├── job.py
	    │   │   │   └── job.pyc
	    │   │   └── ui
	    │   │       ├── page.py
	    │   │       ├── page.pyc
	    │   │       ├── space.py
	    │   │       └── space.pyc
	    │   ├── actor
	    │   ├── config
	    │   ├── model
	    │   │   ├── core
	    │   │   │   ├── job.py
	    │   │   │   └── job.pyc
	    │   │   ├── <pyappdomain>
	    │   │   │   ├── <rootobject>.py
	    │   │   │   └── <rootobject>.pyc
	    │   │   └── ui
	    │   │       ├── page.py
	    │   │       ├── page.pyc
	    │   │       ├── space.py
	    │   │       └── space.pyc
	    │   └── monitoring
	    ├── portal
	    │   ├── spaces
	    │   │   ├── Admin
	    │   │   │   ├── Home
	    │   │   │   │   ├── Home.md
	    │   │   │   │   └── Spaces
	    │   │   │   │       └── Spaces.md
	    │   │   │   └── pagetree.md
	    │   │   └── api
	    │   │       └── Home
	    │   │           ├── Home.md
	    │   │           ├── rest
	    │   │           │   ├── rest_job
	    │   │           │   │   └── rest_job.md
	    │   │           │   ├── rest.md
	    │   │           │   ├── rest_page
	    │   │           │   │   └── rest_page.md
	    │   │           │   └── rest_space
	    │   │           │       └── rest_space.md
	    │   │           └── xmlrpc
	    │   │               ├── xmlrpc_job
	    │   │               │   └── xmlrpc_job.md
	    │   │               ├── xmlrpc.md
	    │   │               ├── xmlrpc_page
	    │   │               │   └── xmlrpc_page.md
	    │   │               └── xmlrpc_space
	    │   │                   └── xmlrpc_space.md
	    │   └── static
	    │       └── js
	    │           └── config.js
	    └── tmp
	        └── action
	            ├── client
	            │   ├── cloud_api_clients.py
	            │   ├── core
	            │   │   └── client_job.py
	            │   └── ui
	            │       ├── client_page.py
	            │       └── client_space.py
	            └── lib
	                ├── cloud_api_job.py
	                ├── cloud_api_page.py
	                └── cloud_api_space.py
	                

Always keep in mind that the shown directory structure is incomplete. It may be necessary to create directories manually when developing your PyApp.


##Adding More Objects
Each time you modify, add, or remove files in your PyApp, you have to install the PyApp again for the changes to become available.
For further development in the Q-Shell you have to get the API of your PyApp in the workflow engine context:

	p.application.getAPI('<yourpyapp>', context = q.enumerators.AppContext.WFE)

In the next sections cover the further creation of a PyApp.	