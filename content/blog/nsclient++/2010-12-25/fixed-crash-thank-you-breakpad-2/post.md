Title: Fixed crash: Thank you breakpad!
Author: mickem
Tags: breakpad, crash, nightly
Status: published

Got some 300 dumps or so submitted on xmas so I went through them and
all were crashing on the same line! Which has been fixed in the latest
nightly build. It seems there was an issue with the new PDH counters
where I missed to initialize a variable to NULL. Crash pad analysis was
pretty straight forward. The dump looks like this:

     ... 6|0|CheckSystem.dll|memmove|F:ddvctoolscrt_bldSELF_64_AMD64crtsrcAMD64memcpy.asm|224|0x0 6|1|CheckSystem.dll|memcpy_s|f:ddvctoolscrt_bldself_64_amd64crtsrcmemcpy_s.c|67|0xa 6|2|CheckSystem.dll|std::basic_string,std::allocator >::assign(std::basic_string,std::allocator > const &,unsigned __int64,unsigned __int64)|c:program files (x86)microsoft visual studio 8vcincludexstring|1049|0x2c 6|3|CheckSystem.dll|PDH::PDHCounter::getName()|c:sourcenscpbranchesstableincludepdhcounters.hpp|75|0x26 6|4|CheckSystem.dll|PDHCollectors::RoundINTPDHBufferListenerImpl<__int64,PDHCollectors::PDHCounterNormalMutex>::get_name()|c:sourcenscpbranchesstableincludepdhcollectors.hpp|321|0x4 6|5|CheckSystem.dll|PDHCollectors::RoundINTPDHBufferListenerImpl<__int64,PDHCollectors::PDHCounterNormalMutex>::getAvrage(unsigned int)|c:sourcenscpbranchesstableincludepdhcollectors.hpp|298|0xf 6|6|ntdll.dll||||0x117287 6|7|CheckSystem.dll|wcstoxl|f:ddvctoolscrt_bldself_64_amd64crtsrcwcstol.c|141|0x7 6|8|KERNELBASE.dll||||0x10ab 6|9|KERNELBASE.dll||||0x10ab 6|10|CheckSystem.dll|PDHCollector::getCPUAvrage(std::basic_string,std::allocator >)|c:sourcenscpbranchesstablemoduleschecksystempdhcollector.cpp|269|0x1d ... 

With the offensive line being:
''6|3|CheckSystem.dll|PDH::PDHCounter::getName()|c:sourcenscpbranchesstableincludepdhcounters.hpp|75|0x26''
The problem (if we look at the code) was a bit perplexing actually:

     std::wstring get_name() const { if (parent_ != NULL) return parent_->getName(); return _T(""); } ... const std::wstring getName() const { return name_; } 

This looks solid enough right? Whats even worse is that it seems to work
fine on my box. So after digging around a bit I noticed this was NULL
"after the second call" meaning something is fishy but with a check for
NULL before the I was a bit puzzled until I noticed there was no default
assignment for the parent\_ pointer meaning in some rare cases when
performance counters was not working properly we would not get a valid
value which in conjunction with an problem in the counter would yield
this error. Anyways, to make a long story short: '''Thank you Google
breakpad and whomever sent in the crash report!''' Tomorrow I will write
up a quick tutorial/info page on how to enable crash report submissions
and how you can help out the development by submitting (manually if you
prefer) crash reports whenever you have a problem! // Michael Medin
