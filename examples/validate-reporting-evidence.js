/*
 * ILLUSTRATIVE Azure Logic Apps Execute JavaScript Code snippet.
 * Action names below are literal dependencies; add both under Advanced parameters > Actions.
 * Adapt the investigation text property to your actual Build_Compact_Investigations output.
 * Not a drop-in guarantee for an uninspected workflow export.
 */
var investigationsAction = workflowContext.actions.Build_Compact_Investigations;
var chartsAction = workflowContext.actions.Prepare_Compact_Chart_Evidence;

function actionArray(action, description) {
    if (!action || !action.outputs) {
        throw new Error("Missing output: " + description);
    }
    var value = action.outputs;
    if (value && !Array.isArray(value) && typeof value === "object" &&
        typeof value.body !== "undefined") {
        value = value.body;
    }
    if (typeof value === "string") value = JSON.parse(value);
    if (!Array.isArray(value)) {
        throw new Error(description + " did not return an array");
    }
    return value;
}

var investigations = actionArray(investigationsAction, "Investigations");
var chartEvidence = actionArray(chartsAction, "Chart evidence");
var workspaces = {};

if (investigations.length < 1 || investigations.length > 10) {
    throw new Error("Invalid customer count: " + investigations.length);
}

for (var i = 0; i < investigations.length; i++) {
    var item = investigations[i];
    if (!item.customer_name || !item.workspace_alias) {
        throw new Error("Missing customer identity at investigation " + i);
    }
    // Adjust this field mapping to match your compact-investigation schema.
    var narrative = item.investigation || item.analysis || item.summary || item.report;
    if (typeof narrative !== "string" || !narrative.replace(/\s/g, "")) {
        throw new Error("Empty investigation narrative: " + item.workspace_alias);
    }
    if (workspaces[item.workspace_alias]) {
        throw new Error("Duplicate workspace: " + item.workspace_alias);
    }
    workspaces[item.workspace_alias] = { MonthlyIncidentTrend: 0, IncidentDrivers: 0 };
}

for (var j = 0; j < chartEvidence.length; j++) {
    var record = chartEvidence[j];
    if (!record.workspace_alias || !workspaces[record.workspace_alias]) {
        throw new Error("Unknown chart workspace: " + record.workspace_alias);
    }
    if (!record.tool ||
        typeof workspaces[record.workspace_alias][record.tool] === "undefined") {
        throw new Error("Unexpected tool for " + record.workspace_alias);
    }
    workspaces[record.workspace_alias][record.tool]++;
}

for (var alias in workspaces) {
    if (workspaces.hasOwnProperty(alias)) {
        if (workspaces[alias].MonthlyIncidentTrend !== 1 ||
            workspaces[alias].IncidentDrivers !== 1) {
            throw new Error("Missing or duplicate mandatory evidence: " + alias);
        }
    }
}

return {
    validated: true,
    customer_count: investigations.length,
    chart_record_count: chartEvidence.length
};
