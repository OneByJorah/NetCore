# NetCore — Persona

Archetype:        The Wire Whisperer

One-line pitch:   Configures the switches nobody wants to console into by hand.

Voice:            terse · technical · unimpressed. Never says "seamless". Never anthropomorphises the hardware.

Sample sentences:
- "Twenty-nine devices, one template, no typos."
- "The running-config is the truth; the diagram is a rumour."
- "Rollback is a button, not a promise."

Palette:          primary #0ea5e9 (link blue) · background #0b1220 · surface #111a2e · muted #94a3b8
Typography:       JetBrains Mono for configs, hostnames, IPs and diffs; UI sans for prose.

Emoji policy:     none

Banner concept:   A real terminal capture of a dry-run config push, or the live dashboard switch
                  list — captured from the running app, never stock art.

Do:
- Show the diff before applying it.
- Say plainly which vendors and transports are actually tested.
- Keep secrets out of config backups and screenshots.

Don't:
- Claim vendor support that was never exercised against a device.
- Imply a dry run touched a switch.
- Present a mock switch as a real one.

Target reader:    Network and sysadmin engineers managing mixed-vendor switches (Cisco-style,
                  HP ProCurve, ArubaOS) who want templated, auditable changes instead of
                  hand-typed console sessions.
