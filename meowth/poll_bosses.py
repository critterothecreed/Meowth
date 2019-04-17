import http.client
from lxml import html
import re
import json

SILPH_ROAD_DOMAIN = "thesilphroad.com"
SILPH_ROAD_BOSS_PATH = "/raid-bosses"
POKEDEX_JSON = "../data/pokemon.json"
GROUP_MAPPING = {
        0 : 'EX',
        1 : '5',
        2 : '4',
        3 : '3',
        4 : '2',
        5 : '1'
        }

def pokedex_no(pokemon_name):
    with open(POKEDEX_JSON, 'r') as json_file:
        data = json.load(json_file)
        for p_entry in data:
            if p_entry['name'] == pokemon_name:
                return p_entry['dex']
        return -1

conn = http.client.HTTPSConnection(SILPH_ROAD_DOMAIN)
conn.request("GET", SILPH_ROAD_BOSS_PATH)
r1 = conn.getresponse()
data1 = r1.read()

tree = html.fromstring(data1)
#titles = tree.xpath('//div[@class="raid-boss-tier-wrap" and position()=2]/following-sibling::div[@class="raid-boss-tier"]//div[@class="boss-name"]/text()')
boss_divs = tree.xpath('//div[@class="raid-boss-tier-wrap" or @class="raid-boss-tier"]')
group = -1
boss_list = dict()

for i in range(len(boss_divs)):
    if len(boss_divs[i].xpath('descendant-or-self::div[@class="raid-boss-tier-wrap"]')):
        #print("Group " + str(group))
        group += 1
        boss_list[GROUP_MAPPING[group]] = []
    else:
        long_name = boss_divs[i].xpath('descendant::div[@class="boss-name"]/text()')[0]
        short_name = long_name.replace("Alolan ","")
        short_name = re.sub('\s*\(.*\)','',short_name)
        boss_list[GROUP_MAPPING[group]].append(pokedex_no(short_name))

print(boss_list)
