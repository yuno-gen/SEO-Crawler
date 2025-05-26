import hashlib, gzip, io, os, time
import scrapy
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE")
sp = create_client(SUPABASE_URL, SUPABASE_KEY)

class GenericSiteSpider(scrapy.Spider):
    name = "generic_site"
    custom_settings = {"HTTPERROR_ALLOW_ALL": True}

    def __init__(self, start_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if start_url is None:
            raise ValueError("start_url arg required, e.g. scrapy crawl generic_site -a start_url=https://example.com")
        self.start_urls = [start_url]

    def parse(self, response):
        url = response.url
        status = response.status
        title = response.xpath("//title/text()").get(default="").strip()
        h1 = " ".join(response.xpath("//h1//text()").getall())[:255]
        ttfb_ms = int(response.meta.get("download_latency", 0) * 1000)

        raw = response.body
        sha1 = hashlib.sha1(raw).hexdigest()
        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode="wb") as f:
            f.write(raw)
        sp.storage.from_("raw-html").upload(f"raw/{sha1}.gz", buf.getvalue())

        sp.table("pages").upsert({
            "url": url,
            "title": title,
            "h1": h1,
            "status": status,
            "fetch_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "ttfb_ms": ttfb_ms,
            "content_hash": sha1,
        }).execute()

        # follow internal links
        for link in response.css("a::attr(href)").getall():
            if link.startswith("/"):
                link = response.urljoin(link)
            if link.startswith(start_url):
                yield scrapy.Request(link, callback=self.parse)