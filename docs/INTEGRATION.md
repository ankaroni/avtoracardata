# Vtora integration contract

## Picker flow
1. Make: sort `market_priority ASC, name ASC`.
2. Model: filter by `make_id`.
3. Generation: filter by `model_id`, newest `year_from` first.
4. Engine: filter by `generation_id`.

Do not expose upstream raw German/source labels in UI. Use canonical fields.

## Listing snapshot
A classified listing must store foreign keys when available, but also snapshot display values:
`make_name`, `model_name`, `generation_name`, `engine_label`.
This prevents historical listings changing when the catalog is corrected.

## Free-text fallback
Catalogs are never perfect. Seller flow should include “Other / not listed” at model, generation and engine stages. Save the seller text separately; do not insert unreviewed user text into the canonical catalog.

## VIN
VIN decoding is a separate concern. Never infer accident/mileage/history from this catalog. A VIN decoder may propose make/model/year, but the seller should confirm the match.

## Search/filter
Index and filter on make/model/generation IDs, year, fuel, transmission, drivetrain, body type, power and displacement. Store user-facing translations in the application i18n layer, not in database enum values.
