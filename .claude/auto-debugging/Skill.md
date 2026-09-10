เพิ่ม auto debug

เพิ่มได้ครับ โดยควรเพิ่มเป็น skill ชื่อ **Auto Debugging / Read–Reproduce–Fix–Verify** แต่ต้องทำงานแบบมี guardrails ไม่ใช่แก้โค้ดอัตโนมัติทันที เพราะแนวทางที่น่าเชื่อถือควรเริ่มจากอ่านหลักฐาน ทำให้เกิดปัญหาซ้ำ แก้แบบ diff เล็ก แล้วรันทดสอบยืนยันอีกครั้ง[1][2]

## Skill ที่เพิ่ม

```text
auto-debugging
```

### หน้าที่

- อ่าน error, stack trace, test failure และ CI logs
- แยก baseline failure ออกจากปัญหาที่เพิ่งเกิด
- สร้างหรือค้นหา reproducer
- ระบุตำแหน่งโค้ดที่เกี่ยวข้อง
- ตั้งสมมติฐาน root cause
- แก้ด้วย patch ที่เล็กที่สุด
- เพิ่มหรือปรับ regression test
- รัน focused test และ full validation
- สรุปสาเหตุ, diff, ผลทดสอบ และความเสี่ยง
- หยุดทันทีเมื่อไม่มีหลักฐานเพียงพอหรือแก้ซ้ำแล้วไม่คืบหน้า

## Prompt สำหรับเพิ่มเข้า Agent

```text
Add an auto-debugging capability with strict evidence-based guardrails.

Skill name:
auto-debugging

Debugging workflow:
1. Read
   - Inspect the error message, stack trace, failing test, CI logs,
     recent diff, relevant documentation, and environment details.
   - Record the exact failure and command that produced it.

2. Establish baseline
   - Check repository status before editing.
   - Run the smallest relevant existing test or reproduction command.
   - Record pass, fail, skipped, and errored counts.
   - Distinguish pre-existing failures from failures introduced by this task.

3. Reproduce
   - Create or locate a deterministic reproducer.
   - Prefer an existing failing test.
   - If no test exists, create a minimal temporary reproduction or a regression
     test only when appropriate.
   - Do not claim a bug is fixed unless the failure was reproduced or there is
     strong direct evidence.

4. Localize
   - Trace the failure to the smallest likely set of files, functions,
     configuration, dependency, or workflow steps.
   - Search symbols, imports, call sites, configuration references, and recent
     changes.
   - State confidence and alternative hypotheses.

5. Plan before patching
   - Propose a minimal repair plan.
   - Identify files allowed to change.
   - Explain expected behavior and validation commands.
   - Do not rewrite unrelated modules or perform broad cleanup.

6. Patch
   - Make the smallest justified change.
   - Preserve existing APIs and repository conventions.
   - Do not modify secrets, production credentials, generated files,
     lockfiles, CI policy, or unrelated files unless the failure requires it.
   - Add or update a focused regression test when a testable bug is confirmed.

7. Verify
   - Re-run the original reproducer.
   - Run the focused test.
   - Run related tests.
   - Run the repository's normal lint, type-check, build, or validation commands
     when available.
   - Compare results with the baseline.
   - Inspect the final diff and repository status.

8. Decide
   - Mark `fixed` only when the original failure is gone and relevant checks pass.
   - Mark `partially-fixed` when the original issue is improved but a known
     blocker remains.
   - Mark `blocked` when reproduction or validation is impossible.
   - Never hide failures or convert failing tests into skipped tests merely to
     obtain a green result.

Hard stop conditions:
- Stop after 3 unsuccessful patch attempts for the same root-cause hypothesis.
- Stop when two consecutive attempts produce no meaningful progress.
- Stop if the required test command is unknown and cannot be safely inferred.
- Stop if the proposed change would affect security, authentication,
  payments, database migrations, production infrastructure, or public APIs
  without explicit review.
- Stop if credentials, secrets, production data, or external destructive actions
  would be required.
- Stop before applying changes to a live environment.

Output for every debug run:
1. Failure summary
2. Baseline command and result
3. Reproduction steps
4. Root-cause hypothesis
5. Files inspected
6. Files changed
7. Patch rationale
8. Tests and validation commands
9. Before/after results
10. Remaining risks and blockers
11. Final status: fixed / partially-fixed / blocked / not-a-bug
```

## เพิ่มใน skill list เดิม

```text
1. repository-inventory
2. evidence-based-codebase-auditor
3. architecture-and-documentation-auditor
4. convention-discovery
5. ci-workflow-auditor
6. test-suite-auditor
7. auto-debugging
8. evidence-report-writer
9. safe-change-planner
```

## กติกาสำหรับ repo นี้

เนื่องจาก CI ของ repo นี้มี failure เดิมอยู่แล้ว ให้เพิ่มข้อกำหนดนี้โดยเฉพาะ:

```text
Repository-specific debugging rule:

Before fixing any CI or YAML failure:
- Record the current branch and Git status.
- Inspect all `.github/workflows/` files.
- Validate YAML syntax independently from action-policy validation.
- Separate failures caused by invalid YAML, unpinned action references,
  missing permissions, unavailable secrets, dependency errors, and test failures.
- Do not claim that CI is fixed merely because one workflow file parses.
- Report the exact number of failing workflows and remaining failures.
- Preserve the user's existing SHA-pinning policy.
- Do not replace SHA-pinned actions with mutable tags.
```

และสำหรับ `deliverables/`:

```text
Deliverable-specific debugging rule:

When debugging a suite under `deliverables/<suite>/`:
- Treat that suite as an isolated package.
- Read its `pyproject.toml`, README, source, and tests first.
- Run its own test and validation commands before running repository-wide checks.
- Do not move files across suites.
- Preserve each suite's existing package and test conventions.
```

## รูปแบบรายงานที่ควรสร้าง

แนะนำให้ Auto Debug บันทึกผลลงใน:

```text
new.inprogress.done/inprogress/auto-debug-<issue-slug>.md
```

เมื่อแก้เสร็จและผ่าน validation แล้วจึงย้ายไป:

```text
new.inprogress.done/done/auto-debug-<issue-slug>.md
```

Template:

```markdown
---
type: bug-fix
status: inprogress
created: 2026-09-10
updated: 2026-09-10
tags:
  - auto-debug
  - validation
---

# Auto Debug: <issue title>

## Failure

- Symptom:
- Command:
- Environment:
- First observed:

## Baseline

- Branch:
- Git status:
- Test command:
- Result:
- Pre-existing failures:

## Reproduction

```text
<exact command>
```

## Root Cause

<evidence-based explanation>

## Patch

- Files changed:
- Change summary:
- Why this is the smallest safe fix:

## Validation

- [ ] Original reproducer passes
- [ ] Focused test passes
- [ ] Related tests pass
- [ ] Lint/type-check/build passes
- [ ] Final diff reviewed
- [ ] No unrelated files changed

## Result

- Status: inprogress
- Remaining blockers:
- Risk:
- Next action:
```

## สรุปคำแนะนำ

ให้เปิด Auto Debug เป็น **เสนอ patch + ตรวจสอบอัตโนมัติ แต่ไม่ auto-merge และไม่แตะ production** ในช่วงแรก การให้ agent เปิด PR พร้อมแนบ root cause, test result และ diff จะปลอดภัยกว่าการให้แก้ `main` โดยตรง โดยเฉพาะ repository ที่มี CI เดิมล้มเหลวและมี policy เรื่อง SHA pinning อยู่แล้ว แนวทางที่ปลอดภัยควรใช้ test เป็นตัวตัดสิน, จำกัดไฟล์ที่แก้, ใช้ sandbox และคง human review ไว้สำหรับการอนุมัติสุดท้าย[3][4]

การอ้างอิง:
[1] Test with GitHub Copilot https://code.visualstudio.com/docs/agents/guides/test-with-copilot
[2] Autonomous Bug-Fixing Agents: From Issue to Verified Patch - AI Agents Guide https://aiagents.codeguides.io/coding-agent-use-cases/autonomous-bug-fixing-agents-from-issue-to-verified-patch/
[3] Self-Healing CI: Designing Guardrailed Auto-Fix PRs ... - DebuggAI https://debugg.ai/resources/self-healing-ci-guardrailed-auto-fix-prs-code-debugging-ai
[4] When debugging AI writes the patch: Should we let agents auto-fix ... https://debugg.ai/resources/when-debugging-ai-writes-the-patch-should-we-let-agents-auto-fix-bugs-in-ci-cd
[5] GitHub Copilot documentation https://docs.github.com/en/copilot
[6] GitHub Copilot tutorial: How to build, test, review, and ship code ... https://github.blog/ai-and-ml/github-copilot/a-developers-guide-to-writing-debugging-reviewing-and-shipping-code-faster-with-github-copilot/
[7] Reference for GitHub Copilot - GitHub Docs https://docs.github.com/en/copilot/reference
[8] Let Copilot Coding Agent handle the busy work - .NET Blog https://devblogs.microsoft.com/dotnet/copilot-coding-agent-dotnet/
[9] Debugging UI with AI: GitHub Copilot agent mode meets MCP servers https://github.blog/ai-and-ml/github-copilot/debugging-ui-with-ai-github-copilot-agent-mode-meets-mcp-servers/
[10] Debugging Workflows | GitHub Agentic Workflows https://github.github.com/gh-aw/troubleshooting/debugging/
[11] 📝 Assignment https://github.com/github/copilot-cli-for-beginners/blob/main/03-development-workflows/README.md
[12] github/awesome-copilot: Community-contributed instructions, agents ... https://github.com/github/awesome-copilot
[13] Can an AI Coding Agent Find and Fix Bugs Automatically? https://www.verdent.ai/guides/answers/ai-agent-find-fix-bugs-automatically
[14] GitHub Copilot for QA — Top 10 https://app.thetestingacademy.com/masterclass/copilot-tips
[15] AI Agents for Developers: PRs, Debugging, DevOps https://www.blockchain-council.org/agentic-ai/ai-agents-for-developers-code-review-pr-automation-debugging-devops-runbooks/
