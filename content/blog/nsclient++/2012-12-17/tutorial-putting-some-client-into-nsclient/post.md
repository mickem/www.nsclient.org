Title: [TUTORIAL] Putting some client into NSClient++
Author: mickem
Tags: cli, nrpe, nsca, tutorial
Status: published

I have posted yet another tutorial this time on using hte client
interface to both use NSClient++ as a client but also how to create
various forms of proxies and such as well as accessing the clients from
scripts. ''NSClient++ despite its name is most often used in server mode
responding to remote calls via either NRPE or check\_nt. The closest
thing to a client we get in normal mode of operation is NSCA where we
submit data back. But NSClient++ can act as a client as well which is
not just something I use for unit testing but something which can
actually be useful in your monitoring environment. A good example of a
really useful feature is creating a proxy or use NSClient++ as proxies
to add intelligence (see my post earlier on writing stateful scripts
Enhance your monitoring with stateful scripts).'' You can find the post
here
\[http://blog.medin.name/2012/12/16/putting-some-client-into-nsclient/\]
