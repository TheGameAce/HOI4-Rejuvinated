This directory contains all custom focus icons for trees added by the Rejuvenated mod. Please organize icons according to the guidelines below.

## Folder structure

Country-specific subfolders — Icons for a particular country go in a folder named after its tag (e.g., `CUB/` for Cuba, `HAI/` for Haiti).

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
