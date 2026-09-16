# Skill repository principles

- Maintain reusable design guidance, scripts and lightweight mechanical parameters. Do not turn references into project reports or a conversation diary.
- Do not include dated narratives, user quotes, decisions, approval history, experiment chronology, abandoned variants or session-specific commentary.
- Use descriptive mechanism names. Do not use "accepted" labels or unexplained variant identifiers such as "A" or "B" in names, paths or prose.
- State dimensions directly. For example, write "Tooth shoulder distance from root: 14 mm" without commentary about previous interpretations or alternatives.
- Mechanical references cover geometry, function, fit, assembly and design constraints. Do not include printer models, nozzle sizes, layer settings, infill, slicer settings, plate transforms or print-run records in these references or their parameter files.
- Keep reusable slicer/export instructions in their dedicated guides; keep project-specific print setup in the local project.
- Never commit or upload FreeCAD files, 3MF files, generated CAD/mesh binaries, logs, test reports, export caches or other generated project artifacts. Never force-add ignored binaries. Keep those outside this repository.
- Preserve useful engineering lessons as concise design rules, without the narrative of how they were learned. State mechanical limits without presenting a test log.
- Before committing, inspect the staged file list and diff for prohibited artifacts, diary language, variant labels and project-specific settings. Keep the main skill concise and load detailed references only when relevant.
