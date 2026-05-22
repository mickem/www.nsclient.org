# About NSClient++

NSClient++ (nscp) aims to be a simple yet powerful and flexible monitoring daemon. It was built for Nagios/Icinga/Naemon, but nothing in the daemon is specific to those systems, and it is used in many other scenarios where check metrics need to be collected, forwarded or acted upon. NSClient++ can also run standalone as the central monitoring system, though that is not recommended — the built-in scheduling and alerting are intentionally minimal compared to a dedicated monitoring server.

## What does it do?

NSClient++ does three things:

* **Allow remote checks** — let a monitoring server request commands on the monitored machine and return the result.
* **Monitor systems in real time** — collect metrics locally and submit them to a remote monitoring server.
* **Resolve problems** — act on its own findings or on instructions from a central server (for example restarting a service when a check fails).

In addition it offers a built-in [Web UI](docs/setup/web-interface.md), a [REST API](docs/api/rest/metrics.md), and is scriptable in [Lua](docs/extending/lua.md) and Python or via any external script.

## What monitoring systems does it support?

NSClient++ was designed to work with Nagios/Naemon/Icinga but can easily be adapted to any monitoring or information system. The full module list lives in the [reference](docs/reference/index.md); the protocols it speaks are:

**Active checks (server side)**

* NRPE — Nagios Remote Plugin Executor
* check_nt — legacy NSClient protocol
* check_mk — Check_MK live status
* REST / HTTP — NSClient++ native API

**Passive submission (client side)**

* NSCA — Nagios Service Check Acceptor
* NSCA-NG — TLS-based next-generation NSCA
* NRDP — Nagios Remote Data Processor
* Icinga 2 — passive results via the Icinga 2 REST API
* Op5 — Op5 Monitor northbound API

**Metrics and log forwarding**

* Graphite
* Syslog
* SMTP
* CollectD
* Elastic
* Prometheus / OpenMetrics (scraped from the REST API)

## Where does it run?

NSClient++ runs on Windows and most Linux distributions. There are two Windows editions — a standard build for Windows Server 2008 R2 / Windows 7 and later, and a legacy build that still runs on Windows XP. See [Supported platforms](docs/setup/supported-platforms.md) for the full matrix.

## Who is behind NSClient++?

NSClient++ is largely written and maintained by **Michael Medin**.
He uses `My Computer Solutions NORDIC KB` as a company to handle the legal and financial aspects of the project.

Contacting the project can be done via email `info@nsclient.org` or on the following address:
```
Michael Medin
My Computer Solutions NORDIC KB
Knipvägen 179
SE-184 62 ÅKERSBERGA
SWEDEN
```
