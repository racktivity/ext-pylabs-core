@metadata title=Generate API Documentation
@metadata tagstring=generate cloud api doc pydoc confluence alkira

# How to Generate the Cloud API Documentation

With the addition of the Alkira wiki, there are two types of documentation that can be generated:

* Confluence format.
* Alkira format.

## Step 1: Installing the Extension

To generate and publish either documentation formats, you need to have the 'cloud_api_generator' Q-Package. This can be obtained by running the Q-Shell and doing the following:

* Find the extension:

[[code]]
i.qp.find('cloud_api_generator')
[[/code]]

[[note]]
**Note** 

If there are multiple versions, you will be asked to choose one. Latest tested version is 3.1.6.
[[/note]]

* Installing the Q-Package:

[[code]]
i.qp.lastPackage.install()
[[/code]]

## Step 2: Checking  the SSO Specifications

* First, you need to get the cloud API specifications from mercurial. To do this run the command below:

[[code]]
q.generator.cloudapi.checkoutSpecs(login='login_name', password='password')
[[/code]]

[[note]]
**Note**

The default directory where the SSO specifications are checked out is:

    /opt/qbase5/tmp/ssospecs

If you would like to change this directory, you need to execute the checkoutSpecs method with an extra parameter, which is 'destination'.

    q.generator.cloudapi.checkoutSpecs(destination='your_destination', login='login_name', password='password')  

[[/note]]


## Step 3: Generate the Specifications

Here is where the documentation format is decided, read the section relative to the format that you need.

[[note]]
**Note**
The generator will search in the default directory `/opt/qbase5/tmp/ssospecs`.

If you used the checkOutSpecs function with a custom destination and you didn't not stop the Q-Shell and no errors were produced, all paths will be set correctly.

Once you finish the generating method and restart the Q-Shell, you need to return the three paths that were changed back to their original value:

* baseSpecDir:

[[code]]
q.generator.cloudapi.baseSpecDir = '/opt/qbase5/var/tmp/bla/ssospecs'
[[/code]]

* specDir:

[[code]]
q.generator.cloudapi.specDir = '/opt/qbase5/var/tmp/bla/ssospecs/1.1/codepackages/Actions_Interface_Rootobject'
[[/code]]

* specDirActors:

[[code]]
q.generator.cloudapi.specDirActors = '/opt/qbase5/var/tmp/bla/ssospecs/1.1/codepackages/Actions_Interface_Actor'
[[/code]]

[[/note]]

The generated content can be found under the following directories:

* *Documentation:* `/opt/qbase5/apps/cloud_api_generator/doc`
* *CloudAPI Client:* `/opt/qbase5/apps/cloud_api_generator/generatedClient`
* *CloudAPI Server:* `/opt/qbase5/apps/cloud_api_generator/generatedServer`


### Alkira Format

To generate the specifications in Alkira format, run the generateAll method with 'documentationFormat='alkira':

[[code]]
q.generator.cloudapi.generateAll(documentationFormat='alkira')
[[code]]


### Confluence Format

To generate the specifications in Confluence format, run the generateAll method with 'documentationFormat='confluence':

[[code]]
q.generator.cloudapi.generateAll(documentationFormat='confluence')
[[code]]


## Publish the Specification

You can publish the generated specification on either Confluence or Alkira. Read the section relative to your requirement.

### Alkira

[[warning]]
**Warning** 
The Alkira Client has not been packaged yet, running the steps below will yield nothing.
[[/warning]]

To publish the documentation on Alkira, you need to insure that the Alkira client is installed. You can do this as follows:

* Find the 'alkira_client_extension' Q-Package:

[[code]]
i.qp.find('alkira_client_extension')
[[/code]]

* Choose the desired version *if* multipies are found, then install the Q-Package:

[[code]]
i.qp.lastPackage.install()
[[/code]]

Once you have the client, you can publish the documentation using the command below:

[[code]]
q.generator.cloudapi.publishToAlkira(space, main_page='Cloud API Documentation', parent_name=None, hostname='127.0.0.1')
[[/code]]

Where:

* *space:* is the name of the space.
* *main_page:* is the name of the page.
* *parent_name:* is the name of a parent page in case you want the documentation page to be a child of it.
* *hostname:* is the IP that the Alkira Client will use to get a connection and add the pages.


### Confluence

To publish the documentation on Confluence, you need to insure that the confluence client is installed. You can do this as follows:

* Find the 'confluence_client_extension' Q-Package:

[[code]]
i.qp.find('confluence_client_extension')
[[/code]]

* Choose the desired version *if* multipies are found, then install the Q-Package:

[[code]]
i.qp.lastPackage.install()
[[/code]]

Once you have the client, you can publish the documentation using the command below:

[[code]]
q.generator.cloudapi.publishDocumentation(confluenceUri, login, password, space, parentpage)
[[/code]]

Where:

* *confluenceUri:* is the Confluence server IP address and DNS name.
* *login:* is your Confluence login.
* *password:* is your Confluence password.
* *space:* is the name of the space on which the pages should be published.
* *parentpage:* is the parent page of the pages that shall be created.
