def plan(classification, messages=None, workspace_path=None, model_budget_policy=None):
    strategy = "direct"
    if classification.task_type == "code_fix" and classification.needs_codebase:
        strategy = "repo_search"
    elif classification.task_type == "docs_lookup" and classification.freshness_required:
        strategy = "docs_freshness"
    elif (
        classification.task_type == "architecture"
        and classification.needs_codebase
        and classification.needs_external_docs
    ):
        strategy = "repo_and_docs"

    return {
        "strategy": strategy,
        "steps": [
            "classify request",
            f"strategy:{strategy}",
            "route model tier",
        ],
        "do_not_do": ["read large repo slices before planning"],
        "recommended_context_limit_tokens": 4000,
    }
