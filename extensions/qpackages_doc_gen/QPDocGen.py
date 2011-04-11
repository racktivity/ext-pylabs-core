from pylabs import q
from Cheetah.Template import Template

class QPDocGen(object):

    _templatePath = q.system.fs.joinPaths(q.dirs.appDir, 'qpackages_doc_generator', 'templates', 'alkira_qp_template.tmpl')
    _taskletTemplatePath = q.system.fs.joinPaths(q.dirs.appDir, 'qpackages_doc_generator', 'templates', 'alkira_qp_tasklet_template.tmpl')

    def _writeFromTemplate(self, templatePath, params, destPath):
        template = Template(q.system.fs.fileGetContents(templatePath), params)
        contents = str(template)
        q.system.fs.writeFile(destPath, contents)

    def _getQPackageConfig(self, arg, path):
        packageName = q.system.fs.getBaseName(path)

        if not packageName.startswith('.hg'):
            versionPaths = q.system.fswalker.find(path, includeFolders=True, recursive=False) 

            for versionPath in versionPaths:
                version = q.system.fs.getBaseName(versionPath)

                q.logger.log('Gathering %s %s metadata.' %(packageName, version), dontprint=True)
                configFilePaths = q.system.fswalker.find(versionPath, pathRegexIncludes=['.cfg'])
                for configFilePath in configFilePaths:
                    configFile = q.tools.inifile.open(configFilePath)
                    configDict = configFile.getSectionAsDict('main')

                    dependenciesList = []
                    configSections = configFile.getSections()
                    for section in configSections:
                        if section.startswith('dep_'):
                            dep_name = section.strip('dep_')
                            dependenciesList.append(dep_name) 
                    dependenciesDict = {packageName: {version: dependenciesList}}

                q.logger.log('Gathering %s %s description files.' %(packageName, version), dontprint=True)
                fileDict = {}
                descriptionFilePaths = q.system.fswalker.find(versionPath, pathRegexIncludes=['.wiki', '.md', '.txt'])
                for descriptionFilePath in descriptionFilePaths:
                    descriptionFile = file(descriptionFilePath)
                    fileContent = descriptionFile.read()
                    descriptionFile.close()
                    fileName = q.system.fs.getBaseName(descriptionFilePath)
                    fileDict.update({fileName: fileContent})
                descriptionDict = {packageName: {version: fileDict}}

                q.logger.log('Gathering %s %s tasklet information.' %(packageName, version), dontprint=True)
                taskletDict = {}
                taskletsDir = q.system.fs.joinPaths(versionPath, 'tasklets')
                taskletsPath = q.system.fswalker.find(versionPath, pathRegexIncludes=['.py'])
                for taskletPath in taskletsPath:
                    taskletFile = file(taskletPath)
                    content = taskletFile.read()
                    taskletFile.close()
                    taskletName = q.system.fs.getBaseName(taskletPath)
                    taskletDict.update({taskletName: content})

                outputPath = q.system.fs.joinPaths(arg['outputPath'], packageName, version)
                if not q.system.fs.isDir(outputPath):
                    q.system.fs.createDir(outputPath)

                q.logger.log('Generating %s version %s documentation.' %(packageName, version), level=2)

                self._writeFromTemplate(self._templatePath, {'packageName': packageName, 'version': version, 'metadata': configDict, 'descriptionFiles': descriptionDict, 'dependenciesDict': dependenciesDict}, q.system.fs.joinPaths(outputPath, '%s_%s.md'%(packageName, version)))

                q.logger.log('Generating %s version %s tasklets documentation.' %(packageName, version), level=2)

                self._writeFromTemplate(self._taskletTemplatePath, {'packageName': packageName, 'version': version, 'tasklets': taskletDict}, q.system.fs.joinPaths(outputPath, '%s_%s_tasklets.md'%(packageName, version)))

    def cloneMetaDataRepo(self, repoUrl, repoUsername, repoPassword, localRepoPath):
        """
        Clones a given repository to a certain desitination.

        @type repoUrl: String
        @param repoUrl: The URL of the repository you want to clone.

        @type repoUsername: String
        @param repoUsername: The username to access the repository.

        @type repoPassword: String
        @param repoPassword: The password to access the repository.

        @type localRepoPath: String
        @param localRepoPath: The destination path where you want the repository to get cloned to. If the path does not exist, it will be created.
        """
        q.clients.hg.clone(repoUrl, repoUsername, repoPassword, destination=localRepoPath, noUpdate=False)

    def generateDocumentation(self, clonedRepoPath, outputPath):
        """
        Produces Q-Package metadata documentation in Markdown format.

        @type clonedRepoPath: String
        @param clonedRepoPath: The path where you cloned the repo (using cloneMetadataRepo).

        @type outputPath: String
        @param outputPath: The path where you want the documentation to be generated in.
        """
        q.system.fswalker.walk(clonedRepoPath, callback=self._getQPackageConfig, arg={'outputPath': outputPath}, includeFolders=True, recursive=False)

    def _publishMainPage(self, space, name, filesLocation, client_object):
        main_content = '#Q-Packages\n'
        page_list = q.system.fswalker.find(filesLocation, recursive=False, includeFolders=True)
        
        for page in page_list:
            qpName = q.system.fs.getBaseName(page)
            main_content += "\n* [%s](/#/%s/%s)"%(qpName.replace('_', '\_'), space, qpName)

        client_object.createPage(space, name, main_content)

    def _generateDocs(self, arg, path):
        qpName = q.system.fs.getBaseName(path)
        versionPaths = q.system.fswalker.find(path, includeFolders=True, recursive=False)
        content = "#%s Versions\n"%qpName.capitalize().replace('_', '\_')

        for versionPath in versionPaths:
            version = q.system.fs.getBaseName(versionPath)
            q.logger.log('Publishing: %s, Version: %s' %(qpName, version), level=2)
            qpVersion = "%s_%s"%(qpName, version)
            content += "\n* [%s %s](/#/%s/%s)"%(qpName.replace('_', '\_'), version.replace('_', '\_'), arg['space'], qpVersion)
            if not arg['client'].pageExists(arg['space'], qpName):
                arg['client'].createPage(arg['space'], qpName, content, parent=arg['name'])
            else:
                arg['client'].updatePage(arg['space'], qpName, content=content)

            mdFilePaths = q.system.fswalker.find(versionPath, pathRegexExcludes=['tasklets'])

            for mdFilePath in mdFilePaths:
                arg['client'].createPage(arg['space'], qpVersion, mdFilePath, parent=qpName, contentIsFilePath=True)

            mdTaskletPaths = q.system.fswalker.find(versionPath, pathRegexIncludes=['tasklets'])

            for mdTaskletPath in mdTaskletPaths:
                taskletVersion = q.system.fs.getBaseName(mdTaskletPath).split('.md')[0]
                parent_page = arg['client'].getPage(arg['space'], qpVersion)
                parent_page.content += "\n### Tasklets\n\n* [%s Tasklets](/#/%s/%s)"%(qpVersion.replace('_', '\_'), arg['space'], taskletVersion)
                arg['client'].connection.page.save(parent_page)
                arg['client'].createPage(arg['space'], taskletVersion, mdTaskletPath, parent=qpVersion, contentIsFilePath=True)

    def publishDocsToAlkira(self, space, name, filesLocation, hostname='127.0.0.1'):
        """
        Publishes the Q-Package documentation to Alkira.

        @type space: String
        @param space: The name of the space on Alkira. If it doesn't exist, it gets created.

        @type name: String
        @param name: The name of the page where all the Q-Packages will be listed.

        @type filesLocation: String
        @param filesLocation: The lcoation where the documentation files where generated (using generateDocumentation).

        @type hostname: String
        @param hostname: The IP that the Alkira Client will use to get a connection and add the pages. Default is localhost.
        """
        alkira_client = q.clients.alkira.getClient(hostname)
        self._publishMainPage(space, name, filesLocation, alkira_client)
        q.system.fswalker.walk(filesLocation, callback=self._generateDocs, arg={'space': space, 'name': name, 'client': alkira_client}, includeFolders=True, recursive=False)
