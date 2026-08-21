# importing modules
import pathlib
import feedparser
import helper
from datetime import datetime, timedelta

URL_1 ="https://www.insurancebusinessmag.com/uk/rss/"
URL_2 ="https://ifamagazine.com/category/insurance-and-protection/feed/"
URL_3 ="https://www.postonline.co.uk/feeds/rss/"
URL_4 ="https://www.reinsurancene.ws/feed/"
URL_5 ="https://www.insurancejournal.com/rss/"
URL_6 ="https://www.dig-in.com/feed.rss"
URL_7 ="https://insurance-edge.net/feed/"
URL_8 ="https://thefintechtimes.com/category/fintech/insurtech/feed/"
URL_9 ="https://insurtechinsights.com/feed/"
URL_10 ="https://www.fca.org.uk/news/rss.xml"
URL_11 ="https://feeds.feedblitz.com/insuranceday-all&x=1"



# processing
if __name__ == "__main__":
    try:
        root = pathlib.Path(__file__).parent.parent.resolve()

        urls = [URL_1, URL_2, URL_3, URL_4, URL_5, URL_6, URL_7, URL_8, URL_9, URL_10, URL_11]
        all_items = []

        for URL in urls:
            feed = feedparser.parse(URL)
            all_items.extend(feed["items"][:25])

        # Use published_parsed or updated_parsed for sorting/filtering
        for item in all_items:
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


        f = root / "insurance.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "news_marker", string)
        f.open("w").write(c)
        print(len(all_items),"News completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
