Title: I am not dead! :)
Author: mickem
Tags: eventlog, filter, sql, status
Status: published

Hello everyone, Sorry for being "off-line" last few weeks but I have
actually been working more diligently then usual. What I am working on
is a parser for defining filter expressions. The first use case for this
is the event log check but in the future this might be added to more
places. The syntax is similar to "SQL WHERE" Clauses so the following
will for instance be a valid check:

     CheckEventLog MaxWarn=1 MaxCrit=1 "filter=(id = 123 OR id = 321) AND (severity='warning' OR severity='error')" 

// Michael Medin
