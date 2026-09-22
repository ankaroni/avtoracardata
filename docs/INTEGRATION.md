# Vtora integration contract

## Picker flow
1. Make: sort `market_priority ASC, name ASC`.
2. Model: filter by `make_id`.
3. Variant: filter by `model_id`; expose verified commercial badges only.

Public hierarchy is strictly **Make → Model → Variant**. Generation, chassis code, production year and raw engine labels are internal metadata.

Do not expose upstream raw German/source labels in UI. Use canonical fields.

## Listing snapshot
A classified listing must store foreign keys when available, but also snapshot display values:
`make_name`, `model_name`, `variant_name`.
This prevents historical listings changing when the catalog is corrected.

## Free-text fallback
Catalogs are never perfect. Seller flow should include “Other / not listed” at model and variant stages. Save the seller text separately; do not insert unreviewed user text into the canonical catalog.

## VIN
VIN decoding is a separate concern. Never infer accident/mileage/history from this catalog. A VIN decoder may propose make/model/year, but the seller should confirm the match.

## Search/filter
Index and filter on make/model/variant IDs, year, fuel, transmission, drivetrain, body type, power and displacement. Store user-facing translations in the application i18n layer, not in database enum values.
