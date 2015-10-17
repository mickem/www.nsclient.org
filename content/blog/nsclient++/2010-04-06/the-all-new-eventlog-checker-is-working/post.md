Title: The all-new eventlog checker is working!
Author: mickem
Tags: eventlog, filter, sql, status
Status: published

Hello everyone (and that is you Google index bot!) '''News''' Today I
can announce the first ever all-new EventLog check working on my
development machine. It was (actually) much much harder to make this
then I had initially anticipated and halfway through I almost gave up.
The checkin (in a few days or so) will be around 2000 lines of code
(thats around 10% of NSClient++) so it was a pretty long haul. Given the
complexity I think this will be in beta for a while but I really think
the new syntax will be pretty awesome! '''How it works''' The check I
run today looks like so:

     CheckEventLog debug=true file=application file=system MaxWarn=1 MaxCrit=1 "filter=severity = 1" truncate=1023 unique descriptions "syntax=%severity%: %source%: %message% (%count%)" 

Most of the options are the "same old": \* debug=true Enable debugging
(something I always do when I develop things :) \* file=application /
system What to check \* MaxWarn/MaxCrit When it is bad/worse \* truncate
Make sure it fits \* unique Keep the result minimal (ie. don't report
multiple items) \* descriptions This might be removed as it is sort of
superfluous but I am not sure yet. \* syntax Same old same old. '''And
here it comes'''

     "filter=severity = 1" 

\* filter Has a new meaning in this case saying report all messages with
a severity of 1 Changing this parameter to for instance:

     "filter=severity = 1 AND severity = 2" 

yields no results as severity cant be BOTH 1 and 2 at the same time
where as

     "filter=severity = 1 OR severity = 2" 

yields more results as we now have both 1 and 2 as allowed values. As
you can see the values are "numeric" at the moment but that will be
fixed a bit later on as I get all the conversion code ready. '''The
nitty gritty details''' Another interesting thing is how this works. The
expression is parsed into a tree which is "enhanced" in several passes.
If we look in the debug log we can see this:

     d CheckEventLog.cpp(648) Using: where 

Use the new "where" mode. '''Parsing'''

     d CheckEventLog.cpp(302) Parsing: severity = 1 OR severity = 2 AND 1='1' d CheckEventLog.cpp(310) Parsing succeeded: {tbd}op:or({tbd}op:=({tbd}:severity, {tbd}#1), {tbd}op:and({tbd}op:=({tbd}:severity, {tbd}#2), {tbd}op:=({tbd}#1, {tbd}'1'))) 

Expression was parsed into the tree. All the "tbd" here is the types
which at the moment are unknown which the parser will do next. '''Type
inference'''

     d CheckEventLog.cpp(318) Type resolution succeeded: {bool}op:or({bool}op:=({int}:severity, {int}#1), {bool}op:and({bool}op:=({int}:severity, {int}#2), {bool}op:=({int}#1, {int}fun:auto_convert({string}'1')))) 

Here we have looked up the types. '''Automatic conversion''' An
interesting point here is the

     {int}fun:auto_convert({string}'1') 

This phase discovered that an "int" was compared to a "string" and
"solved" this by converting the string to an int. '''Static
evaluation''' Next up is a static evaluation

     d CheckEventLog.cpp(326) Static evaluation succeeded: {bool}op:or({bool}op:=({int}:severity, {int}#1), {bool}op:and({bool}op:=({int}:severity, {int}#2), {bool}#1)) 

And as you can see here the function is removed and replaced by an
"boolean value" (true). Since the expression does not contain any
variables the static evaluation figures out it is pointless to do this
over and over and thus removes it. '''Variable Binding'''

     d CheckEventLog.cpp(334) Binding succeeded: {bool}op:or({bool}op:=({int}:severity, {int}#1), {bool}op:and({bool}op:=({int}:severity, {int}#2), {bool}#1)) 

Here we cant really see a difference since the bindings are not showed
but what has happen is that the filter is bound to the variables which
will contain the data. This is actually much faster than the old version
which did "string" comparisons for every check. Now it already knows
what it will do and just executes the code. I have yet to run any tests
on this but presumably a well written where clause will be faster then
the previous version. That is all for now good people you can expect
nightly builds with this functionality either this week or the next. //
Michael Medin
