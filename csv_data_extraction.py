import json

def load_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data

# Get match data
def match_data(data):
# List of columns that will be extracted    
    city_list = []
    match_date_list = []
    match_number_list = []
    match_name_list = []
    match_winner_list = []
    player_of_match_list = []
    venue_list = []

# Extract the data
    info = data['info']
    city = info.get('city')
    match_dates = info.get('dates', [])
    match_number = info.get('event', {}).get('match_number')
    match_name = info.get('event', {}).get('name')
    match_winner = info.get('outcome', {}).get('winner')
    player_of_match = info.get('player_of_match', [])
    venue = info.get('venue')

    # Append the respective list
    city_list.extend([city] * len(match_dates))
    match_date_list.extend(match_dates)
    match_number_list.extend([match_number] * len(match_dates))
    match_name_list.extend([match_name] * len(match_dates))
    match_winner_list.extend([match_winner] * len(match_dates))
    player_of_match_list.extend(player_of_match)
    venue_list.extend([venue] * len(match_dates))

    return city_list, match_date_list, match_number_list, match_name_list, match_winner_list, player_of_match_list, venue_list


# Iterating over each innings to extract the values
def innings_data(data):
# List of columns that will be extracted
    team_list = []
    over_list = []
    batter_list = []
    bowler_list = []
    non_striker_list = []
    batter_runs_list = []
    extras_list = []
    total_runs_list = []
    wicket_kind_list = []
    player_out_list = []
    fielders_list = []
    match_date_list = []

    info = data['info']
    match_dates = info.get('dates', [])

# Extract the data
    for innings in data['innings']:
        team = innings.get('team')
        overs = innings.get('overs')

# Iterrating over each over    
        for over_data in overs:
            over = over_data.get('over')
            deliveries = over_data.get('deliveries')

# Iterating over each delivery
            for delivery in deliveries:
                batter = delivery.get('batter')
                bowler = delivery.get("bowler")
                non_striker = delivery.get("non_striker")
                runs = delivery.get("runs")
                extras = delivery.get("extras", {})
                wickets = delivery.get("wickets", [])   

# Extract runs data
                batter_runs = runs.get('batter', 0)
                extra_runs = sum(extras.values())
                total_runs = runs.get('total', 0)

# Append data to respective lists
                match_date_list.extend(match_dates)
                team_list.append(team)
                over_list.append(over)
                batter_list.append(batter)
                bowler_list.append(bowler)
                non_striker_list.append(non_striker)
                batter_runs_list.append(batter_runs)
                extras_list.append(extra_runs)
                total_runs_list.append(total_runs)

# Extract wicktes data 
                if wickets:
                    wicket = wickets[0]
                    wicket_kind = wicket.get('kind')
                    player_out = wicket.get('player_out')
                    fielders = ", ".join(fielder.get("name") for fielder in wicket.get("fielders", []))
                else:
                    wicket_kind = None
                    player_out = None
                    fielders = None

# Append wicket data to respective list
                wicket_kind_list.append(wicket_kind)
                player_out_list.append(player_out)
                fielders_list.append(fielders)

 # Return extracted data as separate lists
    return match_date_list, team_list, over_list, batter_list, bowler_list, non_striker_list, batter_runs_list, extras_list, total_runs_list, wicket_kind_list, player_out_list, fielders_list


def main():

    input_file = '<replace_path>.json'

    city, match_date, match_number, match_name, match_winner, player_of_match, venue = match_data(load_json(input_file))

    match_filename = f"<replace_path>/match_data_{match_date[0]}_{venue[0]}.csv"

    with open(match_filename, 'w') as f:
        f.write("City,Match_Date,Match_Number,Match_Name,Match_Winner,Player_of_Match,Venue\n")
        for i in range(len(match_date)):
            f.write(f"{city[i]},{match_date[i]},{match_number[i]},{match_name[i]},{match_winner[i]},{player_of_match[i]},{venue[i]}\n")


    match_date, team, over, batter, bowler, non_striker, batter_runs, extras, total_runs, wicket_kind, player_out, fielders = innings_data(load_json(input_file))

    # Write innings data to CSV file
    innings_filename = f"<replace_path>/innings_data_{match_date[0]}_{venue[0]}.csv"
    with open(innings_filename, 'w') as f:
        f.write("Match_Date,Team,Over,Batter,Bowler,Non_Striker,Batter_Runs,Extras,Total_Runs,Wicket_Kind,Player_Out,Fielders\n")
        for i in range(len(match_date)):
            f.write(f"{match_date[i]},{team[i]},{over[i]},{batter[i]},{bowler[i]},{non_striker[i]},{batter_runs[i]},{extras[i]},{total_runs[i]},{wicket_kind[i]},{player_out[i]},{fielders[i]}\n")

if __name__ == "__main__":
    main()    
