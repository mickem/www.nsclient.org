Title: New nightly build
Author: mickem
Tags: nightly
Status: published

New minor build with a new command: CheckSingleRegEntry Used for
checking registry entries (at the moment only existence) Scedule
postponed 1 week since the eventlog took a bit more time ten I had
anticipated and this weekend will be mountainbike weather!!! :)

     2010-04-16 MickeM + Added new Check to CheckSystem: CheckSingleRegEntry Similar to the previous CheckSIngleFile but can be used to check aspects of registry entries. CheckSingleRegEntry path=HKEY_LOCAL_MACHINESYSTEMCurrentControlSetserviceseventlogApplicationMaxSize "syntax=%path%: %exists%" warn==true crit==true check=exists ShowAll=long CheckSingleRegEntry path=HKEY_LOCAL_MACHINESYSTEMCurrentControlSetserviceseventlogApplicationMaxSizeYY "syntax=%path%: %exists%" warn==true crit==true check=exists ShowAll=long Currently only supports checking existanse of keys but more checks will be added soon. 2010-04-14 MickeM ! Fixed erroneous error message "Failed to peek buffer" 

// Michael Medin
