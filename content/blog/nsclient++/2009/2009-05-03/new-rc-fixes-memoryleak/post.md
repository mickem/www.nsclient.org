Title: New RC fixes memoryleak!
Author: mickem
Tags: memory-leak, release-candidate
Status: published

Hello everyone. I have for the past few weeks been trying to track down
a memory leak which has been plaguing me for some time now. And after
spending literal hundreds of hours looking over everything trying
various simulations and what not I found it. And felt pretty silly as I
have suspected that function (and looked at it) for quite some time. I
think I shall create a RAII wrapper for the arrayBuffer to prevent such
issues in the future. Anyways, there are a few other things as well but
nothing dramatic but a memory leak is always worth an upgrade! I shall
fix the last few bits and pieces with the installer and then release the
new version so expect that in the coming week or so. Yes, yes I know I
have said so for quite some time but I wanted to fix this darn memory
leak and it really took a long time to find... // Michael Medin
