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


###Setting Variables

