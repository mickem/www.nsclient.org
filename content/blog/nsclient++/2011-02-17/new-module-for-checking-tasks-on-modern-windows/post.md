Title: New module for checking tasks on modern windows!
Author: mickem
Status: published

Hello, New module out with the latest nightly. It is called
CheckTaskSched2 and work the same as the new improved CheckTaskSched
with the one exception being that it utilizes the new API introduced
with Windows Vista. So if you run this on "modern windows" you should
enable that module instead of the old one. And if you run on previous
version of windows (NT/2k/xp) you should use the previous version of the
module. '''Changes'''

     2011-02-16 MickeM * Added new module CheckTaskSched2 which is the same as CheckTaskSched but designed for Vista and beyond. So if you want to check "new tasks" on modern Windows use this module instead of the CheckTaskSched mosule. They are exactly the same excep using different APIs (and somewhat different options) The CheckTaskSched2 is somewhat limited as the only supported keys are: title, exit_code, status, most_recent_run_time 2011-02-10 MickeM * Fixed issue with where filters and & operator * Added exact bounds to CheckTaskSched * Added conversion of status from string * Fixed time handling in CheckTaskSched to be "UTC" (hence the %most_recent_run_time% syntax string is also UTC) 
