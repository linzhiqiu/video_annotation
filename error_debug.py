#!/usr/bin/env python3
"""
Git History Analyzer - Check for file additions/deletions in recent commits
and analyze scripts for potential file deletion operations.
"""

import subprocess
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


def run_git_command(cmd: List[str]) -> str:
    """Run a git command and return output"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}")
        print(f"stderr: {e.stderr}")
        return ""


def get_last_n_commits(n: int = 4) -> List[str]:
    """Get the last N commit hashes"""
    output = run_git_command(['git', 'log', f'-{n}', '--pretty=format:%H'])
    return output.strip().split('\n') if output else []


def analyze_commit(commit_hash: str) -> Dict:
    """Analyze a single commit for file changes"""
    # Get commit info
    commit_info = run_git_command([
        'git', 'show', '--stat', '--pretty=format:%H%n%an%n%ae%n%ad%n%s',
        commit_hash
    ])
    
    lines = commit_info.split('\n')
    if len(lines) < 5:
        return {}
    
    result = {
        'hash': lines[0],
        'author': lines[1],
        'email': lines[2],
        'date': lines[3],
        'message': lines[4],
        'py_files': {'added': [], 'modified': [], 'deleted': []},
        'caption_output': {'added': 0, 'deleted': 0, 'files': []}
    }
    
    # Get detailed diff stats
    diff_output = run_git_command([
        'git', 'diff-tree', '--no-commit-id', '--name-status', '-r', commit_hash
    ])
    
    for line in diff_output.strip().split('\n'):
        if not line:
            continue
            
        parts = line.split('\t')
        if len(parts) < 2:
            continue
            
        status = parts[0]
        filepath = parts[1]
        
        # Track Python files
        if filepath.endswith('.py'):
            if status == 'A':
                result['py_files']['added'].append(filepath)
            elif status == 'M':
                result['py_files']['modified'].append(filepath)
            elif status == 'D':
                result['py_files']['deleted'].append(filepath)
        
        # Track caption/output_captions/ folder
        if 'caption/output_captions/' in filepath:
            if status == 'A':
                result['caption_output']['added'] += 1
                result['caption_output']['files'].append(('A', filepath))
            elif status == 'D':
                result['caption_output']['deleted'] += 1
                result['caption_output']['files'].append(('D', filepath))
    
    return result


def find_video_json_for_caption(video_id: str, video_urls_files: List[str]) -> List[str]:
    """
    Find which JSON files in video_urls/ contain the given video_id.
    Based on logic from caption/apps/app.py
    """
    matching_files = []
    
    for json_file in video_urls_files:
        try:
            with open(json_file, 'r') as f:
                video_urls = json.load(f)
                
            # Check if any URL contains the video_id
            for url in video_urls:
                # Extract video_id from URL (handles various URL formats)
                if video_id in url:
                    matching_files.append(json_file)
                    break
        except Exception as e:
            print(f"Warning: Could not read {json_file}: {e}")
    
    return matching_files


def analyze_script_for_deletions(script_path: str) -> Dict:
    """Analyze a Python script for file deletion operations"""
    result = {
        'path': script_path,
        'exists': False,
        'has_file_deletion': False,
        'deletion_patterns': []
    }
    
    script_file = Path(script_path)
    if not script_file.exists():
        return result
    
    result['exists'] = True
    
    try:
        with open(script_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        # Patterns that indicate file deletion
        deletion_indicators = [
            (r'os\.remove\s*\(', 'os.remove()'),
            (r'os\.unlink\s*\(', 'os.unlink()'),
            (r'Path\([^)]+\)\.unlink\s*\(', 'Path.unlink()'),
            (r'shutil\.rmtree\s*\(', 'shutil.rmtree()'),
            (r'\.unlink\s*\(', '.unlink()'),
            (r'pathlib.*unlink', 'pathlib unlink'),
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern, pattern_name in deletion_indicators:
                if re.search(pattern, line):
                    result['has_file_deletion'] = True
                    result['deletion_patterns'].append({
                        'line_number': i,
                        'pattern': pattern_name,
                        'code': line.strip()
                    })
        
    except Exception as e:
        print(f"Error reading {script_path}: {e}")
    
    return result


def get_video_urls_files() -> List[str]:
    """Get list of video_urls JSON files from the project"""
    video_urls_dir = Path('video_urls')
    if not video_urls_dir.exists():
        return []
    
    json_files = []
    for json_file in video_urls_dir.rglob('*.json'):
        json_files.append(str(json_file))
    
    return sorted(json_files)


def analyze_single_commit_detailed(commit_hash: str):
    """Detailed analysis of a single commit showing ALL changes"""
    print("=" * 80)
    print(f"DETAILED ANALYSIS OF COMMIT: {commit_hash[:8]}")
    print("=" * 80)
    
    # Get commit info
    commit_info = run_git_command([
        'git', 'show', '--pretty=format:%H%n%an%n%ae%n%ad%n%s', '--name-status',
        commit_hash
    ])
    
    lines = commit_info.split('\n')
    print(f"Hash:    {lines[0]}")
    print(f"Author:  {lines[1]} <{lines[2]}>")
    print(f"Date:    {lines[3]}")
    print(f"Message: {lines[4]}")
    print()
    
    # Get ALL file changes
    diff_output = run_git_command([
        'git', 'diff-tree', '--no-commit-id', '--name-status', '-r', commit_hash
    ])
    
    changes = {
        'added': [],
        'modified': [],
        'deleted': [],
        'renamed': []
    }
    
    for line in diff_output.strip().split('\n'):
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) < 2:
            continue
        
        status = parts[0]
        filepath = parts[1]
        
        if status == 'A':
            changes['added'].append(filepath)
        elif status == 'M':
            changes['modified'].append(filepath)
        elif status == 'D':
            changes['deleted'].append(filepath)
        elif status.startswith('R'):
            changes['renamed'].append((parts[1], parts[2] if len(parts) > 2 else ''))
    
    # Print summary
    print("SUMMARY:")
    print(f"  Files Added:    {len(changes['added'])}")
    print(f"  Files Modified: {len(changes['modified'])}")
    print(f"  Files Deleted:  {len(changes['deleted'])}")
    print(f"  Files Renamed:  {len(changes['renamed'])}")
    print()
    
    # Group deletions by folder
    if changes['deleted']:
        print("DELETED FILES BY FOLDER:")
        folder_counts = {}
        for filepath in changes['deleted']:
            folder = '/'.join(filepath.split('/')[:-1]) if '/' in filepath else '.'
            folder_counts[folder] = folder_counts.get(folder, 0) + 1
        
        for folder, count in sorted(folder_counts.items(), key=lambda x: -x[1]):
            print(f"  {folder}: {count} files")
        print()
        
        # Show first 20 deleted files
        print(f"FIRST 20 DELETED FILES (out of {len(changes['deleted'])}):")
        for filepath in changes['deleted'][:20]:
            print(f"  - {filepath}")
        if len(changes['deleted']) > 20:
            print(f"  ... and {len(changes['deleted']) - 20} more")
        print()
    
    # Show added files
    if changes['added']:
        print(f"ADDED FILES ({len(changes['added'])}):")
        for filepath in changes['added'][:20]:
            print(f"  + {filepath}")
        if len(changes['added']) > 20:
            print(f"  ... and {len(changes['added']) - 20} more")
        print()
    
    # Show modified files
    if changes['modified']:
        print(f"MODIFIED FILES ({len(changes['modified'])}):")
        for filepath in changes['modified']:
            print(f"  M {filepath}")
        print()
    
    return changes


def compare_commits(commit1: str, commit2: str):
    """Compare two commits to see what changed between them"""
    print("=" * 80)
    print(f"COMPARING COMMITS")
    print(f"FROM: {commit2[:8]} → TO: {commit1[:8]}")
    print("=" * 80)
    print()
    
    # Get files in each commit
    files1 = set(run_git_command([
        'git', 'ls-tree', '-r', '--name-only', commit1
    ]).strip().split('\n'))
    
    files2 = set(run_git_command([
        'git', 'ls-tree', '-r', '--name-only', commit2
    ]).strip().split('\n'))
    
    # Calculate differences
    only_in_commit1 = files1 - files2
    only_in_commit2 = files2 - files1
    in_both = files1 & files2
    
    print(f"Files only in {commit1[:8]} (newer):  {len(only_in_commit1)}")
    print(f"Files only in {commit2[:8]} (older):  {len(only_in_commit2)}")
    print(f"Files in both commits:                {len(in_both)}")
    print()
    
    # Analyze caption/output_captions specifically
    caption_only_new = [f for f in only_in_commit1 if f.startswith('caption/output_captions/')]
    caption_only_old = [f for f in only_in_commit2 if f.startswith('caption/output_captions/')]
    
    print("CAPTION/OUTPUT_CAPTIONS FOLDER:")
    print(f"  Files only in newer commit: {len(caption_only_new)}")
    print(f"  Files only in older commit: {len(caption_only_old)}")
    print()
    
    if caption_only_old:
        print(f"  First 20 files LOST from caption/output_captions/:")
        for f in sorted(caption_only_old)[:20]:
            print(f"    - {f}")
        if len(caption_only_old) > 20:
            print(f"    ... and {len(caption_only_old) - 20} more")
    
    # Analyze caption/output_critiques specifically
    critique_only_new = [f for f in only_in_commit1 if f.startswith('caption/output_critiques/')]
    critique_only_old = [f for f in only_in_commit2 if f.startswith('caption/output_critiques/')]
    
    print()
    print("CAPTION/OUTPUT_CRITIQUES FOLDER:")
    print(f"  Files only in newer commit: {len(critique_only_new)}")
    print(f"  Files only in older commit: {len(critique_only_old)}")
    print()
    
    return {
        'only_in_new': only_in_commit1,
        'only_in_old': only_in_commit2,
        'caption_lost': caption_only_old,
        'caption_added': caption_only_new,
        'critique_lost': critique_only_old,
        'critique_added': critique_only_new
    }


def show_all_changes_between_commits(older_commit: str, newer_commit: str):
    """Show ALL changes (deleted, modified, added) between two commits"""
    print("=" * 80)
    print(f"ALL CHANGES BETWEEN COMMITS")
    print(f"FROM (older): {older_commit[:8]} → TO (newer): {newer_commit[:8]}")
    print("=" * 80)
    print()
    
    # Get detailed diff
    diff_output = run_git_command([
        'git', 'diff', '--name-status', older_commit, newer_commit
    ])
    
    changes = {
        'deleted': [],
        'modified': [],
        'added': []
    }
    
    for line in diff_output.strip().split('\n'):
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) < 2:
            continue
        
        status = parts[0]
        filepath = parts[1]
        
        if status == 'D':
            changes['deleted'].append(filepath)
        elif status == 'M':
            changes['modified'].append(filepath)
        elif status == 'A':
            changes['added'].append(filepath)
    
    # Print summary
    print("SUMMARY:")
    print(f"  Deleted:  {len(changes['deleted'])} files")
    print(f"  Modified: {len(changes['modified'])} files")
    print(f"  Added:    {len(changes['added'])} files")
    print()
    
    # Show ALL modified files (especially important for scripts)
    if changes['modified']:
        print("=" * 80)
        print("MODIFIED FILES (will be restored to older version):")
        print("=" * 80)
        
        # Separate by type
        py_files = [f for f in changes['modified'] if f.endswith('.py')]
        json_files = [f for f in changes['modified'] if f.endswith('.json')]
        other_files = [f for f in changes['modified'] if not f.endswith('.py') and not f.endswith('.json')]
        
        if py_files:
            print(f"\nPython scripts ({len(py_files)}):")
            for filepath in sorted(py_files):
                print(f"  M {filepath}")
        
        if json_files:
            print(f"\nJSON files ({len(json_files)}):")
            for filepath in sorted(json_files):
                print(f"  M {filepath}")
        
        if other_files:
            print(f"\nOther files ({len(other_files)}):")
            for filepath in sorted(other_files):
                print(f"  M {filepath}")
        print()
    
    # Show deleted files by folder
    if changes['deleted']:
        print("=" * 80)
        print("DELETED FILES (will be restored):")
        print("=" * 80)
        
        # Separate by location
        caption_output = [f for f in changes['deleted'] if f.startswith('caption/output_captions/')]
        critique_output = [f for f in changes['deleted'] if f.startswith('caption/output_critiques/')]
        scripts = [f for f in changes['deleted'] if f.endswith('.py')]
        other_deleted = [f for f in changes['deleted'] if f not in caption_output + critique_output + scripts]
        
        print(f"\nDeleted from caption/output_captions/: {len(caption_output)} files")
        print(f"Deleted from caption/output_critiques/: {len(critique_output)} files")
        
        if scripts:
            print(f"\nDeleted Python scripts ({len(scripts)}):")
            for filepath in sorted(scripts):
                print(f"  - {filepath}")
        
        if other_deleted:
            print(f"\nOther deleted files ({len(other_deleted)}):")
            for filepath in sorted(other_deleted):
                print(f"  - {filepath}")
        
        # Show sample from each category
        if caption_output:
            print(f"\nSample from caption/output_captions/ (first 10):")
            for filepath in sorted(caption_output)[:10]:
                print(f"  - {filepath}")
        
        if critique_output:
            print(f"\nSample from caption/output_critiques/ (first 10):")
            for filepath in sorted(critique_output)[:10]:
                print(f"  - {filepath}")
        print()
    
    # Show added files (these will be LOST if you restore everything)
    if changes['added']:
        print("=" * 80)
        print("ADDED FILES (WARNING: will be LOST if you restore everything!):")
        print("=" * 80)
        
        # Separate by type and location
        critique_added = [f for f in changes['added'] if f.startswith('caption/output_critiques/')]
        py_added = [f for f in changes['added'] if f.endswith('.py')]
        other_added = [f for f in changes['added'] if f not in critique_added + py_added]
        
        if critique_added:
            print(f"\nAdded to caption/output_critiques/: {len(critique_added)} files")
            print("Sample (first 10):")
            for filepath in sorted(critique_added)[:10]:
                print(f"  + {filepath}")
        
        if py_added:
            print(f"\nAdded Python scripts ({len(py_added)}):")
            for filepath in sorted(py_added):
                print(f"  + {filepath}")
        
        if other_added:
            print(f"\nOther added files ({len(other_added)}):")
            for filepath in sorted(other_added):
                print(f"  + {filepath}")
        print()
    
    return changes


def create_selective_recovery_plan(changes):
    """Create recovery plan that keeps new files but restores deleted/modified ones"""
    print("=" * 80)
    print("SELECTIVE RECOVERY PLAN - RESTORE DELETED/MODIFIED, KEEP NEW FILES")
    print("=" * 80)
    print()
    print("Strategy: Restore all deleted and modified files WITHOUT removing the new files")
    print()
    
    deleted_folders = set()
    for f in changes['deleted']:
        folder = '/'.join(f.split('/')[:-1]) if '/' in f else '.'
        deleted_folders.add(folder)
    
    print("RECOMMENDED APPROACH:")
    print()
    print("# Restore by folder to avoid removing new files:")
    
    # Check for root-level deletions
    root_deleted = [f for f in changes['deleted'] if '/' not in f]
    if root_deleted:
        print("\n# Root-level deleted files:")
        for f in root_deleted:
            print(f"git checkout e0928799 -- {f}")
    
    # Restore major folders
    major_folders = ['caption/output_captions', 'caption/output_critiques']
    for folder in major_folders:
        folder_files = [f for f in changes['deleted'] if f.startswith(folder + '/')]
        if folder_files:
            print(f"\n# Restore {folder}/ ({len(folder_files)} files)")
            print(f"git checkout e0928799 -- {folder}/")
    
    # Show modified files that will be restored
    if changes['modified']:
        print(f"\n# Also restore {len(changes['modified'])} modified files:")
        if len(changes['modified']) <= 10:
            for f in changes['modified']:
                print(f"git checkout e0928799 -- {f}")
        else:
            print("# (Restore individual files or use the command below)")
    
    print("\n# Then commit everything:")
    print("git add -A")
    print("git commit -m 'Restore deleted and modified files from e0928799'")
    print("git push")
    print()
    print("=" * 80)
    print("NOTE: This approach will KEEP the 1,025 newly added files!")
    print("=" * 80)


def main():
    import sys
    
    # Check if specific commit hash is provided
    if len(sys.argv) > 1 and sys.argv[1] == '--analyze-commit':
        if len(sys.argv) < 3:
            print("Usage: python error_debug.py --analyze-commit <commit_hash>")
            return
        commit_hash = sys.argv[2]
        analyze_single_commit_detailed(commit_hash)
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == '--compare':
        if len(sys.argv) < 4:
            print("Usage: python error_debug.py --compare <newer_commit> <older_commit>")
            print("Example: python error_debug.py --compare e42a1f0f e0928799")
            return
        compare_commits(sys.argv[2], sys.argv[3])
        create_recovery_plan()
        return
    
    if len(sys.argv) > 1 and sys.argv[1] == '--show-all-changes':
        if len(sys.argv) < 4:
            print("Usage: python error_debug.py --show-all-changes <older_commit> <newer_commit>")
            print("Example: python error_debug.py --show-all-changes e0928799 e42a1f0f")
            return
        changes = show_all_changes_between_commits(sys.argv[2], sys.argv[3])
        create_selective_recovery_plan(changes)
        return
    
    print("=" * 80)
    print("GIT HISTORY ANALYSIS - Last 4 Commits")
    print("=" * 80)
    print()
    import sys
    
    # Check if specific commit hash is provided
    if len(sys.argv) > 1 and sys.argv[1] == '--analyze-commit':
        if len(sys.argv) < 3:
            print("Usage: python error_debug.py --analyze-commit <commit_hash>")
            return
        commit_hash = sys.argv[2]
        analyze_single_commit_detailed(commit_hash)
        return
    
    print("=" * 80)
    print("GIT HISTORY ANALYSIS - Last 4 Commits")
    print("=" * 80)
    print()
    
    # Get last 4 commits
    commits = get_last_n_commits(4)
    
    if not commits:
        print("No commits found!")
        return
    
    print(f"Analyzing {len(commits)} commits...\n")
    
    # Analyze each commit
    for i, commit_hash in enumerate(commits, 1):
        print(f"\n{'='*80}")
        print(f"COMMIT {i}/{len(commits)}: {commit_hash[:8]}")
        print(f"{'='*80}")
        
        analysis = analyze_commit(commit_hash)
        
        if not analysis:
            print("Could not analyze commit")
            continue
        
        print(f"Author:  {analysis['author']} <{analysis['email']}>")
        print(f"Date:    {analysis['date']}")
        print(f"Message: {analysis['message']}")
        print()
        
        # Python files
        if any(analysis['py_files'].values()):
            print("Python Files Changed:")
            if analysis['py_files']['added']:
                print(f"  Added ({len(analysis['py_files']['added'])}):")
                for f in analysis['py_files']['added']:
                    print(f"    + {f}")
            if analysis['py_files']['modified']:
                print(f"  Modified ({len(analysis['py_files']['modified'])}):")
                for f in analysis['py_files']['modified']:
                    print(f"    M {f}")
            if analysis['py_files']['deleted']:
                print(f"  Deleted ({len(analysis['py_files']['deleted'])}):")
                for f in analysis['py_files']['deleted']:
                    print(f"    - {f}")
        else:
            print("No Python files changed")
        
        print()
        
        # caption/output_captions/ changes
        if analysis['caption_output']['added'] > 0 or analysis['caption_output']['deleted'] > 0:
            print(f"caption/output_captions/ folder changes:")
            print(f"  Files added:   {analysis['caption_output']['added']}")
            print(f"  Files deleted: {analysis['caption_output']['deleted']}")
            
            if analysis['caption_output']['files']:
                print(f"  Details:")
                for status, filepath in analysis['caption_output']['files'][:10]:  # Show first 10
                    symbol = '+' if status == 'A' else '-'
                    print(f"    {symbol} {filepath}")
                
                if len(analysis['caption_output']['files']) > 10:
                    print(f"    ... and {len(analysis['caption_output']['files']) - 10} more files")
                
                # Try to trace which JSON contains these videos
                if analysis['caption_output']['added'] > 0:
                    print("\n  Tracing added files to video_urls JSON:")
                    video_urls_files = get_video_urls_files()
                    
                    for status, filepath in analysis['caption_output']['files']:
                        if status == 'A':
                            # Extract video_id from filepath
                            # Example: caption/output_captions/subject_description/video_123_feedback.json
                            match = re.search(r'video_([^_/]+)', filepath)
                            if match:
                                video_id = match.group(1)
                                matching_jsons = find_video_json_for_caption(video_id, video_urls_files)
                                if matching_jsons:
                                    print(f"    Video {video_id}: {', '.join(matching_jsons)}")
        else:
            print("No changes in caption/output_captions/ folder")
    
    # Analyze specific scripts for file deletion capability
    print("\n\n" + "=" * 80)
    print("SCRIPT ANALYSIS - Checking for File Deletion Capabilities")
    print("=" * 80)
    print()
    
    scripts_to_check = [
        'caption/export.py',
        'caption/generate_critiques.py'
    ]
    
    for script_path in scripts_to_check:
        print(f"\nAnalyzing: {script_path}")
        print("-" * 80)
        
        analysis = analyze_script_for_deletions(script_path)
        
        if not analysis['exists']:
            print(f"  ❌ File not found!")
            continue
        
        if analysis['has_file_deletion']:
            print(f"  ⚠️  WARNING: File deletion operations detected!")
            print(f"  Found {len(analysis['deletion_patterns'])} potential deletion pattern(s):")
            for pattern in analysis['deletion_patterns']:
                print(f"    Line {pattern['line_number']}: {pattern['pattern']}")
                print(f"      Code: {pattern['code']}")
        else:
            print(f"  ✅ No file deletion operations found")
    
    # Additional analysis for branch switching scenario
    print("\n\n" + "=" * 80)
    print("BRANCH SWITCHING ANALYSIS")
    print("=" * 80)
    print()
    print("Checking for potential issues from branch switching (git checkout -b camerabench-pro)...")
    print()
    
    # Get current branch
    current_branch = run_git_command(['git', 'branch', '--show-current']).strip()
    print(f"Current branch: {current_branch}")
    
    # Check reflog for recent branch operations
    reflog = run_git_command(['git', 'reflog', '-20'])
    
    checkout_operations = []
    for line in reflog.split('\n'):
        if 'checkout:' in line.lower() or 'branch:' in line.lower():
            checkout_operations.append(line.strip())
    
    if checkout_operations:
        print(f"\nRecent branch operations (last {len(checkout_operations)}):")
        for op in checkout_operations:
            print(f"  {op}")
        
        print("\nNote: Branch switching itself doesn't delete files, but if you:")
        print("  1. Switched to a new branch (camerabench-pro)")
        print("  2. Made commits on that branch")
        print("  3. Switched back to main")
        print("  4. Then committed again on main")
        print("  → Files committed on camerabench-pro won't appear on main!")
    else:
        print("No recent branch checkout operations found in reflog")
    
    print("\n" + "=" * 80)
    print("Analysis Complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()