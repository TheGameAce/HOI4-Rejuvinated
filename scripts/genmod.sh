# Generates .mod file for HOI4 launcher to recognize Rejuvinated/.
# You could do it by hand.

#!/usr/bin/bash

PROJROOT="$(realpath $(dirname $0)/..)"
MODSFOLDER="/home/$USER/.local/share/Paradox Interactive/Hearts of Iron IV/mod"

echo "Project root is $PROJROOT"
echo "Generating Rejuvinated.mod file at $MODSFOLDER..."

cp -fv "$PROJROOT/Rejuvinated/descriptor.mod" "$MODSFOLDER/Rejuvinated.mod"
echo "" >> "$MODSFOLDER/Rejuvinated.mod" #newline
echo "path=\"$PROJROOT/Rejuvinated\"" >> "$MODSFOLDER/Rejuvinated.mod"
