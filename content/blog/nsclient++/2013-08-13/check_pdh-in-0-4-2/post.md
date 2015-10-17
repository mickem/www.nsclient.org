Title: check_pdh in 0.4.2
Author: mickem
Tags: 0.4.2, check_pdh
Status: published

Performance counters are troublesome but they are also one of the best
ways to monitor systems and applications in Windows. Much of the
difficult with performance counters (PDH) come from the fact that they
are localized. In build 102 of 0.4.1 we added support for "English
counters" this has also been added to 0.4.2 but there have been many
other additions and enhancments as well. And we have also removed PDH
from all system checks so in the event that performance counters do not
work (which is common) all check\_xxx will still work with 0.4.2. But to
briefly describe how check\_pdh have evolved in 0.4.2 it has (as all
other commands) gotten the new syntax as well as filters. This means we
can do:

     check_pdh help help-csv Show help screen as a comma separated list. This is useful for parsing the output in scripts and generate documentation etc debug Show debugging information in the log filter=ARG Filter which marks interesting items. Interesting items are items which will be included in the check. They do not denote warning or critical state but they are checked use this to filter out unwanted items. warning=ARG Filter which marks items which generates a warning state. If anything matches this filter the return status will be escalated to warning. warn=ARG Short alias for warning critical=ARG Filter which marks items which generates a critical state. If anything matches this filter the return status will be escalated to critical. crit=ARG Short alias for critical. ok=ARG Filter which marks items which generates an ok state. If anything matches this any previous state for this item will be reset to ok. empty-syntax=ARG Message to display when nothing matched filter. If no filter is specified this will never happen unless the file is empty. Default value: empty-syntax=No matches ... 

Unfortunately there are no defaults since that would not make sense so
you cannot like with most other commands run "check\_pdh" to get a
sensible check since there is no way to know which counter you want to
check. The least we need is: \* counter to specify which counter to
check \* warn or crit to specify the boundaries to check A simple
counter looks like this:

     check_pdh "counter=SystemSystem Up Time" "warn=value > 5" "crit=value > 9999" SystemSystem Up Time = 204213 'SystemSystem Up Time value'=204213;5;9999 

Notice that I have a Swedish locale yet the English counter works since
NSClient++ now loads them as well. We can of course use indexes as well
if we specify the expand-index option.

     check_pdh "counter=430" "warn=value > 5" "crit=value > 9999" expand-index Everything looks good 'MinneDedikationsgräns value'=-2147483648;5;9999 

As you can see this means we get the actual counter value back which is
rather neat right? And as you can see I have a Swedish locale so I get
it back in Swedish (the English translation would be MemoryCommit
Limit). If we don't want this behavior we can drop the expand-indexes
option and instead get:

     check_pdh "counter=430" "warn=value > 5" "crit=value > 9999" Everything looks good '430 value'=-2147483648;5;9999 

Now if you have been reading the text you will be thinking wait...
memory commit limit -214??? How can it be minus? This is easily
explained and allows me to show case a new option: The default format is
"long" (which is a signed 32bit number). My machine has a lot more
memory so we need a bigger variable which can be changed using the type
option like so:

     check_pdh "counter=430" "warn=value > 5" "crit=value > 9999" flags=nocap100 expand-index type=large MinneDedikationsgräns = 25729224704 'MinneDedikationsgräns value'=25729224704;5;9999 

Which looks much better there are a few other options as well you can
use such as noscale and nocap100 and so on and so forth be sure to check
the help for details. The last ting I wanted to mention is that there is
another feature which technically is in 0.4.1 but not really visible.
And that is the ability to define counters and have them polled
periodically so you can grab averages and such. For this we need to
configure the counter so it can be polled periodically:

     [/settings/system/windows/counters/foo] collection strategy=rrd type=large counter=counter=Processor(_total)% Processor Time 

The next thing we need to do is simply specify the "alias" (foo int his
case) when we execute check\_pdh:

     check_pdh "counter=foo" "warn=value > 80" "crit=value > 90" Everything looks good 'foo value'=18;80;90 

What we get now is the actual last value to get calculated averages we
need to specify a time as well like so:

     check_pdh "counter=foo" "warn=value > 80" "crit=value > 90" time=30s Everything looks good 'foo value'=3;80;90 

Which means we have no created a poor-mans version of check\_cpu. But
given that this is actually exactly how it is implemented in 0.4.1 I
don't think it is that poor! That's all for now, and for the ones who
keep up to date on my talks I usually talk about real-time monitoring
which I have not touched upon here at all but that will come before
0.4.2 is released Next up is a modernized version of check\_proc and
check\_service... // Michael Medin
