#!/usr/bin/env python3
import argparse
import subprocess
import sys


def _run(cmd: list[str]) -> int:
    return subprocess.call(cmd)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="cli.py")
    sub = ap.add_subparsers(dest="cmd")

    init = sub.add_parser("init", help="Initialize project from MVP_SPECIFICATION.yaml")
    init.add_argument("--guided", action="store_true", help="Run guided wizard to generate/refresh PROJECT_LAYOUT before init.")
    init.add_argument("--answers", default="", help="Wizard answers YAML (declarative).")
    init.add_argument("--preset", default="", help="Wizard preset override (e.g., nextjs_root, apps_packages, template_canonical).")
    init.add_argument("--mode", default="", help="Wizard adaptation mode override (adopt_existing|normalize_to_template).")
    init.add_argument("--auto-apply", action="store_true", help="Wizard: set PROJECT_LAYOUT.adaptation.auto_apply=true")

    sub.add_parser("generate-context", help="Generate AI execution context document")
    update = sub.add_parser("update-template", help="Update template files from template repository")
    update.add_argument("--template-repo", default="", help="Template repository URL")
    update.add_argument("--version", default="", help="Specific version to update to")
    update.add_argument("--dry-run", action="store_true", help="Show what would be updated")
    update.add_argument("--init-versioning", action="store_true", help="Initialize versioning for pre-versioned projects")
    update.add_argument("--force", action="store_true", help="Force update even if versions match")
    feedback = sub.add_parser("submit-feedback", help="Submit AI feedback to template repository")
    feedback.add_argument("--dry-run", action="store_true", help="Show what would be submitted")
    feedback.add_argument("--github-token", default="", help="GitHub token (or set GITHUB_TOKEN env var)")
    upgrade = sub.add_parser("upgrade-legacy", help="Upgrade legacy project to project_initializer format")
    upgrade.add_argument("--analyze", action="store_true", help="Phase 1: Analyze project structure")
    upgrade.add_argument("--plan", action="store_true", help="Phase 2: Generate upgrade plan")
    upgrade.add_argument("--execute", action="store_true", help="Phase 3: Execute upgrade plan")
    upgrade.add_argument("--validate", action="store_true", help="Phase 4: Validate upgrade")
    upgrade.add_argument("--template-repo", default="", help="Template repository URL")
    sub.add_parser("validate", help="Run all pre-commit hooks")
    sub.add_parser("trace", help="Generate traceability graph")
    sub.add_parser("review", help="Run AI review")
    sub.add_parser("commit-checkpoint", help="Commit with validation and proper message format")

    args = ap.parse_args(argv)

    if args.cmd == "init":
        if getattr(args, "guided", False):
            cmd = ["python3", "3_bootstrap_scripts/init_wizard.py", "--non_interactive"]
            if args.answers:
                cmd += ["--answers", args.answers]
            if args.preset:
                cmd += ["--preset", args.preset]
            if args.mode:
                cmd += ["--mode", args.mode]
            if getattr(args, "auto_apply", False):
                cmd += ["--auto_apply"]
            rc = _run(cmd)
            if rc != 0:
                return rc
        return _run(["python3", "3_bootstrap_scripts/init_project.py"])

    if args.cmd == "generate-context":
        return _run(["python3", "3_bootstrap_scripts/generate_ai_context.py"])
    if args.cmd == "update-template":
        cmd = ["python3", "3_bootstrap_scripts/template_update.py"]
        if getattr(args, "template_repo", ""):
            cmd.extend(["--template-repo", args.template_repo])
        if getattr(args, "version", ""):
            cmd.extend(["--version", args.version])
        if getattr(args, "dry_run", False):
            cmd.append("--dry-run")
        if getattr(args, "init_versioning", False):
            cmd.append("--init-versioning")
        if getattr(args, "force", False):
            cmd.append("--force")
        return _run(cmd)
    if args.cmd == "submit-feedback":
        cmd = ["python3", "3_bootstrap_scripts/feedback_collector.py"]
        if getattr(args, "dry_run", False):
            cmd.append("--dry-run")
        if getattr(args, "github_token", ""):
            cmd.extend(["--github-token", args.github_token])
        return _run(cmd)
    if args.cmd == "upgrade-legacy":
        cmd = ["python3", "3_bootstrap_scripts/upgrade_legacy_project.py"]
        if getattr(args, "analyze", False):
            cmd.append("--analyze")
        if getattr(args, "plan", False):
            cmd.append("--plan")
        if getattr(args, "execute", False):
            cmd.append("--execute")
        if getattr(args, "validate", False):
            cmd.append("--validate")
        if getattr(args, "template_repo", ""):
            cmd.extend(["--template-repo", args.template_repo])
        return _run(cmd)
    if args.cmd == "validate":
        return _run(["pre-commit", "run", "--all-files"])
    if args.cmd == "trace":
        return _run(["python3", "3_bootstrap_scripts/traceability_graph.py"])
    if args.cmd == "review":
        return _run(["python3", "3_bootstrap_scripts/ai_review.py"])
    if args.cmd == "commit-checkpoint":
        return _run(["bash", "scripts/commit_checkpoint.sh"])

    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
