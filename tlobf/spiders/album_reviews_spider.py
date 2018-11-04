import scrapy

base_url = "https://www.thelineofbestfit.com/reviews/albums"
num_pages = 5


class AlbumReviewsSpider(scrapy.Spider):
    name = "album_reviews"
    # Set urls for num pages to scrape: P0, P8, P16 ...
    start_urls = [f"{base_url}/P{8*i}" for i in range(num_pages)]

    def parse_album(self, response):
        """Parses album review page for attributes."""
        yield {
            "artist": (
                response.css(".album-meta-artist span::text").extract_first().strip()
            ),
            "album": response.css(".album-meta-title::text").extract_first(),
            "rating": response.css(".album-meta-item--rating::text").extract_first(),
            "release_date": " ".join(
                response.css(".album-meta span > li:nth-child(3)::text")
                .extract_first()
                .split()[2:]
            ),
            "release_country": " ".join(
                response.css(".album-meta span > li:nth-child(4)::text")
                .extract_first()
                .split(":")[1:]
            ).strip(),
            "review_title": response.css(".pagetitle::text").extract_first(),
            "review_author": " ".join(
                response.css(".entry__author a span span::text").extract()
            ),
            "review_datetime": response.css("time::text").extract_first(),
            "review_summary": "".join(
                response.css(".intropara *::text").extract()
            ).strip(),
            "review": "\n\n".join(
                [
                    "".join(p.css("*::text").extract())
                    for p in response.css(".articlebody p")
                ]
            ),
        }

    def parse(self, response):
        """Parses reviews page for individual links."""
        links_selector = response.css("a.content-card::attr(href)")
        for link in links_selector.extract():
            # Pass each link to parse_album
            yield scrapy.Request("https:" + link, callback=self.parse_album)
