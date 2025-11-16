#!/usr/bin/env python3
"""
Project Cleanup Utility
Interactive tool to clean up test files and development artifacts

Usage: python3 cleanup_project.py

This script will:
1. Show current folder structure with file counts and sizes
2. Prompt to delete test/ folder (recommended)
3. Prompt to delete utils/ and dev/ folders (optional)
4. Confirm cleanup completion
5. Show final clean structure

After approval, run this to clean up development artifacts while
preserving production code in dashboard_app/ and database_implementation/
"""

import os
import shutil
from pathlib import Path


def show_project_structure():
    """Display current project structure with statistics"""

    project_root = Path(__file__).parent

    print("📁 CURRENT PROJECT STRUCTURE")
    print("=" * 60)

    folder_stats = {}

    # Analyze each folder
    for item in project_root.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            files = list(item.rglob("*"))
            file_count = sum(1 for f in files if f.is_file())
            total_size = sum(f.stat().st_size for f in files if f.is_file())
            size_mb = total_size / (1024 * 1024)
            folder_stats[item.name] = {
                "files": file_count,
                "size": size_mb,
                "path": item,
            }

    # Show deletable folders
    print("🗑️  DEVELOPMENT ARTIFACTS (Can be deleted):")
    deletable = ["test", "utils", "dev"]
    for folder in deletable:
        if folder in folder_stats:
            info = folder_stats[folder]
            print(f"   {folder}/     {info['files']:4d} files  {info['size']:7.1f} MB")

    print("\n✅ PRODUCTION CODE (Keep these):")
    keep = ["dashboard_app", "database_implementation", "data"]
    for folder in keep:
        if folder in folder_stats:
            info = folder_stats[folder]
            print(f"   {folder}/    {info['files']:4d} files  {info['size']:7.1f} MB")

    # Show root files
    root_files = [
        f for f in project_root.iterdir() if f.is_file() and not f.name.startswith(".")
    ]
    if root_files:
        print("\n📄 ROOT FILES:")
        for file in sorted(root_files):
            size = file.stat().st_size
            if size < 1024:
                size_str = f"{size:4d} B"
            elif size < 1024 * 1024:
                size_str = f"{size / 1024:5.1f} KB"
            else:
                size_str = f"{size / (1024 * 1024):5.1f} MB"
            print(f"   {file.name:<25} {size_str}")


def get_user_confirmation(prompt: str) -> bool:
    """Get yes/no confirmation from user"""
    while True:
        response = input(f"\n❓ {prompt} (y/N): ").lower().strip()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no", ""]:
            return False
        else:
            print("   Please enter 'y' for yes or 'n' for no.")


def cleanup_folder(folder_path: Path) -> bool:
    """Remove a folder and return success status"""
    if not folder_path.exists():
        print(f"ℹ️  {folder_path.name}/ folder not found")
        return False

    # Calculate statistics
    files = list(folder_path.rglob("*"))
    file_count = sum(1 for f in files if f.is_file())
    total_size = sum(f.stat().st_size for f in files if f.is_file())
    size_mb = total_size / (1024 * 1024)

    print(f"🗑️  About to delete {folder_path.name}/:")
    print(f"   Files: {file_count}")
    print(f"   Size:  {size_mb:.1f} MB")

    if get_user_confirmation(f"Delete {folder_path.name}/ folder"):
        shutil.rmtree(folder_path)
        print(f"✅ {folder_path.name}/ folder deleted successfully")
        return True
    else:
        print(f"ℹ️  {folder_path.name}/ folder kept")
        return False


def cleanup_optional_folders():
    """Handle cleanup of optional folders (utils, dev)"""

    project_root = Path(__file__).parent
    optional_folders = ["utils", "dev"]
    any_deleted = False

    # Show info for all optional folders
    for folder_name in optional_folders:
        folder_path = project_root / folder_name
        if folder_path.exists():
            files = list(folder_path.rglob("*"))
            file_count = sum(1 for f in files if f.is_file())
            total_size = sum(f.stat().st_size for f in files if f.is_file())
            size_mb = total_size / (1024 * 1024)
            print(f"🔧 {folder_name}/ folder: {file_count} files, {size_mb:.1f} MB")

    if get_user_confirmation("Delete utils/ and dev/ folders"):
        for folder_name in optional_folders:
            folder_path = project_root / folder_name
            if cleanup_folder(folder_path):
                any_deleted = True
    else:
        print("ℹ️  utils/ and dev/ folders kept")

    return any_deleted


def show_final_structure():
    """Display the final cleaned project structure"""

    project_root = Path(__file__).parent

    print("\n" + "=" * 60)
    print("🎉 CLEANUP COMPLETED!")
    print("=" * 60)

    print("\n📊 FINAL PROJECT STRUCTURE:")

    # Show remaining folders
    folders = [
        item
        for item in project_root.iterdir()
        if item.is_dir() and not item.name.startswith(".")
    ]

    for folder in sorted(folders):
        files = list(folder.rglob("*"))
        file_count = sum(1 for f in files if f.is_file())
        total_size = sum(f.stat().st_size for f in files if f.is_file())
        size_mb = total_size / (1024 * 1024)
        print(f"   📁 {folder.name}/     {file_count:4d} files  {size_mb:7.1f} MB")

    # Show root files
    root_files = [
        f for f in project_root.iterdir() if f.is_file() and not f.name.startswith(".")
    ]
    if root_files:
        print("\n📄 Root Files:")
        for file in sorted(root_files):
            size = file.stat().st_size
            if size < 1024:
                size_str = f"{size:4d} B"
            elif size < 1024 * 1024:
                size_str = f"{size / 1024:5.1f} KB"
            else:
                size_str = f"{size / (1024 * 1024):5.1f} MB"
            print(f"   📄 {file.name:<25} {size_str}")


def main():
    """Main cleanup function"""

    print("🧹 PROJECT CLEANUP UTILITY")
    print("=" * 60)
    print()
    print("This script helps clean up development artifacts after")
    print("approving the AI analysis approach.")
    print()
    print("It will preserve production code while removing:")
    print("  - Test files and results")
    print("  - Development utilities")
    print("  - Temporary development artifacts")

    # Show current structure
    show_project_structure()

    print("\n" + "=" * 60)
    print("🗑️  CLEANUP OPTIONS:")
    print("=" * 60)

    # Clean test folder (recommended)
    test_deleted = cleanup_folder(Path(__file__).parent / "test")

    # Clean optional folders
    optional_deleted = cleanup_optional_folders()

    # Show final structure
    show_final_structure()

    # Show summary
    print("\n" + "=" * 60)
    print("📋 CLEANUP SUMMARY:")
    print("=" * 60)

    if test_deleted:
        print("✅ test/ folder deleted (removed all test artifacts)")
    else:
        print("ℹ️  test/ folder kept (contains test files and results)")

    if optional_deleted:
        print("✅ utils/ and/or dev/ folders deleted")
    else:
        print("ℹ️  utils/ and dev/ folders kept")

    print("\n✅ Production code preserved:")
    print("   📁 dashboard_app/      (main application)")
    print("   📁 database_implementation/ (database system)")
    print("   📄 config.py, database.py, tools.py, etc. (configuration files)")

    print(f"\n🎯 Ready for production deployment!")
    print(f"\n💡 Next steps after cleanup:")
    print(f"   1. Review the dashboard application")
    print(f"   2. Test database functionality")
    print(f"   3. Deploy with: cd dashboard_app && ./run_dashboard.sh")


if __name__ == "__main__":
    main()
