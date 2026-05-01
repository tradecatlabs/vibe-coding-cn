---
name: postgresql
description: "PostgreSQL database skill: psql usage, schema design, SQL queries, DDL/DML, transactions, RETURNING, indexing, EXPLAIN, permissions, libpq connection basics, and performance troubleshooting."
---

# postgresql Skill

Use this skill to design, query, debug, and operate PostgreSQL databases with evidence-based SQL and safe production habits.

## When to Use This Skill

Trigger when any of these applies:
- Writing or reviewing PostgreSQL SQL, DDL, DML, indexes, views, transactions, or migrations.
- Using `psql`, connection strings, `libpq`, or PostgreSQL client behavior.
- Debugging slow queries, locking, permissions, schema/search path, connection failures, or data-modifying statements.
- Designing normalized schema, constraints, keys, and query plans.
- Explaining PostgreSQL-specific features such as `RETURNING`, CTEs, roles, or `EXPLAIN`.

## Not For / Boundaries

- Not for destructive production changes without backups, migration plan, and rollback path.
- Do not expose database passwords, connection strings with secrets, dumps containing private data, or production credentials.
- Prefer explicit transactions and small verified changes for DDL/DML that touches real data.
- Required inputs: PostgreSQL version, schema/table definitions, query, expected result, observed error or plan, data volume, and environment.
- When docs or behavior differ by version, verify against the installed server with `SHOW server_version;`.

## Quick Reference

### Common Patterns

**Connect with psql**
```bash
psql "postgresql://user@localhost:5432/mydb"
```

**Check server version**
```sql
SHOW server_version;
```

**Create a table with a generated id**
```sql
CREATE TABLE users (
  id serial PRIMARY KEY,
  firstname text NOT NULL,
  lastname text NOT NULL
);
```

**Insert and return generated data**
```sql
INSERT INTO users (firstname, lastname)
VALUES ('Joe', 'Cool')
RETURNING id;
```

**Update and inspect changed rows**
```sql
UPDATE products
SET price = price * 1.10
WHERE price <= 99.99
RETURNING name, price AS new_price;
```

**Create an index**
```sql
CREATE INDEX test1_id_index ON test1 (id);
```

**Read a query plan**
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM users WHERE lastname = 'Cool';
```

**Use a transaction guard for data changes**
```sql
BEGIN;
UPDATE users SET lastname = 'Checked' WHERE id = 1 RETURNING *;
ROLLBACK;
```

**Harden search path for untrusted schemas**
```sql
SELECT pg_catalog.set_config('search_path', '', false);
```

## Examples

### Example 1: Add a Safe Migration

- Input: new table requirement and target PostgreSQL version.
- Steps:
  1. Write `CREATE TABLE` with primary key, `NOT NULL`, and constraints.
  2. Add indexes only for known query predicates.
  3. Run migration in a transaction in staging and verify with `\d`.
- Expected output / acceptance: migration is reversible or has a rollback plan and schema matches expected constraints.

### Example 2: Debug a Slow Query

- Input: SQL query, table definitions, estimated data volume, and current indexes.
- Steps:
  1. Run `EXPLAIN (ANALYZE, BUFFERS)` on a safe environment.
  2. Identify sequential scans, bad row estimates, sort/hash spills, or missing predicates.
  3. Propose the smallest index/query rewrite and re-run the plan.
- Expected output / acceptance: before/after plan evidence shows lower runtime or IO for the target workload.

### Example 3: Validate Data-Modifying SQL

- Input: `UPDATE` or `DELETE` statement for production data.
- Steps:
  1. Convert the predicate to a `SELECT count(*)` and inspect sample rows.
  2. Run inside `BEGIN` with `RETURNING` on a staging or transaction-guarded session.
  3. Commit only after row count and returned rows match the expected blast radius.
- Expected output / acceptance: affected rows are known before commit and the rollback path is explicit.

## References

- `references/index.md`: navigation for local PostgreSQL references.
- `references/getting_started.md`: psql, tutorial SQL, build/install, and basics.
- `references/sql.md`: SQL language, DDL/DML, `RETURNING`, monitoring, and advanced examples.

## Maintenance

- Sources: local `references/` extracted from PostgreSQL documentation.
- Last updated: 2026-04-28
- Known limits: server behavior depends on PostgreSQL version, extensions, configuration, statistics, and workload; validate with live plans.
