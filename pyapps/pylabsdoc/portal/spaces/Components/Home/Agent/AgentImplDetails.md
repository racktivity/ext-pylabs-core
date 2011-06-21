@metadata title=Implementation Details
@metadata tagstring=implementation


# Implementation Remarks Agent v4


* when executing cmd returns a unique nr (sort of jobnr for XMPP, is referred to tasknr in the implementation) does this by retunring JOBNR $jobnr

    ** nr is unique per agent

* every agent has a unique name or nr which is unique for domain


v3. Python version

* everything where no (*)

v3. C version
extra
* as small as possible in memory and disk footprint (*)
* crossplatform (*)
* xmpp communication  encrypted (*)
* ejabberd servers