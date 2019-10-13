# -*- coding: utf-8 -*-
import scrapy

from fifaindex.items import PlayerItem


class FIFAIndexCrawler(scrapy.Spider):
    name = 'fifaindex'
    start_urls = ['https://www.fifaindex.com/players/']

    def parse(self, response):
        for i, player_href in enumerate(response.css('table.table-players > tbody > tr > td > figure > a::attr(href)')):
            player_url = response.urljoin(player_href.get())
            yield scrapy.Request(player_url, callback=self.parse_player)

        next_pages = response.css('a.page-link::attr(href)').getall()
        if next_pages:
            next_page_url = response.urljoin(next_pages[-1])
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_player(self, response):
        player = PlayerItem(url=response.url)

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
            if cards:
                parser(player, cards)

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
        if len(card.css('.card-body p')) != 2:
            cards.insert(0, card)
            return

        player['national_team_name'] = card.css('.card-header a::text').get()

        p = card.css('.card-body p')
        player['national_team_position'] = p[0].css('span.position::text').get()
        player['national_team_kit_number'] = p[1].css('span.float-right::text').get()

    def parse_club_card(self, player, cards):
        card = cards.pop(0)
        if len(card.css('.card-body p')) != 4:
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
