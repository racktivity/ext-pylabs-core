from pylabs import q
from pylabs.baseclasses.CMDBSubObject import CMDBSubObject

from Cheetah.Template import Template as CheetahTemplate

#Default template for an nginx site (location)
SiteTemplate = CheetahTemplate.compile(source="""
        location $location {
          #for $option in $options
          $option[0]    $option[1];
          #end for
        }
""")

class NginxSite(CMDBSubObject):
    """
    Class which is responsible for the configuration of 1 Nginx site
    """
    name = q.basetype.string(doc="The name of the site", allow_none=True)
    location = q.basetype.string(doc="location of the site files")
    options = q.basetype.list(doc="site specific options", default=list())

    # Overload this attribute if you wish to use your own template
    template = SiteTemplate

    def __init__(self, name, location):
        CMDBSubObject.__init__(self)
        self.name = name
        self.location = location

    def addOption(self, option_type, option_settings):
        """
        Add an option to Site Configuration
        
        @param option_type: Name of the option to add
        @type option_type: string
        @param option_settings: Settings of the option to add
        @type option_settings: string
        @raise KeyError if key with the same tuple of (option_type, option_settings) already exists
        """
        option = (option_type, option_settings)
        if option in self.options:
            raise KeyError('Option tuple already exists')
        self.options.append(option)

    def removeOption(self, option_type, option_settings):
        """
        Remove an Option
        
        @param option_type: Name of the option to remove
        @type option_type: string
        @param option_settings: Settings of the option to add
        @type option_settings: string
        @raise KeyError: if option tuple (option_type, option_settings) not found in options dict
        """
        self.options.remove((option_type, option_settings))

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

