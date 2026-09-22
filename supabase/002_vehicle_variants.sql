-- User-facing catalog: Brand -> Model -> Variant.
-- Year/fuel/transmission/body/power remain listing fields, not picker hierarchy.
create table if not exists vehicle_variants (
  id bigint generated always as identity primary key,
  model_id bigint not null references vehicle_models(id) on delete cascade,
  slug text not null,
  name text not null,
  source text not null default 'curated',
  is_active boolean not null default true,
  sort_order integer not null default 999,
  unique(model_id, slug)
);
create index if not exists idx_vehicle_variants_model on vehicle_variants(model_id, sort_order, name);
alter table vehicle_variants enable row level security;
drop policy if exists "public read variants" on vehicle_variants;
create policy "public read variants" on vehicle_variants for select using (true);
