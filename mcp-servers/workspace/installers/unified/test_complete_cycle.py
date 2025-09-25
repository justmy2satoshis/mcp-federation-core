#!/usr/bin/env python3
"""
Test Complete Installation Cycle for MCP Federation Core
Tests Install → Uninstall → Reinstall to ensure clean cycles
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from uninstall import MCPFederationUninstaller

def test_complete_cycle():
    """Test Install → Uninstall → Reinstall cycle"""
    print('\n' + '='*70)
    print('TESTING COMPLETE INSTALLATION CYCLE')
    print('='*70)

    # Step 1: Check initial state
    print('\nStep 1: Analyzing current installation...')
    print('-' * 50)

    uninstaller = MCPFederationUninstaller()
    initial_analysis = uninstaller.analyze_installation()

    print(f'Found {initial_analysis["total_federation_found"]}/15 Federation MCPs')
    print(f'Found {len(initial_analysis["user_mcps_found"])} user MCPs')

    if initial_analysis["total_federation_found"] == 15:
        print('[OK] All 15 Federation MCPs are installed')
    elif initial_analysis["total_federation_found"] > 0:
        print(f'[PARTIAL] Only {initial_analysis["total_federation_found"]} of 15 Federation MCPs installed')
    else:
        print('[EMPTY] No Federation MCPs currently installed')

    # Display detailed status
    uninstaller.display_complete_analysis(initial_analysis)

    # Step 2: Dry run first
    print('\n' + '='*70)
    print('Step 2: Running dry-run uninstall...')
    print('-' * 50)

    mcp_base = Path('C:/Users/User/mcp-servers/mcp_base')
    uninstaller.dry_run(mcp_base)

    # Step 3: Ask for confirmation
    print('\n' + '='*70)
    print('Step 3: Ready to perform ACTUAL uninstall')
    print('-' * 50)

    if initial_analysis["total_federation_found"] == 0:
        print('[SKIP] No Federation MCPs to uninstall')
        return

    print(f'\n[WARNING] This will remove {initial_analysis["total_federation_found"]} Federation MCPs')
    print('Type "YES" to proceed with actual uninstall, or anything else to abort:')

    confirm = input('> ').strip()

    if confirm != 'YES':
        print('[ABORT] Test cancelled by user')
        return

    # Step 4: Create backup
    print('\n' + '='*70)
    print('Step 4: Creating backup before uninstall...')
    print('-' * 50)

    backups = uninstaller.backup_configurations()
    print(f'[OK] Backups created: {len(backups)} config files saved')

    # Step 5: Actual uninstall
    print('\n' + '='*70)
    print('Step 5: Performing actual uninstall...')
    print('-' * 50)

    uninstaller.selective_uninstall(mcp_base)

    # Step 6: Verify complete removal
    print('\n' + '='*70)
    print('Step 6: Verifying complete removal...')
    print('-' * 50)

    post_analysis = uninstaller.analyze_installation()

    if post_analysis['total_federation_found'] == 0:
        print('[SUCCESS] All Federation MCPs successfully removed')
    else:
        print(f'[ERROR] WARNING: {post_analysis["total_federation_found"]} Federation MCPs still present!')
        for mcp in post_analysis['federation_mcps_found']:
            print(f'  - Still present: {mcp}')

    # Step 7: Check for orphaned files
    print('\n' + '='*70)
    print('Step 7: Checking for orphaned files...')
    print('-' * 50)

    orphaned = []
    for pattern in ['*federation*', '*mcp-unified*', '*expert-role*']:
        if mcp_base.exists():
            orphaned.extend(mcp_base.glob(pattern))

    if orphaned:
        print(f'[WARN] Found {len(orphaned)} orphaned files/directories:')
        for item in orphaned[:5]:  # Show first 5
            print(f'  - {item.name}')
        if len(orphaned) > 5:
            print(f'  ... and {len(orphaned) - 5} more')
    else:
        print('[OK] No orphaned Federation files found')

    # Step 8: Verify user MCPs intact (if any)
    if initial_analysis['user_mcps_found']:
        print('\n' + '='*70)
        print('Step 8: Verifying user MCPs preserved...')
        print('-' * 50)

        if len(post_analysis['user_mcps_found']) == len(initial_analysis['user_mcps_found']):
            print(f'[OK] All {len(post_analysis["user_mcps_found"])} user MCPs preserved')
        else:
            print('[ERROR] User MCP count mismatch!')
            print(f'  Before: {len(initial_analysis["user_mcps_found"])}')
            print(f'  After: {len(post_analysis["user_mcps_found"])}')

    # Final summary
    print('\n' + '='*70)
    print('TEST SUMMARY')
    print('='*70)

    success = post_analysis['total_federation_found'] == 0

    print(f'\nInitial state:')
    print(f'  - Federation MCPs: {initial_analysis["total_federation_found"]}/15')
    print(f'  - User MCPs: {len(initial_analysis["user_mcps_found"])}')

    print(f'\nFinal state:')
    print(f'  - Federation MCPs: {post_analysis["total_federation_found"]}/15')
    print(f'  - User MCPs: {len(post_analysis["user_mcps_found"])}')

    print(f'\nBackups:')
    print(f'  - Location: uninstaller_backups/{uninstaller.timestamp}')

    if success:
        print('\n[SUCCESS] Clean removal achieved!')
        print('Ready for clean reinstallation of MCP Federation Core')
    else:
        print('\n[FAILED] Issues found - review above for details')

    print('\n' + '='*70)
    print('Next steps:')
    print('1. Run installer to reinstall: python ../install.py')
    print('2. Verify all 15 MCPs are installed')
    print('3. Test functionality')
    print('4. If issues, restore backup: python uninstall.py --mode restore')
    print('='*70)

def verify_clean_state():
    """Quick verification that system is clean for reinstall"""
    uninstaller = MCPFederationUninstaller()
    analysis = uninstaller.analyze_installation()

    if analysis['total_federation_found'] == 0:
        print('[OK] System is clean - ready for installation')
        return True
    else:
        print(f'[WARN] {analysis["total_federation_found"]} Federation MCPs still present')
        return False

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Test MCP Federation installation cycle')
    parser.add_argument('--verify-only', action='store_true',
                        help='Only verify clean state without full test')

    args = parser.parse_args()

    if args.verify_only:
        verify_clean_state()
    else:
        test_complete_cycle()