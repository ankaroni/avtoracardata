-- Vtora Bulgaria vehicle catalog schema (PostgreSQL / Supabase)
create table if not exists vehicle_makes (
  id bigint generated always as identity primary key,
  slug text not null unique, name text not null, country text,
  market text not null default 'GLOBAL', market_priority integer not null default 999,
  created_at timestamptz not null default now()
);
create table if not exists vehicle_models (
  id bigint generated always as identity primary key,
  make_id bigint not null references vehicle_makes(id) on delete cascade,
  slug text not null, name text not null, year_from smallint, year_to smallint,
  unique(make_id, slug)
);
create table if not exists vehicle_generations (
  id bigint generated always as identity primary key,
  model_id bigint not null references vehicle_models(id) on delete cascade,
  source_key text not null, name text not null, year_from smallint, year_to smallint,
  body_type text, unique(model_id, source_key)
);
create table if not exists vehicle_engines (
  id bigint generated always as identity primary key,
  generation_id bigint not null references vehicle_generations(id) on delete cascade,
  source_key text not null, label text not null, fuel_type text, cylinders smallint,
  displacement_cc integer, power_hp integer, torque_nm integer, transmission text,
  drivetrain text, zero_to_100_s numeric(5,2), top_speed_kmh integer,
  fuel_economy_combined_l100 numeric(6,2), length_mm integer, width_mm integer,
  height_mm integer, wheelbase_mm integer, curb_weight_kg integer,
  unique(generation_id, source_key)
);
create table if not exists vehicle_engine_specs (
  engine_id bigint not null references vehicle_engines(id) on delete cascade,
  key text not null, value text, primary key(engine_id,key)
);
create index if not exists idx_vehicle_models_make on vehicle_models(make_id);
create index if not exists idx_vehicle_generations_model on vehicle_generations(model_id);
create index if not exists idx_vehicle_engines_generation on vehicle_engines(generation_id);
create index if not exists idx_vehicle_makes_market_priority on vehicle_makes(market,market_priority,name);
alter table vehicle_makes enable row level security;
alter table vehicle_models enable row level security;
alter table vehicle_generations enable row level security;
alter table vehicle_engines enable row level security;
alter table vehicle_engine_specs enable row level security;
drop policy if exists "public read makes" on vehicle_makes;
create policy "public read makes" on vehicle_makes for select using (true);
drop policy if exists "public read models" on vehicle_models;
create policy "public read models" on vehicle_models for select using (true);
drop policy if exists "public read generations" on vehicle_generations;
create policy "public read generations" on vehicle_generations for select using (true);
drop policy if exists "public read engines" on vehicle_engines;
create policy "public read engines" on vehicle_engines for select using (true);
drop policy if exists "public read engine specs" on vehicle_engine_specs;
create policy "public read engine specs" on vehicle_engine_specs for select using (true);
