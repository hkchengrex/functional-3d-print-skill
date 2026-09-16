# Functional 3D Print Skill

Turn an idea into a functional 3D print with Codex. Get an **editable FreeCAD model, a 3MF project for your slicer, and clear print settings**.

Open the FreeCAD file to adjust dimensions yourself, or ask Codex to refine the design.

## Features

Repository content is limited to reusable instructions, scripts and lightweight design parameters. Keep FreeCAD and 3MF outputs local; do not commit them or force-add ignored binaries. Use descriptive mechanism names rather than approval labels for references.

- Design holders, mounts, enclosures, and multipart assemblies.
- Account for fit, strength, print orientation, adhesion, and support removal.
- Choose lettering that suits the design and your nozzle.
- Reduce color changes and waste in multicolor prints.
- Try small test pieces before committing to a larger print.
- Preview important styling, fonts, and color choices before the design is finalized.
- Match validation to the change, with focused checks for small revisions.
- Reuse scripted FreeCAD and Bambu exports with saved project settings and cached results.

Works with **Bambu Studio, OrcaSlicer, PrusaSlicer, and UltiMaker Cura**. Use your preferred print settings or let Codex suggest them.

## Install

You'll need Codex, FreeCAD, and your preferred slicer installed.

Paste this into Codex:

```text
Use $skill-installer to install the skill from:
https://github.com/hkchengrex/functional-3d-print-skill/tree/main/skills/freecad-editable-printing
```

## Try it

```text
Use $freecad-editable-printing to design a card holder with
"HOLDER" lettering. I use Bambu Studio with an A1,
have 0.4 mm and 0.2 mm nozzles, and print PLA.
```

Describe what you want to make and share any dimensions or preferences you know. Codex will ask for important missing details and help you work through the design.

## What you get

- **FreeCAD file (.FCStd)** — an editable model with adjustable dimensions.
- **Slicer project (.3mf)** — the model arranged for printing with your settings.
- **Preview and print guidance** — including nozzle, material, layer height, walls, infill, supports, brim, and orientation.

## Repeatable exports

For FreeCAD and Bambu Studio, configure a `print-project.json` once, then run:

```text
python skills/freecad-editable-printing/scripts/export_project.py /path/to/print-project.json
```

The pipeline saves and reopens an editable CAD copy, renders a preview, checks solids and meshes, and creates a native Bambu project with verified settings and filament assignments. Detailed logs stay on disk; successful runs return a short JSON summary. Unchanged inputs and outputs use a cache.

See the [manifest and export guide](skills/freecad-editable-printing/references/export-pipeline.md) for setup, dependencies, supported features, and limitations. Geometry design remains a separate step. The automation supports single-plate Bambu projects; other slicers use their native project workflows. CLI checks do not establish desktop preset persistence or physical fit and strength.
