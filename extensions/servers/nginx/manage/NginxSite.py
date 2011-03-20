from pylabs import q
from pylabs.baseclasses.CMDBSubObject import CMDBSubObject

from Cheetah.Template import Template as CheetahTemplate

#Default template for an nginx site (location)
SiteTemplate = CheetahTemplate.compile(source="""
        location $location {
          #for $key, $value in $options.iteritems()
          $key    $value;
          #end for
        }
""")

class NginxSite(CMDBSubObject):
    """
    Class which is responsible for the configuration of 1 Nginx site
    """
    name = q.basetype.string(doc="The name of the site", allow_none=True)
    location = q.basetype.string(doc="location of the site files")
    options = q.basetype.dictionary(doc="site specific options", default=dict())

    # Overload this attribute if you wish to use your own template
    template = SiteTemplate

    def __init__(self, name, location):
        CMDBSubObject.__init__(self)
        self.name = name
        self.location = location

    def addOption(self, key, value):
        """
        Add an option to Site Configuration
        
        @param key: Key name of the option to add
        @type key: string
        @param value: Value of the option to add
        @type value: list
        @raise KeyError if key with the same name already exists
        """
        if key in self.options.keys():
            raise KeyError('Option [%s] already exists' % key)
        self.options[key] = ' '.join(set(value))

    def removeOption(self, key):
        """
        Remove an Option
        
        @param key: Key name of the option to remove
        @type key: string
        @raise KeyError: if key not found in options dict
        """
        del self.options[key]

    def pm_getTemplateContext(self):
        """
        Get the template context for this class.

        Overload this method if you wish to use custom variables in your template.

        @return: the template context for this site
        @rtype: dict
        """
        return {
            "name": self.name,
            "location": self.location,
            "options": self.options,
        }

    def pm_getConfig(self):
        """
        Get the configuration for this site

        @return: configuration for this site
        @rtype: string
        """
        context = self.pm_getTemplateContext()
        return str(self.template(searchList=[context]))

