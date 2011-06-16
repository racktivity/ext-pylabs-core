@metadata title=Check Out Mercurial Repo
@metadata tagstring=checkout mercurial repository


# How to Check Out a Mercurial Repository in PyLabs

To check out a mercurial repository in PyLabs, use this one-liner in the Q-Shell:

    p.clients.mercurial.getClient('checkoutdir', 'repo-location', 'branch')
    
For example:

    p.clients.mercurial.getClient(q.dirs.varDir+'mercurial', 'https://username:password@bitbucket.org/incubaid/pylabs-core', 'default')

        