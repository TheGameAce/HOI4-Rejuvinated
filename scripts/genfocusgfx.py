## Created by anvilpepe (quilki)


import re
import os
import argparse
import sys
import hashlib
import time
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Set, Optional, Dict, Tuple

def create_parser():
    """Create and configure the argument parser for genfocusgfx."""
    
    parser = argparse.ArgumentParser(
        prog='genfocusgfx',
        description='Generate focus graphics configuration for HOI4 mods',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
EXAMPLES:
  Basic usage:
    genfocusgfx focus_tree.txt output.gfx
  
  With mod integration:
    genfocusgfx focus_tree.txt output.gfx -m ./my_mod --icons-path gfx/interface/custom_goals
  
  Filter specific focuses:
    genfocusgfx focus_tree.txt output.gfx --focus-ids focus1 focus2 focus3
  
  Dry run for testing:
    genfocusgfx focus_tree.txt output.gfx --dry-run -vv
        """
    )

    # ========== POSITIONAL ARGUMENTS ==========
    parser.add_argument(
        'source',
        type=lambda x: validate_file_path(parser, x),
        help='Input file containing focus definitions (required)'
    )
    parser.add_argument(
        'output', 
        help='Output file for generated graphics configuration (required)'
    )

    # ========== GENERAL OPTIONS ==========
    general_group = parser.add_argument_group('GENERAL OPTIONS')
    verbosity_group = general_group.add_mutually_exclusive_group()
    
    verbosity_group.add_argument(
        '-v', '--verbose',
        action='count',
        default=0,
        help='''Increase verbosity level:
    -v   = INFO level
    -vv  = DEBUG level
    -vvv = TRACE level'''
    )
    
    verbosity_group.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress all non-essential output (errors only)'
    )
    
    general_group.add_argument(
        '--dry-run',
        action='store_true',
        help='''Simulate execution without writing files.
    Shows what would be created/changed.'''
    )
    
    general_group.add_argument(
        '--version',
        action='version',
        version='genfocusgfx 1.0.0',
        help='Display version information and exit'
    )

    # ========== IMAGE HANDLING ==========
    image_group = parser.add_argument_group('IMAGE CONFIGURATION')
    
    image_group.add_argument(
        '--default-image',
        type=str,
        default='gfx/interface/goals/goal_unknown.dds',
        help='''Path to default icon image (Paradox-compliant).
    Default: %(default)s'''
    )
    
    image_group.add_argument(
        '-p', '--generate-placeholder',
        action='store_true',
        help='Generate placeholder images for missing focus icons'
    )

    # ========== PATH CONFIGURATION ==========
    path_group = parser.add_argument_group('PATH CONFIGURATION')
    
    path_group.add_argument(
        '--icons-path',
        type=str,
        default='gfx/interface/goals',
        help='''Path to your mod's focus icon folder.
    Will search for images matching focus IDs.
    Requires --mod-root to be set.'''
    )
    
    path_group.add_argument(
        '-m', '--mod-root',
        type=str,
        metavar='PATH',
        help='''Your mod's root folder (contains descriptor.mod).
    Required for icon lookup and placeholder generation.'''
    )
    
    path_group.add_argument(
        '-g', '--game-root',
        type=str,
        metavar='PATH',
        help='''Path to HOI4 installation root.
    Used to locate default game assets.
    Example: "C:/Steam/steamapps/common/Hearts of Iron IV"'''
    )

    # ========== FOCUS FILTERING ==========
    filtering_group = parser.add_argument_group('FOCUS FILTERING')
    
    filtering_group.add_argument(
        '--focus-ids',
        type=str,
        nargs='+',
        metavar='ID',
        help='Process only specific focus IDs'
    )
    
    filtering_group.add_argument(
        '--exclude-ids',
        type=str,
        nargs='+',
        metavar='ID',
        help='Exclude specific focus IDs from processing'
    )
    
    filtering_group.add_argument(
        '--prefix',
        type=str,
        help='''Process only focuses with this prefix.
    Example: --prefix MOD_ (matches MOD_focus_name, not mod_focus_name)'''
    )
    
    filtering_group.add_argument(
        '--suffix',
        type=str,
        help='Process only focuses with this suffix'
    )

    # ========== OUTPUT CONTROL ==========
    output_group = parser.add_argument_group('OUTPUT CONTROL')
    
    output_group.add_argument(
        '--versioned-output',
        action='store_true',
        help='''Add metadata header with timestamp and source hash.
    Does not affect mod functionality.'''
    )
    
    output_group.add_argument(
        '--output-format',
        choices=['standard', 'compact', 'pretty'],
        default='standard',
        help='Formatting style for output file (default: %(default)s)'
    )
    
    output_group.add_argument(
        '--indent',
        type=int,
        default=4,
        choices=[2, 4, 8],
        help='Indentation level for output file (default: %(default)s)'
    )

    # ========== WORKFLOW & SAFETY ==========
    workflow_group = parser.add_argument_group('WORKFLOW & SAFETY')
    
    workflow_group.add_argument(
        '--report',
        type=str,
        metavar='FILE',
        help='Generate detailed report at specified path'
    )
    
    workflow_group.add_argument(
        '--report-format',
        choices=['txt', 'json', 'csv', 'md'],
        default='txt',
        help='Format for report file (default: %(default)s)'
    )
    
    workflow_group.add_argument(
        '--no-backup',
        action='store_true',
        help='Do not create backup files when overwriting'
    )
    
    safety_group = workflow_group.add_mutually_exclusive_group()
    
    safety_group.add_argument(
        '--force',
        action='store_true',
        help='Never prompt for confirmation (force all actions)'
    )
    
    safety_group.add_argument(
        '--interactive',
        action='store_true',
        help='Always prompt before overwriting files'
    )
    
    workflow_group.add_argument(
        '--unsafe',
        action='store_true',
        help='Disable all safety checks (NOT RECOMMENDED)'
    )

    # ========== VALIDATION ==========
    validation_group = parser.add_argument_group('VALIDATION')
    
    validation_group.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors'
    )

    return parser


def validate_file_path(parser, path):
    """Validate that a file path exists."""
    if not os.path.exists(path):
        parser.error(f"File not found: {path}")
    return path


def log_message(level: int, message: str, args):
    """Log messages based on verbosity level."""
    if args.quiet:
        return
    
    if level == 0:  # Always show errors
        print(f"ERROR: {message}", file=sys.stderr)
    elif level == 1 and args.verbose >= 1:  # Warnings at -v
        print(f"WARNING: {message}")
    elif level == 2 and args.verbose >= 1:  # Info at -v
        print(f"INFO: {message}")
    elif level == 3 and args.verbose >= 2:  # Debug at -vv
        print(f"DEBUG: {message}")
    elif level == 4 and args.verbose >= 3:  # Trace at -vvv
        print(f"TRACE: {message}")


def get_file_hash(filepath: str) -> str:
    """Calculate MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def find_icon_for_focus(focus_id: str, args, icon_report: Dict) -> Tuple[str, bool]:
    """Find the appropriate icon path for a focus. Returns (icon_path, icon_found)."""
    icon_found = False
    icon_path = args.default_image
    
    # Check mod root for custom icon
    if args.mod_root and args.icons_path:
        mod_icon_path = os.path.join(args.mod_root, args.icons_path)
        
        # Try different naming conventions and extensions
        naming_patterns = [
            focus_id,  # direct match
            f"GFX_{focus_id}",  # GFX_prefix
            f"goal_{focus_id.lower()}",  # goal_prefix (common pattern)
            f"GFX_goal_{focus_id}"  # GFX_goal_prefix
        ]
        
        possible_extensions = ['.dds', '.tga', '.png']
        
        for pattern in naming_patterns:
            for ext in possible_extensions:
                icon_file = os.path.join(mod_icon_path, f"{pattern}{ext}")
                if os.path.exists(icon_file):
                    relative_path = os.path.relpath(icon_file, args.mod_root)
                    icon_path = relative_path.replace('\\', '/')
                    icon_found = True
                    
                    # Record found icon in report
                    if focus_id not in icon_report['found_icons']:
                        icon_report['found_icons'][focus_id] = []
                    icon_report['found_icons'][focus_id].append({
                        'pattern': pattern,
                        'extension': ext,
                        'full_path': icon_file,
                        'relative_path': icon_path
                    })
                    
                    log_message(3, f"Found icon for {focus_id}: {icon_path}", args)
                    return icon_path, icon_found
    
    # Record missing icon in report
    if not icon_found:
        if focus_id not in icon_report['missing_icons']:
            icon_report['missing_icons'][focus_id] = {
                'patterns_tried': naming_patterns,
                'extensions_tried': possible_extensions,
                'icon_path': args.icons_path
            }
    
    return icon_path, icon_found


def clone_default_image_as_placeholder(focus_id: str, default_image_path: str, mod_root: str, icons_path: str, args) -> Optional[str]:
    """Clone the default image as a placeholder named GFX_{focus_id}.dds."""
    try:
        # Find the actual default image file
        default_image_full_path = find_default_image_file(default_image_path, args)
        if not default_image_full_path:
            log_message(1, f"Cannot find default image: {default_image_path}", args)
            return None
        
        # Determine the extension from the default image
        _, ext = os.path.splitext(default_image_full_path)
        if not ext:
            ext = '.dds'  # Default to .dds if no extension
        
        # Create the placeholder filename
        placeholder_filename = f"GFX_{focus_id}{ext}"
        
        # Create the destination path
        dest_dir = os.path.join(mod_root, icons_path)
        dest_path = os.path.join(dest_dir, placeholder_filename)
        
        # Ensure destination directory exists
        os.makedirs(dest_dir, exist_ok=True)
        
        # Copy the default image to create the placeholder
        shutil.copy2(default_image_full_path, dest_path)
        
        # Calculate relative path for Paradox format
        relative_path = os.path.relpath(dest_path, mod_root)
        relative_path = relative_path.replace('\\', '/')
        
        log_message(2, f"Created placeholder GFX_{focus_id}{ext} from default image", args)
        return relative_path
        
    except Exception as e:
        log_message(1, f"Failed to create placeholder for {focus_id}: {e}", args)
        return None


def find_default_image_file(default_image_path: str, args) -> Optional[str]:
    """Find the actual file for the default image path."""
    # Check if it's an absolute path
    if os.path.isabs(default_image_path):
        if os.path.exists(default_image_path):
            return default_image_path
    
    # Check in game root
    if args.game_root:
        game_path = os.path.join(args.game_root, default_image_path)
        if os.path.exists(game_path):
            return game_path
    
    # Check in mod root
    if args.mod_root:
        mod_path = os.path.join(args.mod_root, default_image_path)
        if os.path.exists(mod_path):
            return mod_path
    
    # Check relative to current directory
    if os.path.exists(default_image_path):
        return default_image_path
    
    return None


def filter_focus_ids(focus_ids: List[str], args) -> List[str]:
    """Apply filtering to focus IDs based on arguments."""
    filtered = set()
    for f in focus_ids:
        if f in filtered:
            log_message(1, f"Duplicate focus ID: {f}", args)
        filtered.add(f)
    
    # Apply prefix filter
    if args.prefix:
        filtered = {fid for fid in filtered if fid.startswith(args.prefix)}
    
    # Apply suffix filter
    if args.suffix:
        filtered = {fid for fid in filtered if fid.endswith(args.suffix)}
    
    # Apply focus-ids filter
    if args.focus_ids:
        focus_set = set(args.focus_ids)
        filtered = filtered.intersection(focus_set)
    
    # Apply exclude-ids filter
    if args.exclude_ids:
        exclude_set = set(args.exclude_ids)
        filtered = filtered - exclude_set
    
    # Convert back to list and sort
    return sorted(list(filtered))


def format_sprite(focus_id: str, icon_path: str, args, indent_level: int = 1) -> str:
    """Format a single sprite definition."""
    indent = ' ' * (args.indent * indent_level)
    
    if args.output_format == 'compact':
        return f'{indent}spriteType = {{ name = GFX_{focus_id} texturefile = {icon_path} }}\n spriteType = {{ name = GFX_{focus_id}_shine texturefile = {icon_path} }}\n'
    elif args.output_format == 'pretty':
        lines = [
            f'{indent}spriteType = {{',
            f'{indent}    name = GFX_{focus_id}',
            f'{indent}    texturefile = {icon_path}',
            f'{indent}}}'
        ] + [
            f'{indent}spriteType = {{',
            f'{indent}    name = GFX_{focus_id}_shine',
            f'{indent}    texturefile = {icon_path}',
            f'{indent}}}'
        ]
        return '\n'.join(lines) + '\n'
    else:  # standard format
        lines = [
            f'{indent}spriteType = {{',
            f'{indent}    name = GFX_{focus_id}',
            f'{indent}    texturefile = {icon_path}',
            f'{indent}}}'
        ] + [
            f'{indent}spriteType = {{',
            f'{indent}{indent}name = GFX_{focus_id}_shine',
            f'{indent}{indent}texturefile = {icon_path}',
            f'{indent}{indent}animation = {{',
            f'{indent}{indent}{indent}animationmaskfile = {icon_path}',
            f'{indent}{indent}{indent}animationtexturefile = gfx/interface/goals/shine_overlay.dds',
            f'{indent}{indent}{indent}animationrotation = -90.0',
            f'{indent}{indent}{indent}animationlooping = no',
            f'{indent}{indent}{indent}animationtime = 0.75',
            f'{indent}{indent}{indent}animationdelay = 0',
            f'{indent}{indent}{indent}animationblendmode = "add"',
            f'{indent}{indent}{indent}animationtype = "scrolling"',
            f'{indent}{indent}{indent}animationrotationoffset = {{ x = 0.0 y = 0.0 }}',
            f'{indent}{indent}{indent}animationtexturescale = {{ x = 1.0 y = 1.0 }}',
            f'{indent}{indent}}}',
            f'{indent}{indent}animation = {{',
            f'{indent}{indent}{indent}animationmaskfile = {icon_path}',
            f'{indent}{indent}{indent}animationtexturefile = gfx/interface/goals/shine_overlay.dds',
            f'{indent}{indent}{indent}animationrotation = 90.0',
            f'{indent}{indent}{indent}animationlooping = no',
            f'{indent}{indent}{indent}animationtime = 0.75',
            f'{indent}{indent}{indent}animationdelay = 0',
            f'{indent}{indent}{indent}animationblendmode = "add"',
            f'{indent}{indent}{indent}animationtype = "scrolling"',
            f'{indent}{indent}{indent}animationrotationoffset = {{ x = 0.0 y = 0.0 }}',
            f'{indent}{indent}{indent}animationtexturescale = {{ x = 1.0 y = 1.0 }}',
            f'{indent}{indent}}}',
            f'{indent}{indent}legacy_lazy_load = no',
            f'{indent}}}'
        ]
        return '\n'.join(lines) + '\n'


def generate_header(args, source_hash: str) -> str:
    """Generate versioned output header."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    lines = [
        '# Generated by genfocusgfx',
        f'# Timestamp: {timestamp}',
        f'# Source hash: {source_hash}',
        f'# Source file: {os.path.basename(args.source)}',
        '#',
        ''
    ]
    return '\n'.join(lines)


def generate_report(focus_ids: List[str], args, start_time: float, icon_report: Dict) -> Dict:
    """Generate report data including icon status."""
    end_time = time.time()
    duration = end_time - start_time
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'duration_seconds': round(duration, 2),
        'source_file': args.source,
        'output_file': args.output,
        'total_focuses': len(focus_ids),
        'focus_ids': focus_ids,
        'icon_statistics': {
            'total_found': len(icon_report['found_icons']),
            'total_missing': len(icon_report['missing_icons']),
            'total_placeholders_created': len(icon_report['placeholders_created'])
        },
        'found_icons': icon_report['found_icons'],
        'missing_icons': icon_report['missing_icons'],
        'placeholders_created': icon_report['placeholders_created'],
        'arguments': vars(args)
    }
    
    return report


def save_report(report: Dict, args):
    """Save report to file in requested format with detailed icon information."""
    if not args.report:
        return
    
    report_path = args.report
    os.makedirs(os.path.dirname(report_path) if os.path.dirname(report_path) else '.', exist_ok=True)
    
    if args.report_format == 'json':
        import json
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
    
    elif args.report_format == 'csv':
        import csv
        with open(report_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Focus ID', 'Status', 'Icon Path', 'Notes'])
            
            # Write found icons
            for focus_id, icons in report['found_icons'].items():
                for icon_info in icons:
                    writer.writerow([focus_id, 'FOUND', icon_info['relative_path'], f"Pattern: {icon_info['pattern']}"])
            
            # Write missing icons
            for focus_id, info in report['missing_icons'].items():
                writer.writerow([focus_id, 'MISSING', '', f"Tried {len(info['patterns_tried'])} patterns"])
            
            # Write placeholders created
            for focus_id, info in report['placeholders_created'].items():
                writer.writerow([focus_id, 'PLACEHOLDER_CREATED', info['icon_path'], 'Cloned from default image'])
    
    elif args.report_format == 'md':
        with open(report_path, 'w') as f:
            f.write(f"# genfocusgfx Report\n\n")
            f.write(f"**Timestamp**: {report['timestamp']}\n")
            f.write(f"**Duration**: {report['duration_seconds']} seconds\n")
            f.write(f"**Source**: {report['source_file']}\n")
            f.write(f"**Output**: {report['output_file']}\n")
            f.write(f"**Total Focuses**: {report['total_focuses']}\n\n")
            
            # Icon Statistics
            f.write("## Icon Statistics\n\n")
            stats = report['icon_statistics']
            f.write(f"- **Icons Found**: {stats['total_found']}\n")
            f.write(f"- **Icons Missing**: {stats['total_missing']}\n")
            f.write(f"- **Placeholders Created**: {stats['total_placeholders_created']}\n\n")
            
            # Missing Icons Section
            if report['missing_icons']:
                f.write("## Missing Icons\n\n")
                f.write("| Focus ID | Patterns Tried |\n")
                f.write("|----------|----------------|\n")
                for focus_id, info in report['missing_icons'].items():
                    patterns = ", ".join(info['patterns_tried'][:3])  # Show first 3 patterns
                    if len(info['patterns_tried']) > 3:
                        patterns += f" ... (+{len(info['patterns_tried']) - 3} more)"
                    f.write(f"| `{focus_id}` | {patterns} |\n")
                f.write("\n")
            
            # Found Icons Section
            if report['found_icons']:
                f.write("## Found Icons\n\n")
                f.write("| Focus ID | Icon Path | Pattern |\n")
                f.write("|----------|-----------|---------|\n")
                for focus_id, icons in report['found_icons'].items():
                    for icon_info in icons:
                        f.write(f"| `{focus_id}` | `{icon_info['relative_path']}` | {icon_info['pattern']} |\n")
                f.write("\n")
            
            # Placeholders Created Section
            if report['placeholders_created']:
                f.write("## Placeholders Created\n\n")
                f.write("| Focus ID | Placeholder Path |\n")
                f.write("|----------|------------------|\n")
                for focus_id, info in report['placeholders_created'].items():
                    f.write(f"| `{focus_id}` | `{info['icon_path']}` |\n")
                f.write("\n")
    
    else:  # txt format (default)
        with open(report_path, 'w') as f:
            f.write(f"genfocusgfx Report\n")
            f.write(f"=" * 60 + "\n\n")
            f.write(f"Timestamp: {report['timestamp']}\n")
            f.write(f"Duration: {report['duration_seconds']} seconds\n")
            f.write(f"Source: {report['source_file']}\n")
            f.write(f"Output: {report['output_file']}\n")
            f.write(f"Total Focuses: {report['total_focuses']}\n\n")
            
            # Icon Statistics
            f.write("ICON STATISTICS:\n")
            f.write("-" * 40 + "\n")
            stats = report['icon_statistics']
            f.write(f"Icons Found: {stats['total_found']}\n")
            f.write(f"Icons Missing: {stats['total_missing']}\n")
            f.write(f"Placeholders Created: {stats['total_placeholders_created']}\n\n")
            
            # Missing Icons Section
            if report['missing_icons']:
                f.write("MISSING ICONS:\n")
                f.write("-" * 40 + "\n")
                for focus_id, info in report['missing_icons'].items():
                    f.write(f"  {focus_id}:\n")
                    f.write(f"    Search path: {info['icon_path']}\n")
                    f.write(f"    Patterns tried: {', '.join(info['patterns_tried'][:3])}")
                    if len(info['patterns_tried']) > 3:
                        f.write(f" ... (+{len(info['patterns_tried']) - 3} more)")
                    f.write("\n")
                f.write("\n")
            
            # Found Icons Section
            if report['found_icons']:
                f.write("FOUND ICONS:\n")
                f.write("-" * 40 + "\n")
                for focus_id, icons in report['found_icons'].items():
                    f.write(f"  {focus_id}:\n")
                    for icon_info in icons:
                        f.write(f"    Pattern: {icon_info['pattern']}\n")
                        f.write(f"    Path: {icon_info['relative_path']}\n")
                f.write("\n")
            
            # Placeholders Created Section
            if report['placeholders_created']:
                f.write("PLACEHOLDERS CREATED:\n")
                f.write("-" * 40 + "\n")
                for focus_id, info in report['placeholders_created'].items():
                    f.write(f"  {focus_id}: {info['icon_path']}\n")
                f.write("\n")
            
            f.write("=" * 60 + "\n")


def create_backup(filepath: str, args):
    """Create backup of existing file."""
    if args.no_backup or not os.path.exists(filepath):
        return
    
    backup_path = f"{filepath}.backup"
    try:
        import shutil
        shutil.copy2(filepath, backup_path)
        log_message(2, f"Created backup: {backup_path}", args)
    except Exception as e:
        log_message(1, f"Failed to create backup: {e}", args)


def check_overwrite(filepath: str, args) -> bool:
    """Check if we should overwrite an existing file."""
    if not os.path.exists(filepath):
        return True
    
    if args.force:
        return True
    
    if args.interactive:
        response = input(f"File {filepath} already exists. Overwrite? [y/N]: ")
        return response.lower() in ['y', 'yes']
    
    # Default: don't overwrite without confirmation
    log_message(0, f"File {filepath} already exists. Use --force to overwrite or --interactive for prompt.", args)
    return False


def main(args):
    """Main processing function."""
    start_time = time.time()
    
    # Initialize icon report
    icon_report = {
        'found_icons': {},
        'missing_icons': {},
        'placeholders_created': {}
    }
    
    # Parse focus IDs from source file
    log_message(2, f"Reading focus definitions from {args.source}", args)
    
    try:
        with open(args.source, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        
        # Find all focus IDs using regex
        focus_matches = re.findall(r'focus\s*=\s*{\s*id\s*=\s*(\w+)', content, re.DOTALL)
        
        if not focus_matches:
            log_message(0, "No focus IDs found in source file", args)
            if args.strict:
                sys.exit(1)
            return
        
        log_message(2, f"Found {len(focus_matches)} focus IDs", args)
        
    except Exception as e:
        log_message(0, f"Error reading source file: {e}", args)
        sys.exit(1)
    
    # Apply filtering
    focus_ids = filter_focus_ids(focus_matches, args)
    
    if not focus_ids:
        log_message(1, "No focus IDs match the specified filters", args)
        if args.strict:
            sys.exit(1)
        return
    
    log_message(2, f"Processing {len(focus_ids)} focus IDs after filtering", args)
    
    # Check if we can overwrite output file
    if not check_overwrite(args.output, args):
        sys.exit(1)
    
    # Create backup if needed
    if not args.dry_run:
        create_backup(args.output, args)
    
    # Calculate source hash for versioned output
    source_hash = get_file_hash(args.source) if args.versioned_output else ""
    
    # Generate output content
    output_lines = []
    
    if args.versioned_output:
        output_lines.append(generate_header(args, source_hash))
    
    output_lines.append('spriteTypes = {\n')
    
    for focus_id in focus_ids:
        # Find appropriate icon
        icon_path, icon_found = find_icon_for_focus(focus_id, args, icon_report)
        
        # Generate placeholder if requested and icon not found
        if not icon_found and args.generate_placeholder and args.mod_root and args.icons_path:
            new_icon_path = clone_default_image_as_placeholder(
                focus_id, args.default_image, args.mod_root, args.icons_path, args
            )
            if new_icon_path:
                icon_path = new_icon_path
                icon_report['placeholders_created'][focus_id] = {
                    'icon_path': new_icon_path,
                    'source_image': args.default_image
                }
                log_message(2, f"Created placeholder for {focus_id} at {new_icon_path}", args)
        
        # Format sprite definition
        sprite_def = format_sprite(focus_id, icon_path, args)
        output_lines.append(sprite_def)
        
        log_message(3, f"Processed focus: {focus_id} -> {icon_path}", args)
    
    output_lines.append('}\n')
    
    # Write output or show dry-run preview
    if args.dry_run:
        print("\n=== DRY RUN - No files will be written ===\n")
        print(''.join(output_lines))
        print(f"\nWould write {len(focus_ids)} focus definitions to {args.output}")
        
        # Show icon statistics even in dry run
        found_count = len(icon_report['found_icons'])
        missing_count = len(icon_report['missing_icons'])
        print(f"\nIcon Statistics (dry run):")
        print(f"  Icons found: {found_count}")
        print(f"  Icons missing: {missing_count}")
        if args.generate_placeholder and args.mod_root:
            print(f"  Placeholders would be created: {missing_count}")
        
        # List missing icons
        if missing_count > 0:
            print(f"\nMissing Icons:")
            for focus_id in icon_report['missing_icons'].keys():
                print(f"  - {focus_id}")
    else:
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else '.', exist_ok=True)
            
            with open(args.output, 'w', encoding='utf-8') as f:
                f.writelines(output_lines)
            
            log_message(2, f"Successfully wrote {len(focus_ids)} focus definitions to {args.output}", args)
            
            # Show icon statistics
            found_count = len(icon_report['found_icons'])
            missing_count = len(icon_report['missing_icons'])
            placeholder_count = len(icon_report['placeholders_created'])
            
            log_message(2, f"Icon Statistics:", args)
            log_message(2, f"  Icons found: {found_count}", args)
            log_message(2, f"  Icons missing: {missing_count}", args)
            if args.generate_placeholder:
                log_message(2, f"  Placeholders created: {placeholder_count}", args)
            
            # Log missing icons if any
            if missing_count > 0 and args.verbose >= 1:
                log_message(1, f"Missing icons for {missing_count} focuses. Check report for details.", args)
            
            # Generate report if requested
            if args.report:
                report = generate_report(focus_ids, args, start_time, icon_report)
                save_report(report, args)
                log_message(2, f"Report saved to {args.report}", args)
                
        except Exception as e:
            log_message(0, f"Error writing output file: {e}", args)
            sys.exit(1)
    
    # Final summary
    duration = time.time() - start_time
    log_message(2, f"Completed in {duration:.2f} seconds", args)


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    
    # Show help if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    # Validate argument combinations
    if (args.icons_path != 'gfx/interface/goals' or args.generate_placeholder) and not args.mod_root:
        parser.error("--mod-root is required when using --icons-path or --generate-placeholder")
    
    # Run main function
    try:
        main(args)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        if args.verbose >= 3:
            import traceback
            traceback.print_exc()
        else:
            print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)