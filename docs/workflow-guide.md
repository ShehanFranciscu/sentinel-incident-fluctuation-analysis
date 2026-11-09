# Implementation guide — reference workflow

> These steps describe the pattern. They are not a complete export or a one-click deployment and must be adapted to your approved environment.

## Prerequisites

- Microsoft Sentinel-enabled Log Analytics workspaces in approved customer environments.
- An Azure Logic Apps Standard application and a configured monthly recurrence schedule.
- Azure Lighthouse delegated access and an appropriately privileged Entra application identity or managed identity where supported.
- Approved KQL implementations for all five tools.
- A Microsoft Foundry project, model deployment, agent endpoint, and Code Interpreter capability appropriate to the chosen agent configuration.
- An authorized email connector and recipients.
- Review of data protection, allowed cross-tenant access, token quotas, budget and customer agreements.

## Workflow outline

1. Initialize a customer registry with `customer_name`, `workspace_alias` and `workspace_id`, plus arrays for query results and completed investigations.
2. Keep approved KQL definitions in their designated workflow actions or secured configuration, with no changes to the tested query semantics.
3. For each workspace, invoke `POST https://api.loganalytics.azure.com/v1/workspaces/{workspaceId}/query` using authorized credentials and a JSON body containing the KQL query. Verify the workspace GUID and authentication audience before deployment.
4. Run `MonthlyIncidentTrend` and `IncidentDrivers`. Store results with customer identity, tool name, status and returned table schema/rows.
5. Evaluate whether to run `AnalyticsRuleChanges`, `AnalyticsRuleHealth` and `TelemetryVolumeComparison` for that customer. A skipped conditional query is not a confirmed healthy state.
6. For each customer, filter its evidence, check mandatory tool availability, and invoke the Foundry agent in `CUSTOMER_ANALYSIS` mode. Preserve a short, complete narrative with customer/workspace identity.
7. Build compact chart evidence from numeric results; avoid long raw alert-name arrays, while retaining meaningful source classifications and rule changes.
8. Validate that each expected customer has one non-empty investigation and required trend/driver evidence. In Logic Apps Inline Code, use explicit action references and declare dependencies.
9. Invoke the same agent in `MANAGEMENT_PDF` mode. Provide concise investigations and chart evidence; request an actual PDF Code Interpreter artifact.
10. Extract the returned file reference, retrieve the PDF, and validate both its structure and report coverage before authorizing email delivery. On failure, terminate or alert rather than emailing an error-only PDF.

## Reliability checklist

- Use bounded 429 retry/backoff guided by deployment limits; repeated calls with an oversized payload may not help.
- Monitor model token usage, request size, pipeline duration, failed queries and failed reports.
- Avoid logging client secrets, bearer tokens, unredacted source evidence or customer reports in unrestricted run history.
- Check idempotency of email delivery so reruns don't send duplicate reports without intent.
- Do not equate a valid PDF file with a complete management deliverable.

## Missing implementation components

The public reference intentionally lacks production workflow JSON, specific Entra role grants, connection secrets, the five exact KQL bodies, real API endpoint identifiers and confidential customer data. Those must be supplied or implemented by the authorized deploying team.
