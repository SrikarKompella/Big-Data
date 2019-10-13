# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PlayerItem(scrapy.Item):
    url = scrapy.Field()

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
