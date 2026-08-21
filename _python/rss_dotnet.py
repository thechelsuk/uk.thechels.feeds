# importing modules
import pathlib
import feedparser
import helper
from datetime import datetime, timedelta

URL_1 ="https://devblogs.microsoft.com/dotnet/feed/"
URL_2 ="https://blog.jetbrains.com/dotnet/feed/"
URL_3 ="https://andrewlock.net/rss.xml"
URL_4 ="https://dotnetkicks.com/feeds/rss"
URL_5 ="https://dotnettips.wordpress.com/feed/"
URL_6 ="https://blog.cwa.me.uk/feed"
URL_7 ="http://feeds.hanselman.com/ScottHanselman"
URL_8 ="https://azurestatusfeed.azurewebsites.net/"
URL_9 ="https://www.alvinashcraft.com/feed.xml"



# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()

        urls = [URL_1, URL_2, URL_3, URL_4, URL_5, URL_6, URL_7, URL_8, URL_9]
        all_items = []

        for URL in urls:
            feed = feedparser.parse(URL)
            all_items.extend(feed["items"][:25])

        # Use published_parsed or updated_parsed for sorting/filtering
        for item in all_items:
            item["title"] = item["title"].replace("|", " - ").replace(">", " - ")
            if "published_parsed" in item and item["published_parsed"] is not None:
                item["_sort_date"] = item["published_parsed"]
            elif "updated_parsed" in item and item["updated_parsed"] is not None:
                item["_sort_date"] = item["updated_parsed"]
            else:
                item["_sort_date"] = None

        # Filter out items without a valid date
        all_items = [item for item in all_items if item["_sort_date"] is not None]
        all_items.sort(key=lambda x: x["_sort_date"], reverse=True)

        cutoff_date = datetime.now() - timedelta(days=30)
        all_items = [item for item in all_items if datetime(*item["_sort_date"][:6]) > cutoff_date]

        string = ""
        for item in all_items:
            # Use helper.time_ago for display only
            item_time = helper.time_ago(item["_sort_date"])
            string += f"- {item['title']} ([{item_time}]({item['link']}))\n"


        f = root / "dotnet.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "news_marker", string)
        f.open("w").write(c)
        print(len(all_items),"News completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
