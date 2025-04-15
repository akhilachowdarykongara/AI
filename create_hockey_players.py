from supabase import create_client
import os
from datetime import date

# Initialize Supabase client
SUPABASE_URL = ""
SUPABASE_KEY = ""

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Player data
players_data = [
    {
        "name": "Wayne Gretzky",
        "birth_date": "1961-01-26",
        "nationality": "Canadian",
        "position": "Center",
        "games_played": 1487,
        "goals": 894,
        "assists": 1963,
        "points": 2857,
        "teams": ["Edmonton Oilers", "Los Angeles Kings", "St. Louis Blues", "New York Rangers"],
        "captain_years": 9,
        "stanley_cups": 4,
        "biography": "Known as 'The Great One', Wayne Gretzky is widely considered the greatest hockey player of all time. He revolutionized the sport with his exceptional playmaking abilities and hockey intelligence. He holds numerous NHL records including most goals, assists, and points. "
    },
    {
        "name": "Mario Lemieux",
        "birth_date": "1965-10-05",
        "nationality": "Canadian",
        "position": "Center",
        "games_played": 915,
        "goals": 690,
        "assists": 1033,
        "points": 1723,
        "teams": ["Pittsburgh Penguins"],
        "captain_years": 13,
        "stanley_cups": 2,
        "biography": "Mario Lemieux, nicknamed 'The Magnificent One', overcame serious health issues including cancer to become one of hockey's greatest players. He saved the Penguins franchise as both a player and owner."
    },
    {
        "name": "Gordie Howe",
        "birth_date": "1928-03-31",
        "nationality": "Canadian",
        "position": "Right Wing",
        "games_played": 1767,
        "goals": 801,
        "assists": 1049,
        "points": 1850,
        "teams": ["Detroit Red Wings", "Hartford Whalers"],
        "captain_years": 4,
        "stanley_cups": 4,
        "biography": "Known as 'Mr. Hockey', Gordie Howe played professional hockey for 26 seasons in the NHL and 6 seasons in the WHA. His career spanned five decades, and he was known for his scoring ability, physical play, and longevity. He played professionally with his sons Mark and Marty on the Houston Aeros and New England Whalers."
    },
    {
        "name": "Bobby Orr",
        "birth_date": "1948-03-20",
        "nationality": "Canadian",
        "position": "Defenseman",
        "games_played": 657,
        "goals": 270,
        "assists": 645,
        "points": 915,
        "teams": ["Boston Bruins", "Chicago Black Hawks"],
        "captain_years": 2,
        "stanley_cups": 2,
        "biography": "Bobby Orr revolutionized the defenseman position with his offensive prowess and end-to-end rushes. He won eight consecutive Norris Trophies and is the only defenseman to win the Art Ross Trophy as scoring champion. His career was cut short by knee injuries."
    },
    {
        "name": "Sidney Crosby",
        "birth_date": "1987-08-07",
        "nationality": "Canadian",
        "position": "Center",
        "games_played": 1191,
        "goals": 550,
        "assists": 952,
        "points": 1502,
        "teams": ["Pittsburgh Penguins"],
        "captain_years": 16,
        "stanley_cups": 3,
        "biography": "'Sid the Kid' entered the NHL as a generational talent and lived up to expectations. Known for his exceptional work ethic and 200-foot game, Crosby has led the Penguins to three Stanley Cups while winning multiple individual awards including two Hart Trophies."
    },
    {
        "name": "Alexander Ovechkin",
        "birth_date": "1985-09-17",
        "nationality": "Russian",
        "position": "Left Wing",
        "games_played": 1364,
        "goals": 822,
        "assists": 664,
        "points": 1486,
        "teams": ["Washington Capitals"],
        "captain_years": 13,
        "stanley_cups": 1,
        "biography": "'The Great 8' is considered one of the greatest goal scorers in NHL history. Known for his powerful shot and physical play, Ovechkin finally won his first Stanley Cup in 2018. He's chasing Wayne Gretzky's all-time goals record."
    },
    {
        "name": "Mark Messier",
        "birth_date": "1961-01-18",
        "nationality": "Canadian",
        "position": "Center",
        "games_played": 1756,
        "goals": 694,
        "assists": 1193,
        "points": 1887,
        "teams": ["Edmonton Oilers", "New York Rangers", "Vancouver Canucks"],
        "captain_years": 15,
        "stanley_cups": 6,
        "biography": "Known as 'The Moose', Messier was one of the greatest leaders in NHL history. He is the only player to captain two different teams to Stanley Cup championships, winning with both the Oilers and Rangers."
    },
    {
        "name": "Maurice Richard",
        "birth_date": "1921-08-04",
        "nationality": "Canadian",
        "position": "Right Wing",
        "games_played": 978,
        "goals": 544,
        "assists": 421,
        "points": 965,
        "teams": ["Montreal Canadiens"],
        "captain_years": 4,
        "stanley_cups": 8,
        "biography": "'The Rocket' was the first player to score 50 goals in 50 games and the first to reach 500 goals in the NHL. A cultural icon in Quebec, Richard played with intensity and passion that made him a legendary figure in hockey history."
    },
    {
        "name": "Jean Beliveau",
        "birth_date": "1931-08-31",
        "nationality": "Canadian",
        "position": "Center",
        "games_played": 1125,
        "goals": 507,
        "assists": 712,
        "points": 1219,
        "teams": ["Montreal Canadiens"],
        "captain_years": 10,
        "stanley_cups": 10,
        "biography": "'Le Gros Bill' was known for his elegance both on and off the ice. He won 10 Stanley Cups as a player and 7 more as an executive with the Canadiens. Beliveau was one of hockey's greatest ambassadors."
    },
    {
        "name": "Patrick Roy",
        "birth_date": "1965-10-05",
        "nationality": "Canadian",
        "position": "Goalie",
        "games_played": 1029,
        "goals": 0,
        "assists": 45,
        "points": 45,
        "teams": ["Montreal Canadiens", "Colorado Avalanche"],
        "captain_years": 0,
        "stanley_cups": 4,
        "biography": "Revolutionary goaltender who popularized the butterfly style. Roy won four Stanley Cups and three Conn Smythe Trophies as playoff MVP. He held the record for most NHL wins by a goaltender when he retired."
    },
    {
        "name": "Steve Yzerman",
        "birth_date": "1965-05-09",
        "nationality": "Canadian",
        "position": "Center",
        "games_played": 1514,
        "goals": 692,
        "assists": 1063,
        "points": 1755,
        "teams": ["Detroit Red Wings"],
        "captain_years": 19,
        "stanley_cups": 3,
        "biography": "'The Captain' led Detroit for 19 seasons, the longest captaincy in NHL history. Yzerman transformed from a pure scorer into a complete two-way player, leading the Red Wings to three Stanley Cups."
    },
    {
        "name": "Brett Hull",
        "birth_date": "1964-08-09",
        "nationality": "Canadian-American",
        "position": "Right Wing",
        "games_played": 1269,
        "goals": 741,
        "assists": 650,
        "points": 1391,
        "teams": ["Calgary Flames", "St. Louis Blues", "Dallas Stars", "Detroit Red Wings", "Phoenix Coyotes"],
        "captain_years": 3,
        "stanley_cups": 2,
        "biography": "'The Golden Brett' possessed one of the most accurate shots in NHL history. Son of Bobby Hull, he scored 86 goals in 1990-91 season and won Stanley Cups with Dallas and Detroit."
    },
    {
        "name": "Joe Sakic",
        "birth_date": "1969-07-07",
        "nationality": "Canadian",
        "position": "Center",
        "games_played": 1378,
        "goals": 625,
        "assists": 1016,
        "points": 1641,
        "teams": ["Quebec Nordiques", "Colorado Avalanche"],
        "captain_years": 17,
        "stanley_cups": 2,
        "biography": "Known for his lethal wrist shot and clutch performances, Sakic spent his entire career with the same franchise. He led the Avalanche to two Stanley Cups and won the Hart Trophy in 2001."
    },
    {
        "name": "Phil Esposito",
        "birth_date": "1942-02-20",
        "nationality": "Canadian",
        "position": "Center",
        "games_played": 1282,
        "goals": 717,
        "assists": 873,
        "points": 1590,
        "teams": ["Chicago Black Hawks", "Boston Bruins", "New York Rangers"],
        "captain_years": 6,
        "stanley_cups": 2,
        "biography": "Revolutionary center who popularized positioning in front of the net. First player to score 100 points in a season and held many scoring records before Gretzky."
    },
    {
        "name": "Bobby Hull",
        "birth_date": "1939-01-03",
        "nationality": "Canadian",
        "position": "Left Wing",
        "games_played": 1063,
        "goals": 610,
        "assists": 560,
        "points": 1170,
        "teams": ["Chicago Black Hawks", "Winnipeg Jets", "Hartford Whalers"],
        "captain_years": 3,
        "stanley_cups": 1,
        "biography": "'The Golden Jet' was known for his blazing speed and powerful slapshot. First player to score more than 50 goals in a season and helped legitimize the WHA by joining the Winnipeg Jets."
    },
    {
        "name": "Martin Brodeur",
        "birth_date": "1972-05-06",
        "nationality": "Canadian",
        "position": "Goalie",
        "games_played": 1266,
        "goals": 0,
        "assists": 47,
        "points": 47,
        "teams": ["New Jersey Devils", "St. Louis Blues"],
        "captain_years": 0,
        "stanley_cups": 3,
        "biography": "NHL's all-time leader in wins and shutouts. Brodeur revolutionized the goalie position with his puck-handling skills and led the Devils to three Stanley Cups."
    },
    {
        "name": "Guy Lafleur",
        "birth_date": "1951-09-20",
        "nationality": "Canadian",
        "position": "Right Wing",
        "games_played": 1126,
        "goals": 560,
        "assists": 793,
        "points": 1353,
        "teams": ["Montreal Canadiens", "New York Rangers", "Quebec Nordiques"],
        "captain_years": 0,
        "stanley_cups": 5,
        "biography": "'The Flower' was known for his speed and flowing hair as he rushed up ice. First player to score 50 goals and 100 points in six straight seasons."
    },
    {
        "name": "Ray Bourque",
        "birth_date": "1960-12-28",
        "nationality": "Canadian",
        "position": "Defenseman",
        "games_played": 1612,
        "goals": 410,
        "assists": 1169,
        "points": 1579,
        "teams": ["Boston Bruins", "Colorado Avalanche"],
        "captain_years": 15,
        "stanley_cups": 1,
        "biography": "NHL's all-time leader in points by a defenseman. Played 21 seasons with Boston before winning his only Stanley Cup with Colorado in his final game."
    },
    {
        "name": "Jaromir Jagr",
        "birth_date": "1972-02-15",
        "nationality": "Czech",
        "position": "Right Wing",
        "games_played": 1733,
        "goals": 766,
        "assists": 1155,
        "points": 1921,
        "teams": ["Pittsburgh Penguins", "Washington Capitals", "New York Rangers", "Philadelphia Flyers", "Dallas Stars", "Boston Bruins", "New Jersey Devils", "Florida Panthers", "Calgary Flames"],
        "captain_years": 3,
        "stanley_cups": 2,
        "biography": "Second all-time in NHL points, Jagr's combination of size, skill, and longevity made him one of hockey's most dominant players. Won five scoring titles and played professionally well into his 40s."
    },
    {
        "name": "Terry Sawchuk",
        "birth_date": "1929-12-28",
        "nationality": "Canadian",
        "position": "Goalie",
        "games_played": 971,
        "goals": 0,
        "assists": 0,
        "points": 0,
        "teams": ["Detroit Red Wings", "Boston Bruins", "Toronto Maple Leafs", "Los Angeles Kings", "New York Rangers"],
        "captain_years": 0,
        "stanley_cups": 4,
        "biography": "Revolutionary goaltender who set the standard for the position. His 103 shutouts stood as a record for decades until Martin Brodeur broke it."
    },
    {
        "name": "Denis Potvin",
        "birth_date": "1953-10-29",
        "nationality": "Canadian",
        "position": "Defenseman",
        "games_played": 1060,
        "goals": 310,
        "assists": 742,
        "points": 1052,
        "teams": ["New York Islanders"],
        "captain_years": 8,
        "stanley_cups": 4,
        "biography": "Captain of the Islanders dynasty that won four straight Stanley Cups. Combined offensive skill with physical play to revolutionize the defenseman position."
    },
    {
        "name": "Peter Forsberg",
        "birth_date": "1973-07-20",
        "nationality": "Swedish",
        "position": "Center",
        "games_played": 708,
        "goals": 249,
        "assists": 636,
        "points": 885,
        "teams": ["Quebec Nordiques", "Colorado Avalanche", "Philadelphia Flyers", "Nashville Predators"],
        "captain_years": 3,
        "stanley_cups": 2,
        "biography": "One of the most complete players in NHL history, combining skill, vision, and physical play. Career was shortened by injuries but maintained nearly point-per-game average."
    },
    {
        "name": "Mike Bossy",
        "birth_date": "1957-01-22",
        "nationality": "Canadian",
        "position": "Right Wing",
        "games_played": 752,
        "goals": 573,
        "assists": 553,
        "points": 1126,
        "teams": ["New York Islanders"],
        "captain_years": 0,
        "stanley_cups": 4,
        "biography": "Pure goal scorer who scored 50+ goals in nine consecutive seasons. Career cut short by back injuries but still maintained highest goals-per-game average in NHL history."
    },
    {
        "name": "Paul Coffey",
        "birth_date": "1961-06-01",
        "nationality": "Canadian",
        "position": "Defenseman",
        "games_played": 1409,
        "goals": 396,
        "assists": 1135,
        "points": 1531,
        "teams": ["Edmonton Oilers", "Pittsburgh Penguins", "Los Angeles Kings", "Detroit Red Wings", "Hartford Whalers", "Philadelphia Flyers", "Chicago Blackhawks", "Carolina Hurricanes", "Boston Bruins"],
        "captain_years": 0,
        "stanley_cups": 4,
        "biography": "One of the fastest skaters in NHL history, Coffey redefined offensive defenseman role. Second all-time in points by a defenseman."
    },
    {
        "name": "Marcel Dionne",
        "birth_date": "1951-08-03",
        "nationality": "Canadian",
        "position": "Center",
        "games_played": 1348,
        "goals": 731,
        "assists": 1040,
        "points": 1771,
        "teams": ["Detroit Red Wings", "Los Angeles Kings", "New York Rangers"],
        "captain_years": 8,
        "stanley_cups": 0,
        "biography": "One of the most consistent scorers in NHL history, recording eight straight 100-point seasons. Never won a Stanley Cup but was inducted into Hall of Fame in 1992."
    },
    {
        "name": "Chris Chelios",
        "birth_date": "1962-01-25",
        "nationality": "American",
        "position": "Defenseman",
        "games_played": 1651,
        "goals": 185,
        "assists": 763,
        "points": 948,
        "teams": ["Montreal Canadiens", "Chicago Blackhawks", "Detroit Red Wings", "Atlanta Thrashers"],
        "captain_years": 4,
        "stanley_cups": 3,
        "biography": "Known for his longevity and competitive spirit, Chelios played until age 48. Won Norris Trophy three times and represented USA in four Olympics."
    },
    {
        "name": "Stan Mikita",
        "birth_date": "1940-05-20",
        "nationality": "Slovak-Canadian",
        "position": "Center",
        "games_played": 1394,
        "goals": 541,
        "assists": 926,
        "points": 1467,
        "teams": ["Chicago Black Hawks"],
        "captain_years": 2,
        "stanley_cups": 1,
        "biography": "Spent entire 22-year career with Chicago, revolutionizing the curved stick blade. Only player to win Art Ross, Hart, and Lady Byng trophies in same season, doing it twice."
    },
    {
        "name": "Jacques Plante",
        "birth_date": "1929-01-17",
        "nationality": "Canadian",
        "position": "Goalie",
        "games_played": 837,
        "goals": 0,
        "assists": 0,
        "points": 0,
        "teams": ["Montreal Canadiens", "New York Rangers", "St. Louis Blues", "Toronto Maple Leafs", "Boston Bruins"],
        "captain_years": 0,
        "stanley_cups": 6,
        "biography": "Revolutionary goalie who popularized the face mask and was first to regularly play puck outside crease. Won six Stanley Cups with Montreal and seven Vezina Trophies."
    },
    {
        "name": "Nicklas Lidstrom",
        "birth_date": "1970-04-28",
        "nationality": "Swedish",
        "position": "Defenseman",
        "games_played": 1564,
        "goals": 264,
        "assists": 878,
        "points": 1142,
        "teams": ["Detroit Red Wings"],
        "captain_years": 6,
        "stanley_cups": 4,
        "biography": "Known as 'The Perfect Human' for his flawless positioning and consistency. Won seven Norris Trophies and four Stanley Cups while playing entire career with Detroit."
    }
]

# Function to insert players
def insert_players():
    # Clear existing data first (optional)
    supabase.table('hockey_players').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
    
    # Insert players in batches to avoid timeout
    batch_size = 5
    for i in range(0, len(players_data), batch_size):
        batch = players_data[i:i + batch_size]
        supabase.table('hockey_players').insert(batch).execute()
        print(f"Inserted players {i+1} to {min(i+batch_size, len(players_data))}")

def main():
    try:
        # Insert players
        insert_players()
        print("Successfully inserted player data!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if _name_ == "_main_":
    main()