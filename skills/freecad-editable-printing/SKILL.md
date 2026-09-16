---
name: freecad-editable-printing
description: Design and revise functional parts intended for 3D printing, using human-editable FreeCAD models by default. Use for printable objects, enclosures, holders, mounts, assemblies, fit and support design, and slicer projects. Honor an explicitly requested CAD framework.
---

# Functional 3D printing

Use editable native bodies, sketches, standard features, and shared parameters with units. Preserve user-edited CAD, slicer settings, text, colors, and styling. Start from the latest master; save revisions separately unless replacement is requested. Mesh export does not turn a mesh into editable CAD.

## Choose the scope

- **Explain/review:** inspect relevant geometry or settings; do not rebuild or export unless needed for the answer.
- **Small revision:** edit the existing model; check affected features and dependent fit/appearance. Do not rerun unrelated mechanical tests or parameter variants.
- **New mechanism, assembly, or parameter relationship:** check solids, critical dimensions, mating clearance/interference, assembly access, and print orientation. Exercise meaningful parameter variants when those relationships changed; restore intended values. Use representative physical tests for uncertain fit, flexing, or support removal.
- **Export only:** run the saved export command. Read compact results and inspect the preview; do not recreate packaging code or reread its implementation.

Ask only for missing dimensions, loads, hardware, material, or slicer choices that materially affect the task. Use established preferences. Distinguish assumptions, digital checks, and physical performance.

## Project record and automation

Reuse `print-project.json` beside the project. Record source/master, output paths, runtimes, profiles, part transforms/material slots, intended overrides, and design details to preserve. Keep project-specific preferences in this record, not the global skill.

For FreeCAD + Bambu, configure once using [export-pipeline.md](references/export-pipeline.md), then run:

```text
<python> <skill>/scripts/export_project.py <project>/print-project.json
```

The script saves/reopens editable CAD, checks exported solids and closed meshes, renders a preview, creates aligned multipart geometry, exports through Bambu, pins process overrides, and checks CLI-reopened settings/material assignments. It logs details to disk and returns one compact JSON result. Unchanged inputs and outputs use a hash cache; `--force` bypasses it. This is packaging validation, not proof of fit, strength, support removability, or desktop preset persistence.

Create geometry with project modeling code first; export only after the requested geometry is settled. Do not regenerate an existing model solely to package it. Preserve native editability. The [enclosure example](scripts/build_enclosure.py) and [presentation example](scripts/save_presentation.py) are for new example projects, not generic exporters; they write beside themselves, so copy them before running.

## Load only relevant details

- Strength, assemblies, adhesion, support removal, or test pieces: [mechanical-design.md](references/mechanical-design.md).
- Text, fine detail, or multicolor changes: [appearance.md](references/appearance.md).
- First slicer setup, another slicer, or persistence troubleshooting: matching section of [slicer-projects.md](references/slicer-projects.md).

Do not load all references or reread unchanged scripts. Read narrow file ranges and log tails. Keep verbose output on disk. Use bounded waits instead of frequent short polling; do not run competing CAD writers/readers on the same file.

## Check and deliver

For changed appearance, inspect actual geometry and relevant sliced details. Show a focused early preview when consequential aesthetic choices remain open. Reuse established settings and validation unless affected by the change.

Deliver editable `.FCStd`, configured `.3mf`, and an accurate finished preview unless the user requests fewer formats. Keep one final configured 3MF per revision; remove temporary geometry packages after success. Give brief editing/assembly instructions. State changed print settings and consequential limitations; keep the complete settings in the project record or guide rather than repeating them each turn. Clearly identify checks not performed, including desktop reopen when unavailable. Do not describe CLI verification as desktop verification.
