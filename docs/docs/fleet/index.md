# NSClient Fleet

**NSClient Fleet** is the control plane for NSClient++ installations: one server that holds
the configuration for a whole estate of agents, hands each host the part that applies to it,
and shows you what every host is actually running.

It is a separate product from the agent, in [its own
repository](https://github.com/mickem/nsclient-fleet-server). NSClient++ works exactly as it
always has without it — the fleet server is what you add when editing `nsclient.ini` on every
machine has stopped being reasonable.

---

## How it fits together

```
      operator's browser                      NSClient++ agent
              │                                      │
              │ HTTPS                                │ mTLS, ALPN nsclient-fleet/1
              ▼                                      ▼
      ┌───────────────────────────────────────────────────┐
      │  fleet server  (one binary, one port)             │
      │    groups → bundles → desired state per host      │
      └───────────────────────────────────────────────────┘
```

Configuration travels as **bundles** — signed archives holding an INI fragment and,
optionally, scripts. Bundles are assigned to **groups**, and a group selects hosts by tag.
An enrolled agent polls for its desired state, downloads the bundles assigned to it, verifies
their signature, renders them into a `fleet.ini` that its own `nsclient.ini` includes, and
reports back what it applied.

**The server never pushes.** Everything is pulled by the agent over a connection it opens, so
there is no inbound port to open on a monitored host and no module to enable.

---

## Where do you want to go?

### 🚀 I want to try it

[Running it in Docker](docker.md) — one `docker run`, a volume for the state, and a UI to sign
in to. The fastest path from nothing to a server you can enroll a host against.

### 🖥️ I want to install it on a Linux host

[Installing on Linux](linux-install.md) — step by step from a bare machine: the binary under
systemd, the master key, a certificate your browser trusts, the firewall, and the first host.

### 🪟 I want to install it on Windows

[Installing on Windows](windows-install.md) — the same, as a real Windows service: the
directory ACL that is the only thing protecting the data, the env file, the administrator
password hash, and where the logs go when a service has no console.

### 🏭 I want to run it in production

[Deployment reference](deployment.md) — ports and firewall, DNS, the two certificates and the
two trust models, every environment variable, backups and restore, capacity, on-prem mode, and
the platform console.

### 🔗 I want to enroll my agents

[Central management with NSClient Fleet](../setup/fleet.md) — the round trip from the agent's
side: getting NSClient++ to trust the server, enrolling, sending configuration, encrypted
bundles, and leaving the fleet again.

### 🔐 I need to rotate a compromised key

[CA rotation playbook](ca-rotation-playbook.md) — rotating a tenant CA or the bundle-signing
key, planned or after a compromise, without stranding the fleet.

### 🛠️ I am writing my own agent

- [Building the agent](agent-implementation.md) — the enrollment flow: bootstrap token → CSR →
  mTLS, then the poll loop, bundle verification and renewal.
- [Agent integration reference](agent-integration.md) — the post-enrollment contract in
  detail: config sync, state reporting, certificate lifecycle, error handling.

---

## What you need to know before you start

**One name, chosen once.** Agents and browsers both dial the server, and its hostname ends up
inside the certificate agents pin — so changing it later means re-enrolling every host.

**Two things that cannot be recovered.** `MASTER_KEY` encrypts every tenant CA and every host
override; `data/mtls-server.key` is the certificate the whole fleet pins. Neither can be
regenerated, and they are deliberately not stored together. See
[Backups and restore](deployment.md#9-backups-and-restore).

**One port, and nothing may terminate its TLS.** The operator UI, agent mTLS and ACME
challenges all share inbound 443, dispatched on the ClientHello. Agents offer ALPN
`nsclient-fleet/1` and pin the server's certificate, so a reverse proxy that re-encrypts, an
inspecting middlebox or most L7 load balancers will break them.

**Local settings win on the agent.** A key set in a host's own `nsclient.ini` keeps its local
value even when the fleet server sends a different one. That is a legitimate way to run, and a
genuine surprise when a centrally managed setting appears to do nothing.

---

## Hosted or your own hardware

The same binary does both. Left alone it is a multi-tenant service where each tenant signs up,
owns its own CA and sees only its own fleet. Set `ON_PREM=true` and it is single-tenant with
one administrator authenticated by password, no signup and no magic links — see
[On-prem deployment](deployment.md#12-on-prem-deployment).

Nothing about the agent side differs between the two.
