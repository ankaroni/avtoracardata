# Vtora Vehicle Category Standard

## Public hierarchy
1. Make
2. Model
3. Variant

No generation, chassis code, production year, displacement, horsepower, transmission or body style is a category level.

## Examples
- Mercedes-Benz > A-Class > A 180 d
- BMW > 3 Series > 320d
- Audi > A4 > 40 TDI
- Volkswagen > Golf > GTI

## Listing attributes
Year, fuel, transmission, body type, mileage, power, displacement, drivetrain, color and condition belong to the listing form and filters.

## Data rules
- Canonical public names are clean English/market badges.
- Never manufacture a commercial badge from horsepower/displacement.
- Never expose raw upstream generation or engine strings as a Variant.
- Deduplicate aliases and punctuation/case variants.
- Keep historical variants; current production status does not remove them.
- Other / Not listed is a UI fallback, not a canonical variant row.
- Curated variant rows require provenance and verification.
- Bulgaria priority affects ordering only.
