#OSIS Views
As explained in the [PyApp architecture] (sampleapp.md/), OSIS is a Object Store and Indexing System. OSIS is responsible for populating the [Arakoon] (http://www.arakoon.org) object store as well as a PostgreSQL database.
In this section we will mainly talk about the PostgreSQL connection.

Since the Arakoon object store is not queryable, the retrieval of object would be too slow and thus not user-friendly. That's where the PostgreSQL database comes into play.
The PostgreSQL database is used to store different views on Root Objects. A view is a definition of what you want to see of a Root Object. This means that you can create multiple views on one Root Object. For example on a Root Object "Customer" you can create a view which contains only the name and guid of the customer, but another view can contain name, customer ID, postal code, and city. You have to find a good balance in the number of views that you create and the clarity of the views. Too many views make easily a mishmash of your directory, too little views make some operations less effective.

##Creating an OSIS View
An OSIS view is a [tasklet] (http://confluence.incubaid.com/display/PYLABS/Tasklets) which is stored in the directory `<pyapp name>/impl/setup/osis`. See the [PyApps Directory Structure] (sampleapp.md/) for more information about the location of the files.

###Import Libraries
A first thing to add to the OSIS view is the import of the `OsisDB` library:

    from osis.store.OsisDB import OsisDB

Import other libraries if necessary but that is not likely.


###Creating the View Name
A name for an OSIS view must be concise, but clear too. Therefore, we use at least the domain name and the root object name as name for the view.

    def main(q, i, params, tags):
        domain = 'mydomain'
        rootobject = 'myrootobject'
        appname = params['appname']
        view_name = '%s_view_%s_list' %(domain, rootobject)

Note that all variable names can be changed into names of your own choice.
For the `view_name` variable, it is highly recommended to use the domain and root object name in the name of your view list, and to optionally add some more specification to the name.

###Creating the OSIS View
To create an OSIS view, you need to connect to the OSIS database. Also verify if the view_name does not yet exist for the given domain and root object.

    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        ...

Once you have your OSIS connection, it takes you three steps to create the view:

1. Create a view-object, which is comparable with a table
2. Add the desired data to the view-object
3. Add the view to OSIS

    #create view object:
        view = connection.viewCreate(domain, rootobject, view_name)
    #add desired data
        view.setCol('name', q.enumerators.OsisType.STRING, True)
        view.setCol('code', q.enumerators.OsisType.STRING, True)
        view.setCol('customerguid', q.enumerators.OsisType.UUID, True)
        view.setCol('source', q.enumerators.OsisType.STRING, True)

        ...

    #add view to OSIS
        connection.viewAdd(view)

The `setCol`-method of the view object expects three arguments:

* name of a root object property, as defined in the Root Object Model
* type of the property
* boolean to indicate if the value may be null (True) or not (False)
