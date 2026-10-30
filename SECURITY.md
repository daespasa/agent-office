# Security policy

This repository currently contains a specification, schemas and synthetic fixtures, not a working execution service. Required controls are described in [the security model](docs/security-model.md); they are not a claim of an audited implementation.

Do not include credentials, exploit secrets, private logs or customer data in public issues. Use GitHub's private vulnerability reporting channel when enabled on this repository. If it is unavailable, open a minimal issue requesting a private contact without disclosing exploit details.

Implementations must not expose an unauthenticated agent/tool server to a network. Model output, imported notes, remote artifacts and plugins are untrusted. Default demo mode must not execute host commands or make paid requests.
