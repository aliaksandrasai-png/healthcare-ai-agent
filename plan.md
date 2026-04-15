# Healthcare AI Agent Sprint 2026 — DATED EDITION
**START: 15 APRIL 2026 (WED)** → **FINISH: 27 MAY 2026**  
**Time**: 2-3 focused hours/day.  
**Domain**: Healthcare appointment scheduling with safety guardrails.

---

## DAY 0: 15 APRIL (WED) — TODAY
**Morning (1h)**: Create GitHub repo `healthcare-ai-agent`  
**Afternoon (1h)**: Copy this plan into `/plan.md`, commit & push  
**Evening (30min)**: Notion setup: create "Sprint Log 2026" page  
**Before Sleep**: Set phone alarm for 7:00am tomorrow

---

## WEEK 1: PROMPT FOUNDATIONS (16-22 APR)

### Day 1: 16 APR (THU)
**Theory (1h)**: Anthropic Prompt Guide — read "Overview" + "Basic Components"  
**Practice (1h)**: Colab — replicate 1 example, break it, fix it  
**Deliverable**: `week1/prompts_library.md` (create file, add 2 prompts)

### Day 2: 17 APR (FRI)
**Theory (1h)**: DeepLearning.AI "Prompt Engineering for Developers" (Module 1)  
**Practice (1h)**: Add 2 more prompts to library, annotate why they work  
**Deliverable**: 4 prompts total in library

### Day 3: 18 APR (SAT)
**Theory (1h)**: "Chain-of-Thought Prompting" paper — read "Zero-shot" section  
**Practice (1h)**: Convert your best prompt into CoT format  
**Deliverable**: CoT version saved in library

### Day 4: 19 APR (SUN)
**Theory (1h)**: "The Prompt Report" — sections 3.1-3.3  
**Practice (1h)**: Refine your worst prompt based on report  
**Deliverable**: Updated library with failure cases

### Day 5: 20 APR (MON)
**Theory (45min)**: Review 5 prompts from Anthropic's examples  
**Practice (1h 15min)**: Write "master prompt" for appointment scheduling  
**Deliverable**: `week1/master_prompt.md`

### Day 6: 21 APR (TUE)
**Theory (30min)**: YouTube "Prompt Engineering in Practice" (2x speed)  
**Practice (1h 30min)**: Test master prompt with 5 edge cases  
**Deliverable**: Edge cases log in Notion

### Day 7: 22 APR (WED) — WEEK 1 REVIEW
**OFF** or catch-up. If ahead, read "The Prompt Report" Section 3.4  
**Checkpoint**: GitHub repo has `week1/` folder with 3 files. You can explain your master prompt.

---

## WEEK 2: SINGLE AGENT (23-29 APR)

### Day 8: 23 APR (THU)
**Theory (1h)**: OpenAI Function Calling docs — quickstart only  
**Practice (2h)**: Build `week2/agent_v0.py` with `check_availability` function  
**Deliverable**: Working function call + 3 manual tests

### Day 9: 24 APR (FRI)
**Theory (1h)**: Lilian Weng "Tool Use" section  
**Practice (2h)**: Add `book_slot` function + SQLite DB setup  
**Deliverable**: `scheduler.db` with mock data

### Day 10: 25 APR (SAT)
**Theory (30min)**: LangSmith quickstart — set up tracing only  
**Practice (2h)**: Add `cancel_appointment` + integrate LangSmith logging  
**Deliverable**: `agent_v1.py` with full CRUD functions

### Day 11: 26 APR (SUN)
**Theory (30min)**: YouTube "Building AI Agents" (2x speed)  
**Practice (2h)**: Write 10 test cases (include edge cases)  
**Deliverable**: `week2/test_cases.md`

### Day 12: 27 APR (MON)
**Practice (3h)**: Run all 10 tests. Debug failures. Aim for 7/10 pass.  
**Deliverable**: `test_results.md` with pass/fail log

### Day 13: 28 APR (TUE)
**Practice (2h)**: Record 2-min Loom demo (unlisted)  
**Deliverable**: Loom link in `week2/README.md`

### Day 14: 29 APR (WED) — WEEK 2 REVIEW
**OFF** or fix critical bugs  
**Checkpoint**: Agent passes 7/10 tests. Loom demo recorded.

---

## WEEK 3: EVALUATION PIPELINE (30 APR - 6 MAY)

### Day 15: 30 APR (THU)
**Theory (30min)**: "Beyond Accuracy: Behavioral Testing" — read examples  
**Practice (2.5h)**: Setup DeepEval, write 1 unit test for JSON format  
**Deliverable**: `week3/test_eval.py` with 1 passing test

### Day 16: 1 MAY (FRI)
**Theory (30min)**: DeepEval G-Eval docs  
**Practice (2.5h)**: Create 0-3 scale rubric (accuracy, safety, format)  
**Deliverable**: `rubric.json`

### Day 17: 2 MAY (SAT)
**Practice (3h)**: Evaluate 5 agent runs using rubric, log results  
**Deliverable**: `results.md` table with scores

### Day 18: 3 MAY (SUN)
**Practice (3h)**: Automate regression test (`python test_eval.py` runs all)  
**Deliverable**: `evaluation_pipeline.py` working

### Day 19: 4 MAY (MON)
**Practice (2h)**: Run pipeline 3x with different prompts, track changes  
**Deliverable**: `regression_log.md` with 3 runs

### Day 20: 5 MAY (TUE)
**Practice (1h)**: Polish `week3/README.md` with methodology  
**Deliverable**: Clear explanation of eval system

### Day 21: 6 MAY (WED) — WEEK 3 REVIEW
**OFF** or run extra evals  
**Checkpoint**: `python test_eval.py` returns score in 10 seconds.

---

## WEEK 4: SAFETY GUARDRAILS (7-13 MAY)

### Day 22: 7 MAY (THU)
**Theory (30min)**: "LLMs in Healthcare: Risks" — risks section only  
**Practice (2.5h)**: Add PII regex filter to agent  
**Deliverable**: `week4/pii_filter.py` + `agent_v2.py`

### Day 23: 8 MAY (FRI)
**Practice (3h)**: Test PII filter with 10 malicious inputs  
**Deliverable**: `pii_test_log.md`

### Day 24: 9 MAY (SAT)
**Theory (30min)**: YouTube "AI Safety in 20 minutes"  
**Practice (2.5h)**: Add medical disclaimer trigger  
**Deliverable**: `disclaimer_trigger.md` with 10 test phrases

### Day 25: 10 MAY (SUN)
**Practice (3h)**: Implement audit log (`audit.log` with timestamps)  
**Deliverable**: `audit.log.example`

### Day 26: 11 MAY (MON)
**Practice (2h)**: Add toxicity check (keyword: "damn", "frustrated")  
**Deliverable**: `week4/agent_v2.py` fully safe

### Day 27: 12 MAY (TUE)
**Practice (1h)**: Update main README with "Safety Features" section  
**Deliverable**: README with safety badge

### Day 28: 13 MAY (WED) — WEEK 4 REVIEW
**OFF** or test edge cases  
**Checkpoint**: Agent refuses medical advice, logs PII, has audit trail.

---

## WEEK 5: MULTI-AGENT (14-20 MAY)

### Day 29: 14 MAY (THU)
**Theory (1h)**: "ReAct" paper — first 3 pages  
**Practice (2h)**: LangGraph quickstart, build dummy 2-node graph  
**Deliverable**: `week5/graph_v0.py`

### Day 30: 15 MAY (FRI)
**Theory (30min)**: LangGraph conditional routing docs  
**Practice (2.5h)**: Build Router Agent (classifies "schedule" vs "info")  
**Deliverable**: Router with 80% classification accuracy

### Day 31: 16 MAY (SAT)
**Practice (3h)**: Plug Week 4 agent as "Scheduler" node  
**Deliverable**: Router + Scheduler working

### Day 32: 17 MAY (SUN)
**Practice (3h)**: Build InfoBot (hardcoded dict with 3 medical FAQs)  
**Deliverable**: InfoBot node

### Day 33: 18 MAY (MON)
**Practice (2h)**: Connect all 3 agents in LangGraph  
**Deliverable**: `multi_agent.py` running end-to-end

### Day 34: 19 MAY (TUE)
**Practice (2h)**: Record 3-min Loom demo  
**Deliverable**: Loom link in `week5/README.md`

### Day 35: 20 MAY (WED) — WEEK 5 REVIEW
**OFF** or refactor  
**Checkpoint**: You can demo multi-agent system locally.

---

## WEEK 6: SHIP & SHOW (21-27 MAY)

### Day 36: 21 MAY (THU)
**Practice (3h)**: Refactor ALL code. Delete dead files. Add comments.  
**Deliverable**: Clean repo structure

### Day 37: 22 MAY (FRI)
**Practice (3h)**: Write final `/README.md` (use template from plan.md)  
**Deliverable**: README with metrics, demo link, contact

### Day 38: 23 MAY (SAT)
**Practice (3h)**: Record final 4-min Loom demo  
**Deliverable**: YouTube link (unlisted)

### Day 39: 24 MAY (SUN)
**Practice (2h)**: Edit Loom video (trim dead air). Upload to YouTube.  
**Deliverable**: Final demo link in README

### Day 40: 25 MAY (MON)
**Practice (2h)**: Post on r/PromptEngineering  
**Action**: Write post, paste GitHub link, reply to first 3 comments

### Day 41: 26 MAY (TUE)
**Practice (1h)**: Pin repo to GitHub profile. Update LinkedIn.  
**Deliverable**: Professional profile ready

### Day 42: 27 MAY (WED) — FINISH LINE
**OFF** or emergency fixes  
**Checkpoint**: GitHub repo is public, demo works, metrics are real.

---

## EMERGENCY BRAKE: IF YOU FALL BEHIND

- **1 day behind**: Skip theory, do practice only.  
- **3 days behind**: Drop Week 4 safety features → merge into Week 5.  
- **5 days behind**: Skip multi-agent. Perfect Week 2 single agent.  
- **1 week behind**: Restart current week, keep all commits. Ship small daily.

---

## YOUR NEXT 15 MINUTES (RIGHT NOW)

1. Create GitHub repo: `healthcare-ai-agent`
2. Copy this dated plan into `/plan.md`
3. Run:  
```bash
git init  
git add plan.md  
git commit -m "Day 0: Sprint begins 15 Apr 2026"  
git branch -M main  
git remote add origin https://github.com/YOUR_USERNAME/healthcare-ai-agent.git
git push -u origin main