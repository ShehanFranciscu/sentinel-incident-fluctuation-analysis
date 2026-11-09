# Engineering lessons from the implementation

## A working prototype isn't an operational workflow

The local Python proof of concept demonstrated analysis value. Migrating orchestration to Logic Apps Standard separated scheduling, cross-tenant query access, conditional flow, AI interpretation and report delivery.

## Keep authoritative evidence separate from model interpretation

The five KQL queries remain the source of truth. The AI agent receives the outputs and provides interpretations. It does not rebuild the queries, change incident classifications or declare causes without evidence.

## Rate limiting requires data minimization and quota awareness

An eight-customer run encountered model-deployment HTTP 429 errors at the final report call. Helpful mitigations included concise 400–600-word investigations, compact numerical chart evidence, removal of redundant HTTP-response metadata, controlled call pacing and retry policy review. Even a short output can trigger throttling when estimated processed tokens exceed the current deployment's quota.

## Over-compression can break the report

Reducing input payload and prompts too aggressively initially produced a single-page report. A complete PDF needs validated customer coverage, supported chart values and a defined reporting structure. Token optimization must not silently eliminate required customer scorecards.

## A valid PDF is not necessarily a valid *report*

Another run generated a PDF that only said evidence was missing. File retrieval and PDF header checks succeeded, but the deliverable did not satisfy the reporting contract. Checking actual SOURCE A and SOURCE B data in the Foundry request, followed by pre-generation record validation, resolved this class of failure.

## Logic Apps Inline Code references are not arbitrary JavaScript properties

A workflow initially failed template validation when Inline Code dynamically indexed a referenced action using a variable. Using literal action names and declaring those action dependencies fixed the template validation error.

## Presentation requires deterministic layout rules

Unwrapped recommendation tables, clipped chart labels and excessive page breaks hurt readability. Favor ReportLab Paragraph-wrapped cells, dynamic row heights, readable charts, visible legends, customer scorecards and plain-English executive summaries. Instructions help, but reproducible templates and visual QA provide stronger guarantees.
