# Before publishing this project or article

## Permission and ownership

- [x] Architecture publication permission confirmed by the project author (2026-11-09).
- [ ] Confirm who owns the production workflow, KQL implementations, reporting prompts, and screenshots.
- [ ] Obtain permission before publishing any reusable proprietary implementation; choose a license with the rights holder.

## Content review

- [ ] Remove or replace actual customer names and industry-identifying details.
- [ ] Remove tenant, subscription, workspace and Entra application identifiers, GUIDs, endpoint URLs and internal email addresses.
- [ ] Never include client secrets, connection strings, bearer tokens, personal information or authorization headers.
- [ ] Do not upload production run-history exports, incident records, raw KQL results, or unsanitized management PDFs.
- [ ] Check architecture diagrams and screenshots for embedded names, workspace aliases and URLs.
- [ ] Verify that reported capacity and benefits are evidence-backed: eight customers validated; up to ten designed.
- [ ] Avoid unverifiable time-saving, cost-saving and SLA claims.

## GitHub controls

- [ ] Start in a private repository while obtaining disclosure approval, then switch to public only if authorized.
- [ ] Enable secret scanning and push protection where available.
- [ ] Check commit history and prior branches; deleting a file in a later commit does not necessarily erase the original disclosure.
- [ ] Decide on a license only after confirming ownership and approval.
- [ ] Publish fictional examples, not real customer evidence.

## Medium article

- [x] Use the repository-provided generic architecture PNG; do not use the original internal infographic.
- [ ] Add the final GitHub URL after the new repository exists.
- [ ] Review names and claims with the relevant stakeholders.
- [ ] Add author affiliation/disclaimer only as authorized.

## Automated verification

- [ ] Run `python3 scripts/validate_sample.py`.
- [ ] Run `python3 scripts/public_release_check.py`.
- [ ] Review any generated images or assets as well as textual source.
- [ ] Compare the final staged file list against the approved release ZIP.
