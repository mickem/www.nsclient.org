Title: New nightly with the "new" event log checker
Author: mickem
Status: published

Hello, The eventlog checker code is now live in the latest nightly
build. You can try it wout using something along the lines of the
following:

     CheckEventLog debug=true file=application file=system MaxWarn=1 MaxCrit=1 "filter=severity = 'error' AND strings like 'SQLEXPRESS'" truncate=800 unique descriptions "syntax=%severity%: %source%: %strings% (%count%)" 

Most things are similar the "new" option is:
'''filter'''='''<where expression>''' where the <where expression> is
similar to a SQL where clause. operators supported are: =, !=, &gt;,
&lt;, &gt;=, &lt;=, eq, ne, gt, lt, ge, le, OR, AND, like keywords
supported: id, source, type, severity, message, strings, written,
generated Types supported: string, int, severity In pother words since
'''date''' is '''NOT''' supported you cant really use the written and
generated options since you have no way to specify "time" this will be
fixed next week. Same thing goes for type which cant (like severity)
parse strings into integers. But '''PLEASE''' try this out despite the
limitations as I would like some feedback on what kind of features you
would need and also find any bugs. // Michael Medin
