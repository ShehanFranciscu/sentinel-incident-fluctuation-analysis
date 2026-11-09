# Publishing this sanitized reference project

The project is a **documentation and synthetic-data reference**, not a deployable production Logic App. The production PDFs, KQL code, customer details, Azure identifiers and secrets are intentionally excluded.

## Step 1 — Create a clean repository

In the GitHub account where you want the project published, select **New repository** and use:

- Repository name: `sentinel-incident-fluctuation-analysis`
- Description: `Sanitized reference architecture for Azure Logic Apps + Microsoft Foundry multi-customer Sentinel monthly reporting`
- Visibility: preferably **Private** for the initial commit and final inspection, then **Public** when approved.
- Do not pre-create a README, `.gitignore`, or license: these files are handled in the local package.

The remote URL example below only becomes valid **after** the repository has been created. Publishing approval does not imply that an open-source license has been granted; add one only with the rights holder's decision.

## Step 2 — Download, unpack and validate

Extract the public-ready ZIP and open a terminal in the resulting `sentinel-incident-fluctuation-analysis` folder.

```bash
python3 scripts/validate_sample.py examples/management-evidence.example.json
python3 scripts/public_release_check.py
```

Both checks should pass. Inspect the README, docs, diagram images and sample files manually too. Automated detection does not guarantee that confidential information is absent.

## Step 3 — Stage only sanitized files

```bash
git init -b main
git add .
git status --short
git diff --cached --name-only
git commit -m "Initial sanitized Sentinel incident fluctuation reference"
git remote add origin https://github.com/ShehanFranciscu/sentinel-incident-fluctuation-analysis.git
git push -u origin main
```

Do not add real PDF reports, workspace registry exports, KQL query-result CSVs, internal architecture screenshots, secrets, runtime logs, or other files from your production workspace.

If you already have a local Git repository or a differently named remote, adapt these commands rather than overwriting existing history.

## Step 4 — Validate the remote

- Open the repository as a viewer and check all exposed files and images.
- Review the GitHub Actions sample/scan checks.
- Review secret-scanning or push-protection alerts where available.
- Inspect the default branch, other branches and commit history for accidental inclusions.
- If you created it privately, change it to **Public** only after the checks pass.

## Step 5 — Publish the Medium case study

- Use the separately provided `Medium_Article_Ready_for_Publication.md` draft.
- At the architecture placeholder, upload the sanitized `assets/architecture-overview.png` directly into Medium.
- Replace the GitHub placeholder with the new public repository URL.
- Verify the rendered article on mobile, especially table width and image readability.
- Link back from the README to the published article if desired.

**Do not copy any original customer management report or internal workflow export into the article or repository.**
