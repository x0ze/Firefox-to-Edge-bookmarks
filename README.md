# Firefox to Edge Bookmark Migrator

This script extracts bookmarks from Firefox on Windows 7 and converts them into the Microsoft Edge bookmark format for Windows 11.
It scans all user profiles, reads Firefox’s places.sqlite, and writes a compatible Bookmarks file for Edge.

# Features

- Automatically detects Firefox profiles (default-esr)
- Extracts URLs and titles from places.sqlite
- Rebuilds a valid Edge bookmark JSON structure
- Creates or replaces Edge’s Bookmarks file for each user

# Usage

Copy the script to a Windows machine where Firefox (Windows 7) data is present.

Run the script with Python 3 (tested with python 3.5).

```cmd
.\exportBookmarks.py
```
The converted bookmarks will be written to:
`C:/Users/<User>/AppData/Local/Microsoft/Edge/User Data/Default/Bookmarks`

# Common issues
Some problems may occur with this script. There are few checks, so it is possible that no errors will be displayed but no bookmarks will be exported.

- Multiple default profiles : change the `userProfile` variable in line 10 of the script to `default-esr` (because there are several default profiles, so a profile may be empty).
- Multi-profile Firefox setups are not handled.
- Insufficient user rights : run the script with appropriate permissions to access all user folders.


