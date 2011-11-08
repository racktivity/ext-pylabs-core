@metadata title=Root Object

[drp]: #/Pylabs50/Architecture
[arakoon]: http://www.arakoon.org


###Root Object
A Root Object is a logical entity of a PyApp, stored in the Pylabs [DRP][] (Datacenter Resource Planning), and more specific in [Arakoon][]. A Root Object consists of properties, complex properties, and references to other Root Objects.
A complex property, also referred to as 'model object', is for example a contact person in a company. The contact on its turn has its own properties.
For example a customer can have a name and address as properties, contacts as model objects, and references to other customers.