Title: Dotnet/C# goodness
Author: mickem
Tags: 0.4.0, dotnet
Status: published

Just a quick heads up to let people know I am actually doing something.
I got a bit of inspiration from someone asking about interfacing from
dotnet and thought: Well, why the heck not...

     ? NSClient++ 0,4,0,140 2012-02-22 x64 booting... ... d Loading plugin: DotnetPlugin d Using factory: NSCP.Plugin.PluginFactory for test.dll d About to load dotnet plugin: D:/source/nscp/build/x64//modules/dotnettest.dll d Plugin loaded: test.dll e Hello World from C# ... ? Enter command to inject or exit to terminate... check_dotnet d Injecting: check_dotnet... e Got command: check_dotnet/check_dotnet d Result check_dotnet: WARNING ? WARNING:Hello from C# 

This is the first working version of the new dot.net API and plugin
support. This works via a proxy plugin (DotnetPlugins) which loads all
configured dotnet plugins. Plugins can be written in pretty much any
language and I am implementing mine in C\#. It currently requires native
protocol buffer support which is avalible for atleast C\# and presumably
others as well. The API is a bit sketchy but follows closely how the
internal API looks as well as the modern plugins for Lua and Python. The
idea is that you have a factor class which creates instances of plugins
like so:

     namespace NSCP.Plugin { public class PluginFactory : NSCP.IPluginFactory { public NSCP.IPlugin create(NSCP.ICore core, String alias) { return new test.MyPlugin(core); } } } 

Then the plugin itself has access to all internal functions such as
settings and query and registry such so registering the commands looks
like this:

     public bool load(int mode) { core.getLogger().error("Hello World from C#"); core.getRegistry().registerCommand("check_dotnet", "This is a sample command written in C#"); return true; } 

Then we can of course act on our command by providing a query handler
like so:

     public NSCP.IQueryHandler getQueryHandler() { return new MyQueryHandler(core); } 

The last and rather messy step (mainly due top the extreme verbosity of
the \[http://code.google.com/p/protobuf-csharp-port/ C-Sharp port of
protobuffer\]) is to provide the command handler. I hope at some point
someone will be able to provide a plugin layer (written in native
dot-net) to make is slightly less verbose much like I have for Python,
C++ and Lua.

     public NSCP.Result onQuery(string command, byte[] request) { NSCP.Result result = new NSCP.Result(); // Process the incoming message Plugin.QueryRequestMessage request_message = Plugin.QueryRequestMessage.CreateBuilder().MergeFrom(request).Build(); string intcommand = request_message.GetPayload(0).Command; core.getLogger().error("Got command: " + intcommand + "/" + command); // Create response message Plugin.Common.Types.Header.Builder header = Plugin.Common.Types.Header.CreateBuilder(); header.SetVersion(Plugin.Common.Types.Version.VERSION_1); Plugin.QueryResponseMessage.Builder response_message = Plugin.QueryResponseMessage.CreateBuilder(); Plugin.QueryResponseMessage.Types.Response.Builder response = Plugin.QueryResponseMessage.Types.Response.CreateBuilder(); response.SetCommand(command); response.SetResult(Plugin.Common.Types.ResultCode.OK); response.SetMessage("Hello from C#"); response_message.AddPayload(response.Build()); response_message.SetHeader(header.Build()); result.data = response_message.Build().ToByteArray(); result.result = 1; return result; } 

This will all be checked in (if you prefer to check the entire C\#
plugin) during the weekend and a new RC next week will feature this. As
this has taken some time I will most likely have to skip a few of the
bugs I was planing to fix :) So hopefully the next RC will be the last
one. Also note that the C\# plugin API is sketchy so please use it but
beware that things are bound to change as I discover issues and
problems... // Michael Medin // Michael Medin
