# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in UAS-AIOS, please report it responsibly.

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, please email: **contact@neurospan.io**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will acknowledge receipt within 48 hours and provide a timeline for resolution.

## Supported Versions

| Version | Supported |
|---------|-----------|
| latest (main) | Yes |

## Security Considerations

- The `uas_world_model` rule engine uses sandboxed evaluation. Avoid passing untrusted input to rule conditions.
- The runtime service executes Python scripts from sub-app `scripts/` directories. Only run trusted sub-apps.
- API keys and credentials should never be committed to the repository.
