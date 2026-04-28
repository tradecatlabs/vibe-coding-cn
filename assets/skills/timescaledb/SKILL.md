---
name: timescaledb
description: "TimescaleDB time-series skill: PostgreSQL extension setup, hypertables, time_bucket queries, continuous aggregates, compression/columnstore, retention, performance, and migration troubleshooting."
---

# timescaledb Skill

Use this skill to model and operate time-series workloads on TimescaleDB/Tiger Data using hypertables, time buckets, compression, and continuous aggregates.

## When to Use This Skill

Trigger when any of these applies:
- Creating or migrating PostgreSQL tables into TimescaleDB hypertables.
- Designing time-series schemas, chunk intervals, indexes, retention, or compression/columnstore policies.
- Writing `time_bucket` analytics queries or continuous aggregates.
- Debugging ingestion performance, query performance, refresh policies, or migration issues.
- Comparing plain PostgreSQL tables with TimescaleDB hypertables for event/time-series data.

## Not For / Boundaries

- Not a replacement for PostgreSQL fundamentals; use `postgresql` for generic SQL, transactions, roles, and non-time-series schema work.
- Do not enable retention/compression policies on production data without restore-tested backups and data-loss review.
- Continuous aggregates have version-specific behavior; verify real-time aggregation and refresh policy defaults against the installed version.
- Required inputs: TimescaleDB version, PostgreSQL version, table schema, time column, ingest rate, query patterns, retention/compression goals, and error text.
- Tiger Cloud features and self-hosted extension features may differ; verify deployment type before prescribing commands.

## Quick Reference

### Common Patterns

**Enable the extension**
```sql
CREATE EXTENSION IF NOT EXISTS timescaledb;
```

**Create a time-series table**
```sql
CREATE TABLE conditions (
  time timestamptz NOT NULL,
  location text NOT NULL,
  temperature double precision,
  humidity double precision
);
```

**Convert a table to a hypertable**
```sql
SELECT create_hypertable('conditions', 'time');
```

**Bucket raw data by hour**
```sql
SELECT
  time_bucket('1 hour', time) AS bucket,
  location,
  avg(temperature) AS avg_temp
FROM conditions
GROUP BY bucket, location
ORDER BY bucket DESC;
```

**Create a continuous aggregate**
```sql
CREATE MATERIALIZED VIEW conditions_hourly
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 hour', time) AS bucket,
  location,
  avg(temperature) AS avg_temp
FROM conditions
GROUP BY bucket, location;
```

**Inspect hypertable size**
```sql
SELECT * FROM hypertable_detailed_size('conditions');
```

**Verify extension version**
```sql
SELECT extversion FROM pg_extension WHERE extname = 'timescaledb';
```

## Examples

### Example 1: Convert Metrics Table to Hypertable

- Input: existing table `conditions(time, location, temperature, humidity)`.
- Steps:
  1. Confirm `time` is `NOT NULL` and uses a timestamp type.
  2. Enable the extension.
  3. Run `create_hypertable` in staging and test inserts/queries.
- Expected output / acceptance: the table is a hypertable and existing time-range queries still return correct rows.

### Example 2: Add Hourly Rollups

- Input: dashboard needs hourly average temperature by location.
- Steps:
  1. Write the raw `time_bucket('1 hour', time)` query.
  2. Convert it to a continuous aggregate after correctness is verified.
  3. Add a refresh policy only after deciding freshness and backfill windows.
- Expected output / acceptance: dashboard reads from the aggregate with documented refresh expectations.

### Example 3: Performance Triage

- Input: slow time-range query over a hypertable.
- Steps:
  1. Run `EXPLAIN (ANALYZE, BUFFERS)` and confirm chunk pruning.
  2. Check time predicate shape and indexes for dimension filters.
  3. Inspect hypertable/chunk size and compression state before changing policies.
- Expected output / acceptance: root cause is classified as missing time predicate, bad index, chunk sizing, compression side effect, or stale stats.

## References

- `references/index.md`: navigation for local TimescaleDB references.
- `references/installation.md`: install and deployment notes.
- `references/hypertables.md`: hypertables, chunks, sizing, and related APIs.
- `references/time_buckets.md`: `time_bucket` usage.
- `references/continuous_aggregates.md`: aggregate creation and refresh behavior.
- `references/compression.md`: compression/columnstore guidance.
- `references/performance.md`: performance notes.
- `references/tutorials.md`: walkthroughs and examples.

## Maintenance

- Sources: local `references/` extracted from TimescaleDB/Tiger Data documentation.
- Last updated: 2026-04-28
- Known limits: examples use common SQL forms; verify exact function signatures and policy defaults against the installed extension version.
