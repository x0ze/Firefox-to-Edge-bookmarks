import sqlite3
import json
import os

# Please note that this script does not take into account Firefox's multi-profile management.
# ==========================================================================================

basePath="C:\\Users\\"

allUsers = [d for d in os.listdir(basePath) if os.path.isdir(os.path.join(basePath, d))]
profilePath="\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\"                                      #PATH of the Firefox bookmarks file (Windows 7)

for user in allUsers :
    fullProfilePath = basePath+user+profilePath
    if not os.path.exists(fullProfilePath) : continue
    
    contentDirectory=os.listdir(fullProfilePath)
    
    for filename in contentDirectory :
        if 'default' in filename :
            databasePath = fullProfilePath+filename+"\\places.sqlite"

            conn = sqlite3.connect(databasePath)
            cur = conn.cursor()
            res = cur.execute("""SELECT moz_places.url, moz_bookmarks.title FROM moz_places INNER JOIN
                               moz_bookmarks ON moz_bookmarks.fk = moz_places.id""")

            bookmarksToFormat = res.fetchall()[4:]

            jsonStruct = {
               "roots": {
                  "bookmark_bar": {
                     "children": [],
                     "name": "Favorites Bar",
                     "source": "unknown",
                     "type": "folder"
                  },
                  "other": {
                     "children": [  ],
                     "name": "Other favorites",
                     "type": "folder"
                  },
                  "synced": {
                     "children": [  ],
                     "name": "Mobile favorites",
                     "type": "folder"
                  }
               },
               "version": 1
            }


            for bookmark in bookmarksToFormat:
                element = {
                    "name": bookmark[1],
                    "type": "url",
                    "url": bookmark[0]
                }

                jsonStruct["roots"]["bookmark_bar"]["children"].append(element)

            exportedBookmarks = json.dumps(jsonStruct)
            edgeBookmarkPath="C:/Users/"+user+"/AppData/Local/Microsoft/Edge/User Data/Default"         #PATH of the converted bookmarks file for Edge (Windows 11)
            if not os.path.exists(edgeBookmarkPath):
                os.makedirs(edgeBookmarkPath)
            with open(edgeBookmarkPath+'/Bookmarks', 'w') as infile:
                file = infile.write(exportedBookmarks)
            print("[+]"+user+" bookmarks successfully exported in "+edgeBookmarkPath)


print("[+] script executed successfully")


