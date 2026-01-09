This directory contains all custom focus icons for trees added by the Rejuvenated mod. Please organize icons according to the guidelines below.

## Folder structure

`shared/` — Icons that are used across multiple focus trees.

`generic/` — Generic focus icons (do not mix with shared icons).

Country-specific subfolders — Icons for a particular country go in a folder named after its tag (e.g., `CUB/` for Cuba, `HAI/` for Haiti).

## Required and optional files

attributions.yml — Lists original icon authors (only for icons created specifically for that folder). Icons taken from shared/ do not need attribution here.
README.md (optional) — Describes the icon pack, design choices, naming conventions, or focus tree authorship.

## Using genfocusgfx with Placeholders

When generating focus graphics, you can use the `--generate-placeholders` option to create temporary icons from the default image (`gfx/interface/goals/goal_unknown.dds` if unspecified). For a focus named `focus_example`, this will produce `GFX_focus_example.dds`.

### Command example

Assuming your PWD is repository root

**Bare minimum**
```bash
python3 scripts/genfocusgfx.py Rejuvinated/common/national_focus/Haiti.txt Rejuvinated/interface/goals/Haiti.gfx --generate-placeholders --mod-root Rejuvinated --icons-path gfx/interface/goals/HAI 
```
**With custom placeholder**
```bash
python3 scripts/genfocusgfx.py Rejuvinated/common/national_focus/Haiti.txt Rejuvinated/interface/goals/Haiti.gfx --generate-placeholders --mod-root Rejuvinated --icons-path gfx/interface/goals/HAI --default-image Rejuvinated/gfx/interface/goals/shared/RJ_placeholder.dds 
```

## Getting Started

A ready-to-copy template is available in `00_template/`. Duplicate and adapt it for your own focus tree.