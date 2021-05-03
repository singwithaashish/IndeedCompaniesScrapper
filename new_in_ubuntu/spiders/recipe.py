import scrapy


class RecipeSpider(scrapy.Spider):
    name = 'recipe'
    allowed_domains = ['www.glassdoor.co.in']
    start_urls = ['https://www.glassdoor.co.in/Reviews/bangalore-reviews-SRCH_IL.0,9_IM1091.htm']
    page_n = 1

    def parse(self, response):
        all_recipe = response.css('.single-company-result')

        for recipe in all_recipe:
            # item = {
            #     'name' : recipe.css('div.col-9').css('h2').css('a::text').get(),
            #     'rating' : recipe.css('.bigRating::text').get(),
            #     'headquaters' : recipe.css('span.value::text').get(),
            #     'image' : recipe.css('img::attr(src)').get()
            # }
            yield response.follow(f"https://www.glassdoor.co.in{recipe.css('div.col-9').css('h2').css('a::attr(href)').get()}", callback = self.push_in)
        
        
        if RecipeSpider.page_n < 1000:
            next_page_url = f'https://www.glassdoor.co.in/Reviews/bangalore-reviews-SRCH_IL.0,9_IM109{RecipeSpider.page_n}.htm'
            RecipeSpider.page_n += 1
            yield response.follow(next_page_url, callback = self.parse)
            
        
        pass


    def push_in(self, response):
        all_details = {
            'name' : response.css('#DivisionsDropdownComponent::text').get(),
            'Website' : response.css('.css-1hg9omi ::text').get(),
            'Headquarters' : response.css('div[data-test="employer-headquarters"]::text').get(),
            'Size' : response.css('div[data-test="employer-size"]::text').get(),
            'Founded': response.css('div[data-test="employer-founded"]::text').get(),
            'Type': response.css('div[data-test="employer-type"]::text').get(),
            'Industry': response.css('div[data-test="employer-industry"]::text').get(),
            'Revenue': response.css('div[data-test="employer-revenue"]::text').get()
        }
        yield all_details
