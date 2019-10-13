import scrapy
from scrapy.crawler import CrawlerProcess


class FIFAIndexCrawler(scrapy.Spider):
    name = 'fifa_index_crawler'
    start_urls = ['https://www.fifaindex.com/players/']
    custom_settings = {
        'DOWNLOAD_DELAY': 5,
    }

    def parse(self, response):
        # self.download_page(response)
        # for player_href in response.css('table.table-players > tbody > tr > td > figure > a::attr(href)'):
        for i, player_href in enumerate(response.css('table.table-players > tbody > tr > td > figure > a::attr(href)')):
            player_url = response.urljoin(player_href.get())
            yield scrapy.Request(player_url, callback=self.parse_player)

            if i == 0:
                break
        # yield self.go_to_next_page(response)

    def download_page(self, response):
        filename = response.url.split('/')[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

    def parse_player(self, response):
        player = Player()

        cards = response.css('.container .card')[1:] # Ignore abstract card
        parsers = [
            self.parse_player_card,
            self.parse_national_team_card,
            self.parse_club_card,
            self.parse_ball_skills_card,
            self.parse_defence_card,
            self.parse_mental_card,
            self.parse_passing_card,
            self.parse_physical_card,
            self.parse_shooting_card,
            self.parse_goalkeeper_card,
            self.parse_specialities_card,
            self.parse_traits_card,
        ]
        for parser in parsers:
            parser(player, cards)

        self.logger.info(player)
        yield player

    def parse_player_card(self, player, cards):
        card = cards.pop(0)
        player['name'] = card.css('.card-header::text').get()
        player['overall_score'], player['potential_score'] = card.css('.card-header span.rating::text').getall()

        p = card.css('.card-body p')
        player['height'] = {'metric': p[0].css('.data-units-metric::text').get(), 'imperial': p[0].css('.data-units-imperial::text').get()}
        player['weight'] = {'metric': p[1].css('.data-units-metric::text').get(), 'imperial': p[1].css('.data-units-imperial::text').get()}
        player['preferred_foot'] = p[2].css('span.float-right::text').get()
        player['birth_date'] = p[3].css('span.float-right::text').get()
        player['age'] = p[4].css('span.float-right::text').get()
        player['preferred_positions'] = p[5].css('span.position::text').getall()
        player['player_work_rate'] = p[6].css('span.float-right::text').get()
        player['weak_foot'] = self.convert_stars_to_number(p[7].css('span.star'))
        player['skill_moves'] = self.convert_stars_to_number(p[8].css('span.star'))
        player['value'] = {'EUR': p[9].css('span.float-right::text').get(), 'USD': p[10].css('span.float-right::text').get(), 'GBP': p[11].css('span.float-right::text').get()}
        player['wage'] = {'EUR': p[12].css('span.float-right::text').get(), 'USD': p[13].css('span.float-right::text').get(), 'GBP': p[14].css('span.float-right::text').get()}

    def parse_national_team_card(self, player, cards):
        card = cards.pop(0)
        player['national_team_name'] = card.css('.card-header a::text').get()

        p = card.css('.card-body p')
        player['national_team_position'] = p[0].css('span.position::text').get()
        player['national_team_kit_number'] = p[1].css('span.float-right::text').get()

    def parse_club_card(self, player, cards):
        card = cards.pop(0)
        if len(card.css('.card-body p')) < 4:
            cards.insert(0, card)
            return

        player['club_name'] = card.css('.card-header a::text').get()

        p = card.css('.card-body p')
        player['club_position'] = p[0].css('span.position::text').get()
        player['club_kit_number'] = p[1].css('span.float-right::text').get()
        player['club_joined_at'] = p[2].css('span.float-right::text').get()
        player['club_contract_length'] = p[3].css('span.float-right::text').get()

    def parse_ball_skills_card(self, player, cards):
        card = cards.pop(0)
        title = card.css('h5.card-header::text').get()
        if title != 'Ball Skills':
            cards.insert(0, card)
            return

        p = card.css('.card-body p')
        player['ball_control'] = p[0].css('span.badge::text').get()
        player['dribbling'] = p[1].css('span.badge::text').get()

    def parse_defence_card(self, player, cards):
        card = cards.pop(0)
        title = card.css('h5.card-header::text').get()
        if title != 'Defence':
            cards.insert(0, card)
            return

        p = card.css('.card-body p')
        player['marking'] = p[0].css('span.badge::text').get()
        player['slide_tackle'] = p[1].css('span.badge::text').get()
        player['stand_tackle'] = p[2].css('span.badge::text').get()

    def parse_mental_card(self, player, cards):
        card = cards.pop(0)
        title = card.css('h5.card-header::text').get()
        if title != 'Mental':
            cards.insert(0, card)
            return

        p = card.css('.card-body p')
        player['aggression'] = p[0].css('span.badge::text').get()
        player['reactions'] = p[1].css('span.badge::text').get()
        player['att_position'] = p[2].css('span.badge::text').get()
        player['interceptions'] = p[3].css('span.badge::text').get()
        player['vision'] = p[4].css('span.badge::text').get()
        player['composure'] = p[5].css('span.badge::text').get()

    def parse_passing_card(self, player, cards):
        card = cards.pop(0)
        title = card.css('h5.card-header::text').get()
        if title != 'Passing':
            cards.insert(0, card)
            return

        p = card.css('.card-body p')
        player['crossing'] = p[0].css('span.badge::text').get()
        player['short_pass'] = p[1].css('span.badge::text').get()
        player['long_pass'] = p[2].css('span.badge::text').get()

    def parse_physical_card(self, player, cards):
        card = cards.pop(0)
        title = card.css('h5.card-header::text').get()
        if title != 'Physical':
            cards.insert(0, card)
            return

        p = card.css('.card-body p')
        player['acceleration'] = p[0].css('span.badge::text').get()
        player['stamina'] = p[1].css('span.badge::text').get()
        player['strength'] = p[2].css('span.badge::text').get()
        player['balance'] = p[3].css('span.badge::text').get()
        player['sprint_speed'] = p[4].css('span.badge::text').get()
        player['agility'] = p[5].css('span.badge::text').get()
        player['jumping'] = p[6].css('span.badge::text').get()

    def parse_shooting_card(self, player, cards):
        card = cards.pop(0)
        title = card.css('h5.card-header::text').get()
        if title != 'Shooting':
            cards.insert(0, card)
            return

        p = card.css('.card-body p')
        player['heading'] = p[0].css('span.badge::text').get()
        player['shot_power'] = p[1].css('span.badge::text').get()
        player['finishing'] = p[2].css('span.badge::text').get()
        player['long_shots'] = p[3].css('span.badge::text').get()
        player['curve'] = p[4].css('span.badge::text').get()
        player['fk_acc'] = p[5].css('span.badge::text').get()
        player['penalties'] = p[6].css('span.badge::text').get()
        player['volleys'] = p[7].css('span.badge::text').get()

    def parse_goalkeeper_card(self, player, cards):
        card = cards.pop(0)
        title = card.css('h5.card-header::text').get()
        if title != 'Goalkeeper':
            cards.insert(0, card)
            return

        p = card.css('.card-body p')
        player['gk_positioning'] = p[0].css('span.badge::text').get()
        player['gk_diving'] = p[1].css('span.badge::text').get()
        player['gk_handling'] = p[2].css('span.badge::text').get()
        player['gk_kicking'] = p[3].css('span.badge::text').get()
        player['gk_reflexes'] = p[4].css('span.badge::text').get()

    def parse_specialities_card(self, player, cards):
        card = cards.pop(0)
        title = card.css('h5.card-header::text').get()
        if title != 'Specialities':
            cards.insert(0, card)
            return

        player['specialities'] = card.css('.card-body p::text').getall()

    def parse_traits_card(self, player, cards):
        card = cards.pop(0)
        title = card.css('h5.card-header::text').get()
        if title != 'Traits':
            cards.insert(0, card)
            return

        player['traits'] = card.css('.card-body p::text').getall()

    def convert_stars_to_number(self, selector):
        return len(selector.css('i.fas').getall())

    def go_to_next_page(self, response):
        for next_page in response.css('a.page-link'):
            yield response.follow(next_page, self.parse)


class Player(scrapy.Item):
    name = scrapy.Field()
    overall_score = scrapy.Field()
    potential_score = scrapy.Field()
    preferred_foot = scrapy.Field()
    birth_date = scrapy.Field()
    age = scrapy.Field()
    preferred_positions = scrapy.Field()
    player_work_rate = scrapy.Field()
    weak_foot = scrapy.Field()
    skill_moves = scrapy.Field()
    value = scrapy.Field()
    wage = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()

    national_team_name = scrapy.Field()
    national_team_position = scrapy.Field()
    national_team_kit_number = scrapy.Field()

    club_name = scrapy.Field()
    club_position = scrapy.Field()
    club_kit_number = scrapy.Field()
    club_joined_at = scrapy.Field()
    club_contract_length = scrapy.Field()

    ball_control = scrapy.Field()
    dribbling = scrapy.Field()

    marking = scrapy.Field()
    slide_tackle = scrapy.Field()
    stand_tackle = scrapy.Field()

    aggression = scrapy.Field()
    reactions = scrapy.Field()
    att_position = scrapy.Field()
    interceptions = scrapy.Field()
    vision = scrapy.Field()
    composure = scrapy.Field()

    crossing = scrapy.Field()
    short_pass = scrapy.Field()
    long_pass = scrapy.Field()

    acceleration = scrapy.Field()
    stamina = scrapy.Field()
    strength = scrapy.Field()
    balance = scrapy.Field()
    sprint_speed = scrapy.Field()
    agility = scrapy.Field()
    jumping = scrapy.Field()

    heading = scrapy.Field()
    shot_power = scrapy.Field()
    finishing = scrapy.Field()
    long_shots = scrapy.Field()
    curve = scrapy.Field()
    fk_acc = scrapy.Field()
    penalties = scrapy.Field()
    volleys = scrapy.Field()

    gk_positioning = scrapy.Field()
    gk_diving = scrapy.Field()
    gk_handling = scrapy.Field()
    gk_kicking = scrapy.Field()
    gk_reflexes = scrapy.Field()

    specialities = scrapy.Field()

    traits = scrapy.Field()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'LOG_LEVEL': 'INFO',
})

process.crawl(FIFAIndexCrawler)
process.start()