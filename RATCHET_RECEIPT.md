# RATCHET_RECEIPT

**Repository:** `xoate0100/learn_rephase`  
**Generated:** 2026-08-27T06:28:40Z  
**Wave:** fleet-ratchet-full (Wave 0.5)

## Version

| | |
|---|---|
| From | `4.2.0` |
| To | `4.15.0` |
| Hub | `xoate0100/project_initializer@4.15.0` |

## Outcome

**PR opened**



## Flags

- (none)

## Files changed (69)

- `0_phase0_bootstrap/AI_SANDBOX_RULES.md`
- `0_phase0_bootstrap/META_FRAMEWORK_VERSION.yaml`
- `3_bootstrap_scripts/ai_behavior_validation.py`
- `3_bootstrap_scripts/check_state_transition.py`
- `3_bootstrap_scripts/cli.py`
- `3_bootstrap_scripts/crosswalk.py`
- `3_bootstrap_scripts/decision_registry_validate.py`
- `3_bootstrap_scripts/drift_vector_check.py`
- `3_bootstrap_scripts/factory_run.py`
- `3_bootstrap_scripts/fleet_ratchet.py`
- `3_bootstrap_scripts/fleet_upgrade.py`
- `3_bootstrap_scripts/governance_drift_validate.py`
- `3_bootstrap_scripts/guardrail_enforcement.py`
- `3_bootstrap_scripts/module_registry_validate.py`
- `3_bootstrap_scripts/reference_validate.py`
- `3_bootstrap_scripts/task_completion_gate.py`
- `5_reference_architectures/COMMAND_INTERFACE.md`
- `5_reference_architectures/DECISION_REGISTRY.yaml`
- `5_reference_architectures/FLEET_LEDGER.yaml`
- `5_reference_architectures/MODULE_REGISTRY.yaml`
- `5_reference_architectures/content_ir/rubric_v1.yaml`
- `5_reference_architectures/content_ir/voice.ce.course.yaml`
- `5_reference_architectures/content_ir/voice.cutrates.skill.yaml`
- `7_schemas/capabilities_lock.schema.json`
- `7_schemas/capability_agent_manifest.schema.json`
- `7_schemas/capability_conformance_suite.schema.json`
- `7_schemas/capability_descriptor.schema.json`
- `7_schemas/fleet_ledger.schema.json`
- `7_schemas/modules_lock.schema.json`
- `7_schemas/module_manifest.schema.json`
- `7_schemas/stack_adapter.schema.json`
- `7_schemas/content_ir/agents_entry.schema.json`
- `7_schemas/content_ir/content_ir.core.schema.json`
- `7_schemas/content_ir/grounding_ref.schema.json`
- `7_schemas/content_ir/jurisdiction_rule_pack.schema.json`
- `7_schemas/content_ir/profile.ce.course.schema.json`
- `7_schemas/content_ir/profile.cutrates.skill.schema.json`
- `7_schemas/content_ir/rubric_spec.schema.json`
- `7_schemas/content_ir/scene_graph.schema.json`
- `7_schemas/content_ir/variant_layer.schema.json`
- `7_schemas/content_ir/projections/course_package.projection.schema.json`
- `7_schemas/content_ir/projections/skill.projection.schema.json`
- `7_schemas/factory_kernel/batch_result.schema.json`
- `7_schemas/factory_kernel/export_manifest.schema.json`
- `7_schemas/factory_kernel/generation_request.schema.json`
- `7_schemas/factory_kernel/job.schema.json`
- `7_schemas/factory_run/run_manifest.schema.json`
- `7_schemas/mapped/behavioral.capabilities.json`
- `7_schemas/mapped/operational.capabilities.json`
- `7_schemas/mapped/product.capabilities.json`
- `agentic/diff_utils.py`
- `adapters/generic/README.md`
- `adapters/generic/stack_adapter.json`
- `adapters/generic/stack_adapter.yaml`
- `adapters/generic/scripts/stub_verb.py`
- `adapters/node/stack_adapter.json`
- `adapters/node/stack_adapter.yaml`
- `adapters/node/.runtime/initialized.json`
- `adapters/node/lib/capability_adapter.mjs`
- `adapters/node/lib/conformance_runner.mjs`
- `adapters/node/lib/feedback.mjs`
- `adapters/node/lib/providers/surewealth_content_generate.mjs`
- `adapters/node/scripts/apply-updates.mjs`
- `adapters/node/scripts/crosswalk.mjs`
- `adapters/node/scripts/health.mjs`
- `adapters/python/stack_adapter.json`
- `adapters/python/stack_adapter.yaml`
- `meta.ps1`
- `meta.sh`


## Protected / skipped (3)

- `0_phase0_bootstrap/MVP_SPECIFICATION.yaml`
- `0_phase0_bootstrap/feature_flags.yml`
- `5_reference_architectures/CHILD_REPOSITORY_REGISTRY.yaml`

## Notes

- Template sync via hub `template_directories`, respecting `protected_files`.
- Product runtime paths were not force-overwritten.
- NA-14 / NA-16 were **not** executed in this wave.
