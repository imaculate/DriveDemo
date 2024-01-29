import os.path

import merge
from merge.client import Merge
from merge.resources.filestorage import FoldersListRequestExpand


def main():
  test_api_key = "" # from https://app.merge.dev/keys
  test_account_token = "" # token from user
  client = Merge(
      account_token=test_account_token,
      api_key=test_api_key, 
  )
  items = None
  page_token = None

  try:
    while True:
      items = client.filestorage.folders.list(
        expand=FoldersListRequestExpand.DRIVE,
        page_size=10,
        cursor=page_token,
      )
    

      if not items:
        print("No folders found")
      
      print("Files:")
      for item in items.results:
        print(f"{item.name} ({item.id})")
      page_token = items.next
      if page_token is None:
        break
  except e:
    print("Exception when Merge Storage API " + e)


if __name__ == "__main__":
  main()