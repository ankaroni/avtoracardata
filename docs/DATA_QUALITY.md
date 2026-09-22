# Data quality rules

- Preserve upstream source values before destructive normalization where practical.
- Never invent missing displacement, power, torque, production year or drivetrain.
- Empty/unknown remains NULL.
- Normalize presentation vocabulary only when the mapping is unambiguous.
- Deduplicate by hierarchy + normalized source key, never by engine label alone.
- Keep production years as ranges; listing registration year is separate.
- Market priority is merchandising metadata, not factual country availability.
- Run parity checks after every upstream refresh.
- Reject impossible numeric values rather than silently coercing them.
- Catalog corrections should be reviewed and documented in CHANGELOG.md.
