Title: New nightly with support for dates in new CheckEventLog
Author: mickem
Tags: eventlog, filter, sql, status
Status: published

Hello. A new nightly build will be out tomorrow morning (don't think I
have time to build it before bedtime tonight). It will feature support
for date/time in the new CheckEventLog. Dates are handled somewhat
differently from before, but more "logical" I hope. Dates are specified
like so:

     generated gt -2d 

This means event record was generated more recently then "2 days ago".
In other words ''''generated &gt; (now - 2 days)''''. You can of course
also specify ''''generated gt 2d'''' which means records generated "in
the future" (not very sensible really) but for consistency I think this
is much better then "having them then other way around". This can be
combined with the usual AND/OR expressions I mentioned earlier.

     generated gt -2d AND severity = 'error' 

The above means all records from the last 2 days which has severity
error. Anyways, expect this nightly build out early morning tomorrow.
The overall scheduling for the up-coming 0.3.9 release is RC sometimes
this week and unless something pops up a release set for next 2 weeks or
so. // Michael Medin
