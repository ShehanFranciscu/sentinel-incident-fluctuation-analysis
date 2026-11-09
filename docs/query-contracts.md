# KQL evidence contracts

The production design uses **five approved and independently maintained queries**. This public document describes their purpose; it does **not** reproduce, approximate or modify the tested query implementations.

| Tool | Purpose | Key interpretation requirement |
| --- | --- | --- |
| `MonthlyIncidentTrend` | Completed-month incident counts, deltas and source-defined overall classification | Preserve authoritative trend status and period; do not use the model to invent new thresholds. |
| `IncidentDrivers` | Stable analytics-rule identity, rule-level incident changes and composition shifts | Incident/alert counts are not interchangeable; associated incidents can overlap across rules. |
| `AnalyticsRuleChanges` | Analytics rule create/modify/enable/disable and other audit evidence | A configuration change is not automatically a proven cause. |
| `AnalyticsRuleHealth` | Analytics rule execution failures or other health conditions | Distinguish observed execution problems from inferred detection gaps. |
| `TelemetryVolumeComparison` | Source-level ingestion shifts, stopped/new sources and continuity evidence | Check comparable periods/units; ingestion decrease does not prove threats decreased. |

## External query result envelope

Azure Monitor Logs returns `tables[].columns[]` (column name/type) and `tables[].rows[]` (positional values). Convert each row to an object keyed by its actual column names; never infer column indices without inspecting schema.

Workflow aggregation records should carry `customer_name`, `workspace_alias`, `tool`, `status` and `tables` (or explicitly documented normalized `rows`).

The PDF stage requires two mandatory numeric data sources per customer: one MonthlyIncidentTrend record and one IncidentDrivers record. Supporting queries may be conditional; a missing result must not be treated as a clean bill of health.

## Example chart data (fictional)

See [`../examples/management-evidence.example.json`](../examples/management-evidence.example.json). The file is a normalized demonstration shape **not** a direct copy of production query output.
