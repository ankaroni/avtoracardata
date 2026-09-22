# Public picker contract

The Vtora listing picker is strictly:

**Make → Model → Variant**

Examples:
- Mercedes-Benz → A-Class → A 180 d
- BMW → 3 Series → 320d
- Audi → A4 → 40 TDI
- Volkswagen → Golf → GTI

Generation/chassis codes, production years and raw engine labels are NOT selectable hierarchy levels.

The seller enters year, fuel, gearbox, body style, mileage, power and other listing facts separately.

## Critical quality rule
A commercial variant is not guessed from displacement/power. If upstream data cannot prove a badge/variant (e.g. A 180 d), it must be curated/verified before publication. Raw engine labels remain technical metadata only.

## UI
Label the third field `Variant`. Never show strings such as `A-Klasse (1997)` as variants. Include `Other / Not listed` fallback without polluting canonical catalog data.
