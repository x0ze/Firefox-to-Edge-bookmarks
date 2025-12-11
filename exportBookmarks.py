import sqlite3
import json
import os

# This script scans all Windows user directories, finds Firefox bookmark databases,
# extracts the bookmarks, converts them into Microsoft Edge's JSON bookmark format,
# and saves them into the Edge profile directory.
# ⚠ Please note that this script does not take into account Firefox's multi-profile management.

basePath = "C:\\Users\\"

# List all user folders under C:\Users\
allUsers = [d for d in os.listdir(basePath) if os.path.isdir(os.path.join(basePath, d))]

# Relative path to Firefox profiles inside each user folder
profilePath = "\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\"

for user in allUsers:
    fullProfilePath = basePath + user + profilePath

    # Skip users without Firefox profiles
    if not os.path.exists(fullProfilePath):
        continue

    # List all Firefox profile folders
    contentDirectory = os.listdir(fullProfilePath)

    for filename in contentDirectory:
        # Target the default Firefox profile (its name usually contains "default"; if there is an error, change default to "default-esr").
        if 'default' in filename:
            databasePath = fullProfilePath + filename + "\\places.sqlite"

            # Connect to Firefox’s bookmarks database
            conn = sqlite3.connect(databasePath)
            cur = conn.cursor()

            # Query to match bookmarks with their URLs
            res = cur.execute("""
                SELECT moz_places.url, moz_bookmarks.title
                FROM moz_places
                INNER JOIN moz_bookmarks ON moz_bookmarks.fk = moz_places.id
            """)

            # Get all results (skipping the first 4 for unknown internal entries)
            bookmarksToFormat = res.fetchall()[4:]

            # Base structure of the Edge bookmark JSON file
            jsonStruct = {
               "roots": {
                  "bookmark_bar": {
                     "children": [],
                     "name": "Favorites Bar",
                     "source": "unknown",
                     "type": "folder"
                  },
                  "other": {
                     "children": [],
                     "name": "Other favorites",
                     "type": "folder"
                  },
                  "synced": {
                     "children": [],
                     "name": "Mobile favorites",
                     "type": "folder"
                  }
               },
               "version": 1
            }

            # Convert each Firefox bookmark into Edge-compatible format
            for bookmark in bookmarksToFormat:
                element = {
                    "name": bookmark[1],  # Bookmark title
                    "type": "url",
                    "url": bookmark[0]     # Bookmark URL
                }

                # Add to the Favorites Bar
                jsonStruct["roots"]["bookmark_bar"]["children"].append(element)

            # Convert to JSON string
            exportedBookmarks = json.dumps(jsonStruct)

            # Path to the Edge bookmark storage location
            edgeBookmarkPath = "C:/Users/" + user + "/AppData/Local/Microsoft/Edge/User Data/Default"

            # Create the folder if it doesn't exist
            if not os.path.exists(edgeBookmarkPath):
                os.makedirs(edgeBookmarkPath)

            # Write the generated JSON into Edge's Bookmarks file
            with open(edgeBookmarkPath + '/Bookmarks', 'w') as infile:
                infile.write(exportedBookmarks)

            print("[+] " + user + " bookmarks successfully exported to " + edgeBookmarkPath)

print("[+] Script executed successfully")
