@metadata spaceorder=100
@metadata title=Release Notes PyLabs
@metadata tagstring=ReleaseNotes

[History]: #/ReleaseNotes/History
[pylabs209]: http://jira.incubaid.com/browse/PYLABS-209
[changeset1]: 


#PyLabs Release Notes

This section provides the Release Notes for PyLabs

##PyLabs 3.2


### Build 116
Resolve issue with confguring postgresql.

######BUGS   
[PYLABS-218](http://jira.incubaid.com/browse/PYLABS-218) 
The fix of Pylabs 213 prevents the sso from being installed. Fixed in [this changeset](https://bitbucket.org/despiegk/pylabs-core/changeset/7d2f18f7ad77).

### Build 115
Resolve sshkey issue in the CloudFS.

######BUGS   
[PYLABS-209](http://jira.incubaid.com/browse/PYLABS-209) 
CloudFS copy file fails due to changed ssh key. Fixed in [this changeset](https://bitbucket.org/despiegk/pylabs-core/changeset/9bac008aab85).


### Build 114
An urgent bugfix for a time-out problem on remote systems, and some major performance improvements.

######BUGS
[PYLABS-207](http://jira.incubaid.com/browse/PYLABS-207) 
Timeout on q.remote.system.process.execute( is not working (copy of aserver SSOBF-4359). Fixed in [this changeset](https://bitbucket.org/despiegk/pylabs-core/changeset/9bac008aab85).

######IMPROVEMENTS
Various performance improvements (no Jira tracking).  Fixed in the following changesets:
[changeset1](https://bitbucket.org/despiegk/pylabs-core/changeset/e2841cdad37b)
[changeset2](https://bitbucket.org/despiegk/pylabs-core/changeset/6127649774bf)
[changeset3](https://bitbucket.org/despiegk/pylabs-core/changeset/a24ba0a67025)
[changeset4](https://bitbucket.org/despiegk/pylabs-core/changeset/945eba1c4983)
[changeset5](https://bitbucket.org/despiegk/pylabs-core/changeset/f8f0c0499222)





[Previous Releases (empty)][History]
