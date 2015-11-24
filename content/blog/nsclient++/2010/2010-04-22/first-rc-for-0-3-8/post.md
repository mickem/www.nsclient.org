Title: First RC for 0.3.8
Author: mickem
Tags: 0.3.8, release-candidate
Status: published

Hello everyone. Time for a RC:s for the up-coming 0.3.8 so please try it
out and let me know. I will try to post a note later on with the
cumulative updates but for now you will see whats new in this version
only.

     2010-04-21 MickeM - 0.3.8 RC1 + Added support for strings and int (values) to CheckSingleRegEntry Use like so (int): CheckSingleRegEntry path=HKEY_LOCAL_MACHINESYSTEMCurrentControlSetserviceseventlogApplicationMaxSize "syntax=%path%: %int%" warn==20971520 crit==20971520 check=int ShowAll=long CheckSingleRegEntry path=HKEY_LOCAL_MACHINESYSTEMCurrentControlSetserviceseventlogApplicationMaxSize "syntax=%path%: %int%" warn==30971520 crit==30971520 check=int ShowAll=long Use like so (string): CheckSingleRegEntry path=HKEY_LOCAL_MACHINESYSTEMCurrentControlSetserviceseventlogApplicationMaxSize "syntax=%path%: %string%" warn==20971520 crit==20971520 check=string ShowAll=long CheckSingleRegEntry path=HKEY_LOCAL_MACHINESYSTEMCurrentControlSetserviceseventlogApplicationMaxSize "syntax=%path%: %string%" warn==30971520 crit==30971520 check=string ShowAll=long This can ofcourse be combined and all valid operators (like regexp, substr, lt, gt, ne etc etc are supported. 

// Michael Medin
