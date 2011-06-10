[qpinstall]: /pylabsdoc/#/Q-Packages/QPInstall
[modeling]: /pylabsdoc/#/PyLabsApps/Modeling


# Pymodel﻿

The Pymodel extension is a powerful way to define, create and modify complex types.
This extension gives you the ability to browse your OSIS model's definitions that are categorized by their domain; you can also use many serializers to serialize/deserialize your objects to some formats. It is using thrift underneath.


## Required Q-Packages

To use this extension, you need to find and install the latest version of the Q-Package named 'pymodel'. As for the example that we will work with, the 'drpdb_model' Q-Package will also be needed.

If you are unfamiliar with how to install a Q-Package, please check the [Installing Q-Packages][qpinstall] page.


## Usage

The Pylabs model extension is hooked under `q.pymodel.` , so you can find your pymodels according to their namespace name.

## Example Model

As we have previously mentioned, insure that you have the 'drpdb_model' Q-Package installed.
Once you have the package, open your terminal and do the following:

* Create the 'drp' directory:

    mkdir -p /opt/qbase5/lib/pymonkey/models/drp

* Copy the desired files to that directory:

    cp /opt/qbase5/var/qpackages4/files/cloud.aserver.com/drpdb_model/3.1.6/generic/libexec/osis/* /opt/qbase5/lib/pymonkey/models/drp/


## Importing Domains

The default directory from which the models are loaded is `/opt/qbase5/lib/pymonkey/models/`. The models are loaded and grouped by their domains, which are the subdirectories under the base directory. For example all the models under `'/opt/qbase5/lib/pymonkey/models/drp'` , will be grouped under the 'drp' domain.

You can also import some domains on the fly without restarting the Q-Shell by calling:

    q.pymodel.importDomain('myDomain', '/opt/qbase5/lib/pymonkey/models/drp')

[[note]]
**Note** 
The domain that you import will be lost once you close your Q-Shell session.
[[/note]]


## Serializers

There are some serializers that help you to serialize/deserialize your objects, they are as following:
* XML Serializer
* YAML Serializer
* Thrift Serializer
* Thrift Base64 Serializer

[[tip]]
Here's a complete scenario for using the Pymodel extension.

* First, create an empty model object:
    
    model_object = q.pymodel.drp.lan.getEmptyModelObject()

* Returning a YAML serialized string:

    yaml_str = q.pymodel.drp.lan.object2YAML(model_object)

* Returning a Thrift Byte string:

    byte_str = q.pymodel.drp.lan.object2ThriftByteStr(model_object)

* Returning Thrift in base encoded string (can be used over XML-RPC):

    base64_str = q.pymodel.drp.lan.object2ThriftBase64Str(model_object)

* Serialized YAML, Thirft & Thirft Base but returned to a model with Thrift behind:

    model_object = q.pymodel.drp.lan.YAML2object(yaml_str)
    model_object = q.pymodel.drp.lan.thriftByteStr2object(byte_str)
    model_object = q.pymodel.drp.lan.thriftBase64Str2object(base64_str)
[[/tip]]

[[note]]
**Note** 
The XML serializer  does not allow the conversion of an empty object to XML.
[[/note]]


## How to Define a Model

See the [Modeling][modeling] chapter in the PyLabs Applications space.