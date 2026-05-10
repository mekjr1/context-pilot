from contextpilot.router.schemas import Classification


CODE_HINTS = {"fix", "bug", "test", "refactor", "failing", "patch"}
REPO_HINTS = {"repo", "codebase", "file", "function", "class", "module"}
DOC_HINTS = {"latest", "docs", "api", "version", "current", "release"}
ARCH_HINTS = {"architecture", "design", "system", "tradeoff"}


def classify(messages: list[dict], model: str = "") -> Classification:
    text = " ".join(str(m.get("content", "")) for m in messages).lower()
    words = set(text.split())

    task = "unknown"
    if words & CODE_HINTS:
        task = "code_fix"
    if words & ARCH_HINTS:
        task = "architecture"
    if words & DOC_HINTS:
        task = "docs_lookup"
    if "research" in words:
        task = "research"

    needs_code = bool(words & REPO_HINTS)
    needs_docs = bool(words & DOC_HINTS)
    complexity = "trivial" if len(text) < 80 else "easy"
    if len(text) > 400:
        complexity = "medium"
    if len(text) > 1200:
        complexity = "hard"

    tier = "cheap"
    if task in {"code_fix", "docs_lookup"}:
        tier = "default"
    if task in {"architecture", "research"}:
        tier = "strong"
    if complexity == "hard":
        tier = "deep"

    return Classification(
        task_type=task,
        complexity=complexity,
        needs_codebase=needs_code,
        needs_external_docs=needs_docs,
        needs_memory=True,
        freshness_required=needs_docs,
        recommended_model_tier=tier,
        confidence=0.75,
    )
