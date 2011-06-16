@metadata title=Message Tags
@metadata order=20
@metadata tagstring=tag message

# Message Tags

There are two types of tag formats, labels and tags.

Labels are represented simply with a string:

    Label

Tags on the other hand, are in a key & value format separated with a colon: 

    Key:Value


## Reserved Tags

The two reserved tags are:

* *agent:* GUID.
* *application:* GUID.

Of course physically, they are all strings.


## Allowed Characters

The allowed characters are listed below:

* 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
* a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z
* A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z
* -
* _

[[note]]
**Note** 
Other characters are allowed in the value field yet will not be displayed properly. These characters are: , ; ? ! # $ % ^ & * ( ) [ ] { } '
[[/note]]


## Example

First, let's get a tag object:

    tagobject = q.base.tags.getObject()

Now let's set a label to it:

    tagobject.labelSet('ForTesting')

Let's also set a tag to it:

    tagobject.tagSet('Key', 'Value')

Finally, let's check what the tag string looks like:

    In [1]: tagobject.tagstring
    Out[1]: 'ForTesting Key:Value'
