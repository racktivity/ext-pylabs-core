#!/usr/bin/env python2.6
from pylabs.InitBase import q, i
import optparse
parser = optparse.OptionParser()
parser.add_option('-n', '--name', dest='name', default='pylabs-core')
parser.add_option('-v', '--version', dest='version', default='')
parser.add_option('-d', '--domain', dest='domain', default='')
(options, args) = parser.parse_args()
i.qp.updateMetaDataForDomain()
pkg = q.qp.findNewest(name=options.name, domain=options.domain, maxversion=options.version)
pkg.prepareForUpdatingFiles()
pkg.checkout()
pkg.compile()
pkg.package()
domain = q.qp.getDomainObject(pkg.domain)
domain._ensureDomainCanBeUpdated()
domain.publish(commitMessage="Automatic build")
q.application.stop()
