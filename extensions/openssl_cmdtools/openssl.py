from pylabs import q

class OpenSSL(object):
    _opensslexecutable = None

    def getOpensslExecutable(self):
        if self._opensslexecutable == None:
            if q.platform.isWindows():
                self._opensslexecutable = q.system.fs.joinPaths(q.dirs.baseDir,'bin','openssl.exe')
            else:
                self._opensslexecutable = q.system.fs.joinPaths(q.dirs.baseDir,'bin','openssl')
        return self._opensslexecutable

    def generateKey(self):
        key_file = q.system.fs.getTempFileName()
        try:
            q.system.process.execute("%s genrsa -out %s"%(self.getOpensslExecutable(), key_file))
            return q.system.fs.fileGetContents(key_file)
        finally:
            if q.system.fs.exists(key_file):
                q.system.fs.removeFile(key_file)

    def generateCertificateRequest(self, key, countrycode, state, organization, organizationalunit, commonname, configFile=None):
        key_file = q.system.fs.getTempFileName()
        try:
            q.system.fs.writeFile(key_file, key)
            cert_req_file = q.system.fs.getTempFileName()
            try:
                configFile = configFile or q.system.fs.joinPaths(q.dirs.extensionsDir, "openssl_cmdtools", "openssl.cnf")
                q.system.process.execute("%s req -new -key %s -out %s -batch -subj \"/C=%s/ST=%s/O=%s/OU=%s/CN=%s\" -config '%s'" \
                                         %(self.getOpensslExecutable(), key_file, cert_req_file, countrycode, state, organization, organizationalunit, commonname, configFile))
                return q.system.fs.fileGetContents(cert_req_file)
            finally:
                if q.system.fs.exists(cert_req_file):
                    q.system.fs.removeFile(cert_req_file)
        finally:
            if q.system.fs.exists(key_file):
                q.system.fs.removeFile(key_file)

    def generateCertificateAuthority(self, days, configFile, countrycode, state, organization, organizationalunit, commonname):
        certDir = q.system.fs.joinPaths(q.dirs.appDir, 'openvpn', 'keys')
        if not q.system.fs.exists(certDir):
            q.system.fs.createDir(certDir)
        keyfile = q.system.fs.joinPaths(certDir, 'ca.key')
        certfile = q.system.fs.joinPaths(certDir, 'ca.crt')
        q.system.process.execute("%s req -days %s -nodes -new -x509 -keyout %s -out %s -config %s -subj \"/C=%s/ST=%s/O=%s/OU=%s/CN=%s\"" % (self.getOpensslExecutable(), days, keyfile, certfile, configFile, countrycode, state, organization, organizationalunit, commonname))
        q.system.process.execute("chmod 0600 %s" % keyfile)

    def certificateAuthorityBuildKey(self, keyDir, days, configFile, commonName, countrycode, state, organization, organizationalunit):
        q.system.fs.changeDir(keyDir)
        q.system.process.execute("%s req -days %s -nodes -new -keyout %s.key -out %s.csr -config %s -subj \"/C=%s/ST=%s/O=%s/OU=%s/CN=%s\"" % (self.getOpensslExecutable(), days, commonName, commonName, configFile, countrycode, state, organization, organizationalunit, commonName))
        q.system.process.execute("%s ca -days %s -out %s.crt -in %s.csr -config %s -batch -subj \"/C=%s/ST=%s/O=%s/OU=%s/CN=%s\"" % (self.getOpensslExecutable(), days, commonName, commonName, configFile, countrycode, state, organization, organizationalunit, commonName))
        q.system.process.execute("chmod 0600 %s.key" % commonName)

    def certificateAuthorityBuildKeyServer(self, keyDir, days, configFile, commonName, countrycode, state, organization, organizationalunit):
        q.system.fs.changeDir(keyDir)
        q.system.process.execute("%s req -days %s -nodes -new -keyout %s.key -out %s.csr -extensions server -config %s -subj \"/C=%s/ST=%s/O=%s/OU=%s/CN=%s\"" % (self.getOpensslExecutable(), days, commonName, commonName, configFile, countrycode, state, organization, organizationalunit, commonName))
        q.system.process.execute("%s ca -days %s -out %s.crt -in %s.csr -extensions server -config %s -subj \"/C=%s/ST=%s/O=%s/OU=%s/CN=%s\" -batch" % (self.getOpensslExecutable(), days, commonName, commonName, configFile, countrycode, state, organization, organizationalunit, commonName))
        q.system.process.execute("chmod 0600 %s.key" % commonName)

    def createSelfSignedCertificate(self, key, cert_req, days):
        key_file = q.system.fs.getTempFileName()
        try:
            q.system.fs.writeFile(key_file, key)
            cert_req_file = q.system.fs.getTempFileName()
            try:
                q.system.fs.writeFile(cert_req_file, cert_req)
                cert_file = q.system.fs.getTempFileName()
                try:
                    q.system.process.execute("%s x509 -req -days %s -in %s -out %s -signkey %s"%(self.getOpensslExecutable(), days, cert_req_file, cert_file, key_file))
                    return q.system.fs.fileGetContents(cert_file)
                finally:
                    if q.system.fs.exists(cert_file):
                        q.system.fs.removeFile(cert_file)
            finally:
                if q.system.fs.exists(cert_req_file):
                    q.system.fs.removeFile(cert_req_file)
        finally:
            if q.system.fs.exists(key_file):
                q.system.fs.removeFile(key_file)

    def signCertificateRequest(self, cakey, cacert, cert_req, database, serial, configFile=None):
        cakey_file = q.system.fs.getTempFileName()
        try:
            q.system.fs.writeFile(cakey_file, cakey)
            cacert_file = q.system.fs.getTempFileName()
            try:
                q.system.fs.writeFile(cacert_file, cacert)
                cert_req_file = q.system.fs.getTempFileName()
                try:
                    q.system.fs.writeFile(cert_req_file, cert_req)
                    cert_file = q.system.fs.getTempFileName()
                    try:
                        tmpdir = q.system.fs.getTempFileName()
                        q.system.fs.createDir(tmpdir)
                        try:
                            configFile = configFile or q.system.fs.joinPaths(q.dirs.extensionsDir, "openssl_cmdtools", "openssl.cnf")
                            database_file = q.system.fs.joinPaths(tmpdir, "index.txt")
                            serial_file = q.system.fs.joinPaths(tmpdir, "serial")
                            q.system.fs.writeFile(database_file, database)
                            q.system.fs.writeFile(serial_file, serial)
                            q.system.process.execute("cd %s && %s ca -in %s -cert %s -keyfile %s -out %s -outdir . -config '%s' -batch"%(tmpdir, self.getOpensslExecutable(), cert_req_file, cacert_file, cakey_file, cert_file, configFile))
                            return q.system.fs.fileGetContents(cert_file), q.system.fs.fileGetContents(database_file), q.system.fs.fileGetContents(serial_file)
                        finally:
                            if q.system.fs.exists(tmpdir):
                                q.system.fs.removeDirTree(tmpdir)
                    finally:
                        if q.system.fs.exists(cert_file):
                            q.system.fs.removeFile(cert_file)
                finally:
                    if q.system.fs.exists(cert_req_file):
                        q.system.fs.removeFile(cert_req_file)
            finally:
                if q.system.fs.exists(cacert_file):
                    q.system.fs.removeFile(cacert_file)
        finally:
            if q.system.fs.exists(cakey_file):
                q.system.fs.removeFile(cakey_file)

    def revokeCertificate(self, configFile, certFilePath, revokeReasonCode):
        """
        Revoke a certificate
        @param configFile: openssl configuration file location
        @param certFilePath: certification file location
        @param revokeReasonCode: reason for revoking the certificate
        """
        cmd = '%s ca -config %s -revoke %s -crl_reason %s'%(self.getOpensslExecutable(),configFile, certFilePath, str(revokeReasonCode))
        exitCode, output = q.system.process.execute(cmd, outputToStdout = False, dieOnNonZeroExitCode=False)

        return exitCode

    def generateCRL(self, configFile, crlFile):
        """
        Generate CRL
        @param configFile: openssl configuration file location
        @param crlFile: CRL file
        """
        if not q.system.fs.isFile(crlFile):
            q.system.fs.createEmptyFile(crlFile)

        cmd = '%s ca -config %s -gencrl -out %s'%(self.getOpensslExecutable(), configFile, crlFile)
        exitCode, output = q.system.process.execute(cmd, outputToStdout = False)

        return exitCode

    def getCertificateStatus(self, configFile, certSerial):
        """
        Get the certificate status given the serial number
        @param configFile: openssl configuration file location
        @param certSerial: serial number of the certificate
        """
        cmd = '%s ca -status %s -config %s'%(self.getOpensslExecutable(), certSerial, configFile)
        exitcode, output, stderr = q.system.process.run(cmd, stopOnError=False)

        # For some reason, openssl commands return their interesting output via stderr.
        # In this case, we're interested in the second line (actual status), not the first line (config file used)
        return stderr.splitlines()[1]

    def checkCertificateStatus(self, configFile, certSerial, statusToCheck):
        """
        Check the status of the certificate
        @param configFile: openssl configuration file location
        @param certSerial: serial number of the certificate
        @param statusToCheck: status to check e.g Valid, Revoked
        """
        status = self.getCertificateStatus(configFile, certSerial)
        pattern = re.compile('[%s]'%statusToCheck)

        if pattern.search(status):
            return True

        return False