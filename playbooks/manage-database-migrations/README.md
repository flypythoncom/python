---
id: manage-database-migrations
type: playbook
title: Manage Database Schema Migrations
summary: Plan, execute, and verify reversible database migrations with zero-downtime compatibility and rollback safety.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-02
---

# Manage Database Schema Migrations

1. Separate schema migration changes from application code deployments whenever
   introducing non-additive column or table alterations.
2. Follow expand-and-contract: add new nullable columns or tables first, write to
   both old and new fields, backfill historical data in batches, then drop old columns.
3. Verify migration script autogeneration with Alembic; inspect every generated SQL
   statement for destructive operations (`DROP COLUMN`, table locks, or unindexed constraints).
4. Implement and test both `upgrade()` and `downgrade()` functions against a clean
   local test database before submitting the change.
5. Apply explicit statement timeouts during migration runs to prevent locking production
   tables under heavy concurrent workloads.
6. Verify application behavior with both old and new schema versions active to guarantee
   zero-downtime rolling deployment safety.
