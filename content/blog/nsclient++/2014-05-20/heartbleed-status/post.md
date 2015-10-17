Title: Heartbleed status
Author: mickem
Tags: heartbleed, security
Status: published

![heartbleed](/images/blog/heartbleed_f_improf_185x188.png) So
sorry but I forgot to post this update a few weeks ago but unfortunetly
as I have tried to say work is really crazy right now.\
 Anyways NSClient++ **0.4.1** and **0.4.2** **was affected by
Heartbleed**. 0.4.2 was patched about a week after the incident and
0.4.1 took a bit longer as I did not have a build environment setup for
that. But I forgot to post information about this. When it comes to
earlier versions like **0.3.x** they **are not** using the openssl
versions **affected by heartbleed**.

I am planning to start using DLLs to allow third party patching of
dependency libraries in the future so this will hopefully go into 0.4.3.
This means that security issues in thirdparty modules can be patched
manually.

**Anyways, everyone should upgrade to 0.4.1.105 and 0.4.2.93.**

If you do not want to make an upgrade or a re-install you can always
unzip the zip and drop-in the various XXXServer.dll (and technically
client) files into the modules folder. Usually it is only NRPEServer
which is used but all servers support SSL and use the same openssl
version so if you were to enable SSL on check\_nt that would also be
susceptible. So I would recomend replacing all (NSClientServer.dll,
NRPEServer.dll CheckMKServer.dll)

So once again: Please upgrade to 0.4.1.105 and 0.4.2.93 or stay on 0.3.9
if you are on the older version.
