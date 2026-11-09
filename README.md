# Microsoft Sentinel Incident Fluctuation Analysis

**AI-assisted, multi-customer SOC analytics and automated management reporting**

*An incident count tells you **what** changed. Understanding **why** it changed takes a little more work.*

This project showcases an Azure-native approach to investigating month-over-month incident fluctuations across multiple **Microsoft Sentinel** workspaces. It brings together **Kusto Query Language (KQL)**, **Azure Logic Apps Standard**, **Azure Lighthouse**, and **Microsoft Foundry** to turn security telemetry into evidence-backed investigations and readable management reports.

The solution evolved from a locally hosted Python proof of concept into a cloud-orchestrated workflow. An end-to-end implementation has been **validated with eight customer environments**, with the architecture designed to support up to ten.

## Why this project?

A decrease in incidents is not necessarily a security improvement. Analytics rules may have changed, detections may have failed, or important logs may have stopped arriving. Similarly, stable monthly totals can hide substantial changes among individual detection rules.

The goal is to move beyond *"incidents went up or down"* and answer:

- **What changed?** Compare the last two completed months and identify the biggest incident drivers.
- **What might explain it?** Examine rule configuration, execution health, and telemetry changes.
- **What needs attention?** Highlight evidence-supported visibility gaps and actionable SOC follow-ups.
- **How do we communicate it?** Produce a consolidated, visual report that non-SOC stakeholders can understand.

## Key capabilities

| Capability | What it provides |
| --- | --- |
| **Multi-customer coverage** | Queries separate customer Sentinel workspaces through Azure Lighthouse delegated access. |
| **Five-part evidence analysis** | Combines incident trends, rule-level drivers, rule changes, detection health, and telemetry comparisons. |
| **Conditional investigation** | Runs additional health, configuration, and ingestion checks when investigation criteria are met. |
| **AI-assisted interpretation** | Uses a two-mode Foundry agent for focused customer investigations and consolidated management reporting. |
| **Automated PDF reporting** | Generates charts, customer scorecards, executive takeaways, and prioritized recommendations using Code Interpreter. |
| **Reliability safeguards** | Validates customer attribution and reporting evidence, manages larger model requests, and checks the generated PDF before delivery. |

## Architecture

![Azure-native Sentinel incident fluctuation analysis architecture](assets/architecture-overview.png)

The workflow separates **deterministic evidence collection** from **AI-assisted interpretation**:

1. **Orchestrate:** An Azure Logic App starts the monthly reporting process and loads the configured customer workspaces.
2. **Collect:** For each workspace, it executes the two mandatory KQL investigations through the Azure Monitor Logs Query API, with three additional checks run conditionally.
3. **Investigate:** Microsoft Foundry analyzes each customer's results independently and returns a concise, evidence-based assessment.
4. **Prepare:** Customer narratives and numerical chart evidence are compacted, associated with the correct workspaces, and validated for completeness.
5. **Report:** The same agent, in a separate reporting mode, uses Code Interpreter to assemble a multi-customer PDF.
6. **Deliver:** The workflow retrieves and checks the PDF, then sends it to authorized recipients through Outlook.

**Explore:** [Detailed architecture and editable diagrams](docs/architecture.md) · [Workflow implementation guide](docs/workflow-guide.md)

## The five evidence components

Each query has a specific analytical responsibility:

| KQL component | Main question |
| --- | --- |
| `MonthlyIncidentTrend` | How did the incident volume change between completed months? |
| `IncidentDrivers` | Which analytics rules contributed to the change or shifted in composition? |
| `AnalyticsRuleChanges` | Were relevant detection rules created, modified, enabled, or disabled? |
| `AnalyticsRuleHealth` | Were execution failures or rule-health issues observed? |
| `TelemetryVolumeComparison` | Did ingestion changes introduce possible monitoring visibility concerns? |

The KQL results remain the source of truth for numerical reporting. The agent **interprets** the supplied evidence; it does not execute new queries or modify customer environments.

See [evidence contracts and interpretation rules](docs/query-contracts.md) for the public data model.

## Technology stack

| Technology | Role |
| --- | --- |
| **Microsoft Sentinel + KQL** | Security incident analysis and detection evidence |
| **Azure Monitor Logs Query API** | Workspace-specific query execution |
| **Azure Lighthouse** | Delegated access across customer environments |
| **Azure Logic Apps Standard** | Monthly orchestration, conditions, validations, and delivery |
| **Microsoft Foundry** | Customer investigation and report-generation agent |
| **Python / Code Interpreter** | Charting and PDF construction |
| **Office 365 Outlook connector** | Distribution of validated management reports |

## Explore the repository

```text
assets/     Architecture diagrams (PNG, SVG, Graphviz)
docs/       Architecture, workflow, query contracts, engineering lessons
examples/   Fictional customer configuration, evidence, validation JavaScript
prompts/    Illustrative two-mode Foundry agent instructions
scripts/    Local sample validator and privacy-oriented release checker
.github/    Automated checks for example data and common sensitive patterns
```

Suggested starting points:

- [Architecture and trust boundaries](docs/architecture.md)
- [Workflow implementation guide](docs/workflow-guide.md)
- [KQL evidence contracts](docs/query-contracts.md)
- [Engineering lessons and troubleshooting](docs/engineering-lessons.md)
- [Example Foundry agent instructions](prompts/agent-instructions-example.md)

## Try the sample validation

You can run the included **synthetic-data checks** locally with Python 3, without Azure credentials:

```bash
git clone https://github.com/ShehanFranciscu/sentinel-incident-fluctuation-analysis.git
cd sentinel-incident-fluctuation-analysis

python3 scripts/validate_sample.py examples/management-evidence.example.json
python3 scripts/public_release_check.py
```

The first command checks the structure and required trend/driver records in fictional reporting evidence. The second scans repository files for common sensitive patterns. These checks **do not deploy Azure resources or generate a live PDF**.

## Engineering lessons

A few decisions shaped the production workflow:

- **Evidence before explanation:** A change in incident count is an observation, not a confirmed root cause.
- **Customer isolation:** Every query and interpretation stays attributable to its customer workspace.
- **Compact model inputs:** Removing redundant API metadata and limiting chart inputs helped manage token-rate pressure at higher customer counts.
- **Validate before generating:** The PDF stage checks for required customer investigations and chart records instead of assuming the inputs are complete.
- **A valid PDF is not always a valid report:** File-format checks and content-completeness checks serve different purposes.

Read more in [engineering lessons](docs/engineering-lessons.md).

## Project scope

This repository is a **sanitized architecture and reference-code showcase**, based on the working multi-customer implementation. It includes fictional example records, documentation, and illustrative validation code—not the production Logic App export, proprietary KQL implementations, tenant configuration, or real customer data. It is **not a one-click deployment package**.

For anyone adapting the design, the [workflow guide](docs/workflow-guide.md) outlines the components and safeguards that must be implemented in an authorized environment.

Security considerations and disclosure guidance are documented in [SECURITY.md](SECURITY.md). No open-source license is currently provided, so public visibility does not itself grant permission to reuse the code.

## References

- [Azure Lighthouse and Microsoft Sentinel](https://learn.microsoft.com/en-us/azure/lighthouse/how-to/manage-sentinel-workspaces)
- [Azure Monitor Logs Query API](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/api/overview)
- [Inline JavaScript in Azure Logic Apps](https://learn.microsoft.com/en-us/azure/logic-apps/add-run-javascript?tabs=standard)
- [Azure OpenAI quota guidance](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/quota)
