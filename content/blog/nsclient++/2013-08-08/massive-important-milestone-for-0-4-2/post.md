Title: Massive important milestone for 0.4.2
Author: mickem
Tags: 0.4.2, release-candidate
Status: published

Thought I'd let everyone know that I have in fact not been ignoring the
project lately. And the reason I have not been active on the support
side is that I have been working rather hard on something I anticipated
would take a few days but instead took weeks and weeks to finish. The
new simplified filters are now working for existing checks: This means I
can now do:

     check_drivesize C: > 217776967680|'C: used'=202G;178;201 'C: used %'=90%;79;89 'D: used'=366G;372;419 'D: used %'=78%;79;89 'E: used'=0B;0;0 'F: used'=0B;0;0 'G: used'=99G;745;838 'G: used %'=10%;80;90 

What this does underneath is:

     check_drivesize drive=* "warn=used > 80%" "crit=used > 90%" 

The first neat things is that drive and filter now replaces the
multitude of options we had before which was CheckAll, CheckAllOthers.
If I want to convert a CHeckAllOthers check:

     CheckDriveSize Drive=e: Drive=x: Drive=g: CheckAllOthers check_drivesize "filter=drive not in ('E', 'X', 'G')" 

Same thing for types:

     CheckDriveSize CheckAll FilterType=FIXED FilterType=REMOTE check_drivesize "filter=type not in ('FIXED', 'REMOTE')" 

But it also means you can do other neat things like removing all "small
drives":

     check_drivesize "filter=size < 5G" 

When it comes to check bounds a myrrriad (MaxWarnFree, MaxCritFree,
MinWarnFree, MinCritFree, MaxWarnUsed, MaxCritUsed, MinWarnUsed,
MinCritUsed, MaxWarn, MaxCrit, MinWarn, MinCrit) of bounds before which
are all down to two now.

     CheckDriveSize MinWarn=50% MinCrit=25% CheckAll check_drivesize "warn=used < 50%" "crit=crit < 50%" 

But you can also do more advanced things like:

     check_drivesize "warn=( used < 50% OR free > 80% ) AND type NOT IN ('FIXED') AND name NOT LIKE 'my-ignored-volum'" 

'''The old ways''' As you can see this is pretty systematic so
converting old checks to arguments is something which is planned and
will be implemented fairly soon. But there will be some snags such as
having multiple CheckWarnFree wont work or similar things. But I think
for 90% of the people out there the conversion layer will be sufficient
for you not to notice this change. '''Whats next''' Looking at the
future having this done means in a week or so I will release the first
alpha version of 0.4.2. At the same time I will start modernizing the
checks (something I have already started). But I needed the new filters
to support the old things first. // Michael Medin
