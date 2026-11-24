import os
import csv
import json
import sqlite3

REPO_DIR = r"c:\Users\rexxd\Downloads\champions_league_data_repo"
os.makedirs(REPO_DIR, exist_ok=True)

# 1. 36 Equipos de la UEFA Champions League 2024/25
teams_data = [
    {"team_id": 1, "name": "Real Madrid", "short_name": "RMA", "country": "España", "league": "LaLiga", "pot": 1, "stadium": "Santiago Bernabéu", "city": "Madrid"},
    {"team_id": 2, "name": "Manchester City", "short_name": "MCI", "country": "Inglaterra", "league": "Premier League", "pot": 1, "stadium": "Etihad Stadium", "city": "Manchester"},
    {"team_id": 3, "name": "Bayern Múnich", "short_name": "BAY", "country": "Alemania", "league": "Bundesliga", "pot": 1, "stadium": "Allianz Arena", "city": "Múnich"},
    {"team_id": 4, "name": "Paris Saint-Germain", "short_name": "PSG", "country": "Francia", "league": "Ligue 1", "pot": 1, "stadium": "Parc des Princes", "city": "París"},
    {"team_id": 5, "name": "Liverpool", "short_name": "LIV", "country": "Inglaterra", "league": "Premier League", "pot": 1, "stadium": "Anfield", "city": "Liverpool"},
    {"team_id": 6, "name": "Inter de Milán", "short_name": "INT", "country": "Italia", "league": "Serie A", "pot": 1, "stadium": "San Siro", "city": "Milán"},
    {"team_id": 7, "name": "Borussia Dortmund", "short_name": "BVB", "country": "Alemania", "league": "Bundesliga", "pot": 1, "stadium": "Signal Iduna Park", "city": "Dortmund"},
    {"team_id": 8, "name": "RB Leipzig", "short_name": "RBL", "country": "Alemania", "league": "Bundesliga", "pot": 1, "stadium": "Red Bull Arena", "city": "Leipzig"},
    {"team_id": 9, "name": "Barcelona", "short_name": "BAR", "country": "España", "league": "LaLiga", "pot": 1, "stadium": "Estadi Olímpic Lluís Companys", "city": "Barcelona"},
    {"team_id": 10, "name": "Bayer Leverkusen", "short_name": "B04", "country": "Alemania", "league": "Bundesliga", "pot": 2, "stadium": "BayArena", "city": "Leverkusen"},
    {"team_id": 11, "name": "Atlético de Madrid", "short_name": "ATM", "country": "España", "league": "LaLiga", "pot": 2, "stadium": "Metropolitano", "city": "Madrid"},
    {"team_id": 12, "name": "Atalanta", "short_name": "ATA", "country": "Italia", "league": "Serie A", "pot": 2, "stadium": "Gewiss Stadium", "city": "Bérgamo"},
    {"team_id": 13, "name": "Juventus", "short_name": "JUV", "country": "Italia", "league": "Serie A", "pot": 2, "stadium": "Allianz Stadium", "city": "Turín"},
    {"team_id": 14, "name": "Benfica", "short_name": "SLB", "country": "Portugal", "league": "Primeira Liga", "pot": 2, "stadium": "Estádio da Luz", "city": "Lisboa"},
    {"team_id": 15, "name": "Arsenal", "short_name": "ARS", "country": "Inglaterra", "league": "Premier League", "pot": 2, "stadium": "Emirates Stadium", "city": "Londres"},
    {"team_id": 16, "name": "Club Brujas", "short_name": "BRU", "country": "Bélgica", "league": "Pro League", "pot": 2, "stadium": "Jan Breydel", "city": "Brujas"},
    {"team_id": 17, "name": "Shakhtar Donetsk", "short_name": "SHK", "country": "Ucrania", "league": "Premier League Ucraniana", "pot": 2, "stadium": "Veltins-Arena (neutral)", "city": "Gelsenkirchen"},
    {"team_id": 18, "name": "AC Milan", "short_name": "MIL", "country": "Italia", "league": "Serie A", "pot": 2, "stadium": "San Siro", "city": "Milán"},
    {"team_id": 19, "name": "Feyenoord", "short_name": "FEY", "country": "Países Bajos", "league": "Eredivisie", "pot": 3, "stadium": "De Kuip", "city": "Róterdam"},
    {"team_id": 20, "name": "Sporting CP", "short_name": "SCP", "country": "Portugal", "league": "Primeira Liga", "pot": 3, "stadium": "José Alvalade", "city": "Lisboa"},
    {"team_id": 21, "name": "PSV Eindhoven", "short_name": "PSV", "country": "Países Bajos", "league": "Eredivisie", "pot": 3, "stadium": "Philips Stadion", "city": "Eindhoven"},
    {"team_id": 22, "name": "Dinamo Zagreb", "short_name": "DZG", "country": "Croacia", "league": "HNL", "pot": 3, "stadium": "Maksimir", "city": "Zagreb"},
    {"team_id": 23, "name": "Red Bull Salzburgo", "short_name": "SAL", "country": "Austria", "league": "Bundesliga Austríaca", "pot": 3, "stadium": "Red Bull Arena", "city": "Salzburgo"},
    {"team_id": 24, "name": "Lille", "short_name": "LOSC", "country": "Francia", "league": "Ligue 1", "pot": 3, "stadium": "Decathlon Arena", "city": "Lille"},
    {"team_id": 25, "name": "Estrella Roja", "short_name": "CZV", "country": "Serbia", "league": "SuperLiga Serbia", "pot": 3, "stadium": "Rajko Mitić", "city": "Belgrado"},
    {"team_id": 26, "name": "Young Boys", "short_name": "YB", "country": "Suiza", "league": "Super League Suiza", "pot": 3, "stadium": "Wankdorf", "city": "Berna"},
    {"team_id": 27, "name": "Celtic", "short_name": "CEL", "country": "Escocia", "league": "Premiership Escocesa", "pot": 3, "stadium": "Celtic Park", "city": "Glasgow"},
    {"team_id": 28, "name": "Slovan Bratislava", "short_name": "SLO", "country": "Eslovaquia", "league": "Superliga Eslovaca", "pot": 4, "stadium": "Tehelné pole", "city": "Bratislava"},
    {"team_id": 29, "name": "AS Mónaco", "short_name": "ASM", "country": "Francia", "league": "Ligue 1", "pot": 4, "stadium": "Stade Louis II", "city": "Mónaco"},
    {"team_id": 30, "name": "Sparta Praga", "short_name": "SPA", "country": "República Checa", "league": "Fortuna Liga", "pot": 4, "stadium": "epet ARENA", "city": "Praga"},
    {"team_id": 31, "name": "Aston Villa", "short_name": "AVL", "country": "Inglaterra", "league": "Premier League", "pot": 4, "stadium": "Villa Park", "city": "Birmingham"},
    {"team_id": 32, "name": "Bologna", "short_name": "BOL", "country": "Italia", "league": "Serie A", "pot": 4, "stadium": "Renato Dall'Ara", "city": "Bolonia"},
    {"team_id": 33, "name": "Girona", "short_name": "GIR", "country": "España", "league": "LaLiga", "pot": 4, "stadium": "Montilivi", "city": "Girona"},
    {"team_id": 34, "name": "Stuttgart", "short_name": "VFB", "country": "Alemania", "league": "Bundesliga", "pot": 4, "stadium": "MHPArena", "city": "Stuttgart"},
    {"team_id": 35, "name": "Sturm Graz", "short_name": "STU", "country": "Austria", "league": "Bundesliga Austríaca", "pot": 4, "stadium": "Wörthersee Stadion", "city": "Klagenfurt"},
    {"team_id": 36, "name": "Brest", "short_name": "SB29", "country": "Francia", "league": "Ligue 1", "pot": 4, "stadium": "Stade de Roudourou", "city": "Guingamp"}
]

team_map = {t["name"]: t["team_id"] for t in teams_data}

# 2. Calendario de las 8 Jornadas oficiales
matches_raw = [
    # Jornada 1 (17-19 Sept 2024)
    (1, "2024-09-17", "Juventus", "PSV Eindhoven", 3, 1, "FINISHED"),
    (1, "2024-09-17", "Young Boys", "Aston Villa", 0, 3, "FINISHED"),
    (1, "2024-09-17", "Bayern Múnich", "Dinamo Zagreb", 9, 2, "FINISHED"),
    (1, "2024-09-17", "AC Milan", "Liverpool", 1, 3, "FINISHED"),
    (1, "2024-09-17", "Real Madrid", "Stuttgart", 3, 1, "FINISHED"),
    (1, "2024-09-17", "Sporting CP", "Lille", 2, 0, "FINISHED"),
    (1, "2024-09-18", "Sparta Praga", "Red Bull Salzburgo", 3, 0, "FINISHED"),
    (1, "2024-09-18", "Bologna", "Shakhtar Donetsk", 0, 0, "FINISHED"),
    (1, "2024-09-18", "Celtic", "Slovan Bratislava", 5, 1, "FINISHED"),
    (1, "2024-09-18", "Club Brujas", "Borussia Dortmund", 0, 3, "FINISHED"),
    (1, "2024-09-18", "Manchester City", "Inter de Milán", 0, 0, "FINISHED"),
    (1, "2024-09-18", "Paris Saint-Germain", "Girona", 1, 0, "FINISHED"),
    (1, "2024-09-19", "Feyenoord", "Bayer Leverkusen", 0, 4, "FINISHED"),
    (1, "2024-09-19", "Estrella Roja", "Benfica", 1, 2, "FINISHED"),
    (1, "2024-09-19", "AS Mónaco", "Barcelona", 2, 1, "FINISHED"),
    (1, "2024-09-19", "Atalanta", "Arsenal", 0, 0, "FINISHED"),
    (1, "2024-09-19", "Atlético de Madrid", "RB Leipzig", 2, 1, "FINISHED"),
    (1, "2024-09-19", "Brest", "Sturm Graz", 2, 1, "FINISHED"),

    # Jornada 2 (1-2 Oct 2024)
    (2, "2024-10-01", "Red Bull Salzburgo", "Brest", 0, 4, "FINISHED"),
    (2, "2024-10-01", "Stuttgart", "Sparta Praga", 1, 1, "FINISHED"),
    (2, "2024-10-01", "Arsenal", "Paris Saint-Germain", 2, 0, "FINISHED"),
    (2, "2024-10-01", "Bayer Leverkusen", "AC Milan", 1, 0, "FINISHED"),
    (2, "2024-10-01", "Borussia Dortmund", "Celtic", 7, 1, "FINISHED"),
    (2, "2024-10-01", "Barcelona", "Young Boys", 5, 0, "FINISHED"),
    (2, "2024-10-01", "Inter de Milán", "Estrella Roja", 4, 0, "FINISHED"),
    (2, "2024-10-01", "PSV Eindhoven", "Sporting CP", 1, 1, "FINISHED"),
    (2, "2024-10-01", "Slovan Bratislava", "Manchester City", 0, 4, "FINISHED"),
    (2, "2024-10-02", "Shakhtar Donetsk", "Atalanta", 0, 3, "FINISHED"),
    (2, "2024-10-02", "Girona", "Feyenoord", 2, 3, "FINISHED"),
    (2, "2024-10-02", "Aston Villa", "Bayern Múnich", 1, 0, "FINISHED"),
    (2, "2024-10-02", "Dinamo Zagreb", "AS Mónaco", 2, 2, "FINISHED"),
    (2, "2024-10-02", "Liverpool", "Bologna", 2, 0, "FINISHED"),
    (2, "2024-10-02", "Lille", "Real Madrid", 1, 0, "FINISHED"),
    (2, "2024-10-02", "RB Leipzig", "Juventus", 2, 3, "FINISHED"),
    (2, "2024-10-02", "Sturm Graz", "Club Brujas", 0, 1, "FINISHED"),
    (2, "2024-10-02", "Benfica", "Atlético de Madrid", 4, 0, "FINISHED"),

    # Jornada 3 (22-23 Oct 2024)
    (3, "2024-10-22", "AC Milan", "Club Brujas", 3, 1, "FINISHED"),
    (3, "2024-10-22", "AS Mónaco", "Estrella Roja", 5, 1, "FINISHED"),
    (3, "2024-10-22", "Arsenal", "Shakhtar Donetsk", 1, 0, "FINISHED"),
    (3, "2024-10-22", "Aston Villa", "Bologna", 2, 0, "FINISHED"),
    (3, "2024-10-22", "Girona", "Slovan Bratislava", 2, 0, "FINISHED"),
    (3, "2024-10-22", "Juventus", "Stuttgart", 0, 1, "FINISHED"),
    (3, "2024-10-22", "Paris Saint-Germain", "PSV Eindhoven", 1, 1, "FINISHED"),
    (3, "2024-10-22", "Real Madrid", "Borussia Dortmund", 5, 2, "FINISHED"),
    (3, "2024-10-22", "Sturm Graz", "Sporting CP", 0, 2, "FINISHED"),
    (3, "2024-10-23", "Atalanta", "Celtic", 0, 0, "FINISHED"),
    (3, "2024-10-23", "Brest", "Bayer Leverkusen", 1, 1, "FINISHED"),
    (3, "2024-10-23", "Atlético de Madrid", "Lille", 1, 3, "FINISHED"),
    (3, "2024-10-23", "Young Boys", "Inter de Milán", 0, 1, "FINISHED"),
    (3, "2024-10-23", "Barcelona", "Bayern Múnich", 4, 1, "FINISHED"),
    (3, "2024-10-23", "Red Bull Salzburgo", "Dinamo Zagreb", 0, 2, "FINISHED"),
    (3, "2024-10-23", "Manchester City", "Sparta Praga", 5, 0, "FINISHED"),
    (3, "2024-10-23", "RB Leipzig", "Liverpool", 0, 1, "FINISHED"),
    (3, "2024-10-23", "Benfica", "Feyenoord", 1, 3, "FINISHED"),

    # Jornada 4 (5-6 Nov 2024)
    (4, "2024-11-05", "PSV Eindhoven", "Girona", 4, 0, "FINISHED"),
    (4, "2024-11-05", "Slovan Bratislava", "Dinamo Zagreb", 1, 4, "FINISHED"),
    (4, "2024-11-05", "Bologna", "AS Mónaco", 0, 1, "FINISHED"),
    (4, "2024-11-05", "Borussia Dortmund", "Sturm Graz", 1, 0, "FINISHED"),
    (4, "2024-11-05", "Celtic", "RB Leipzig", 3, 1, "FINISHED"),
    (4, "2024-11-05", "Liverpool", "Bayer Leverkusen", 4, 0, "FINISHED"),
    (4, "2024-11-05", "Lille", "Juventus", 1, 1, "FINISHED"),
    (4, "2024-11-05", "Real Madrid", "AC Milan", 1, 3, "FINISHED"),
    (4, "2024-11-05", "Sporting CP", "Manchester City", 4, 1, "FINISHED"),
    (4, "2024-11-06", "Club Brujas", "Aston Villa", 1, 0, "FINISHED"),
    (4, "2024-11-06", "Shakhtar Donetsk", "Young Boys", 2, 1, "FINISHED"),
    (4, "2024-11-06", "Sparta Praga", "Brest", 1, 2, "FINISHED"),
    (4, "2024-11-06", "Bayern Múnich", "Benfica", 1, 0, "FINISHED"),
    (4, "2024-11-06", "Estrella Roja", "Barcelona", 2, 5, "FINISHED"),
    (4, "2024-11-06", "Feyenoord", "Red Bull Salzburgo", 1, 3, "FINISHED"),
    (4, "2024-11-06", "Inter de Milán", "Arsenal", 1, 0, "FINISHED"),
    (4, "2024-11-06", "Paris Saint-Germain", "Atlético de Madrid", 1, 2, "FINISHED"),
    (4, "2024-11-06", "Stuttgart", "Atalanta", 0, 2, "FINISHED"),

    # Jornada 5 (26-27 Nov 2024)
    (5, "2024-11-26", "Sparta Praga", "Atlético de Madrid", 0, 6, "FINISHED"),
    (5, "2024-11-26", "Slovan Bratislava", "AC Milan", 2, 3, "FINISHED"),
    (5, "2024-11-26", "Bayer Leverkusen", "Red Bull Salzburgo", 5, 0, "FINISHED"),
    (5, "2024-11-26", "Young Boys", "Atalanta", 1, 6, "FINISHED"),
    (5, "2024-11-26", "Barcelona", "Brest", 3, 0, "FINISHED"),
    (5, "2024-11-26", "Bayern Múnich", "Paris Saint-Germain", 1, 0, "FINISHED"),
    (5, "2024-11-26", "Inter de Milán", "RB Leipzig", 1, 0, "FINISHED"),
    (5, "2024-11-26", "Manchester City", "Feyenoord", 3, 3, "FINISHED"),
    (5, "2024-11-26", "Sporting CP", "Arsenal", 1, 5, "FINISHED"),
    (5, "2024-11-27", "Estrella Roja", "Stuttgart", 5, 1, "FINISHED"),
    (5, "2024-11-27", "Sturm Graz", "Girona", 1, 0, "FINISHED"),
    (5, "2024-11-27", "AS Mónaco", "Benfica", 2, 3, "FINISHED"),
    (5, "2024-11-27", "Aston Villa", "Juventus", 0, 0, "FINISHED"),
    (5, "2024-11-27", "Bologna", "Lille", 1, 2, "FINISHED"),
    (5, "2024-11-27", "Celtic", "Club Brujas", 1, 1, "FINISHED"),
    (5, "2024-11-27", "Dinamo Zagreb", "Borussia Dortmund", 0, 3, "FINISHED"),
    (5, "2024-11-27", "Liverpool", "Real Madrid", 2, 0, "FINISHED"),
    (5, "2024-11-27", "PSV Eindhoven", "Shakhtar Donetsk", 3, 2, "FINISHED"),

    # Jornada 6 (10-11 Dic 2024)
    (6, "2024-12-10", "Girona", "Liverpool", 0, 1, "FINISHED"),
    (6, "2024-12-10", "Dinamo Zagreb", "Celtic", 0, 0, "FINISHED"),
    (6, "2024-12-10", "Atalanta", "Real Madrid", 2, 3, "FINISHED"),
    (6, "2024-12-10", "Bayer Leverkusen", "Inter de Milán", 1, 0, "FINISHED"),
    (6, "2024-12-10", "Club Brujas", "Sporting CP", 2, 1, "FINISHED"),
    (6, "2024-12-10", "Red Bull Salzburgo", "Paris Saint-Germain", 0, 3, "FINISHED"),
    (6, "2024-12-10", "Shakhtar Donetsk", "Bayern Múnich", 1, 5, "FINISHED"),
    (6, "2024-12-10", "RB Leipzig", "Aston Villa", 2, 3, "FINISHED"),
    (6, "2024-12-10", "Brest", "PSV Eindhoven", 1, 0, "FINISHED"),
    (6, "2024-12-11", "Atlético de Madrid", "Slovan Bratislava", 3, 1, "FINISHED"),
    (6, "2024-12-11", "Lille", "Sturm Graz", 3, 2, "FINISHED"),
    (6, "2024-12-11", "AC Milan", "Estrella Roja", 2, 1, "FINISHED"),
    (6, "2024-12-11", "Arsenal", "AS Mónaco", 3, 0, "FINISHED"),
    (6, "2024-12-11", "Borussia Dortmund", "Barcelona", 2, 3, "FINISHED"),
    (6, "2024-12-11", "Feyenoord", "Sparta Praga", 4, 2, "FINISHED"),
    (6, "2024-12-11", "Juventus", "Manchester City", 2, 0, "FINISHED"),
    (6, "2024-12-11", "Benfica", "Bologna", 0, 0, "FINISHED"),
    (6, "2024-12-11", "Stuttgart", "Young Boys", 5, 1, "FINISHED"),

    # Jornada 7 (21-22 Ene 2025)
    (7, "2025-01-21", "AS Mónaco", "Aston Villa", 1, 0, "FINISHED"),
    (7, "2025-01-21", "Atalanta", "Sturm Graz", 5, 0, "FINISHED"),
    (7, "2025-01-21", "Atlético de Madrid", "Bayer Leverkusen", 2, 1, "FINISHED"),
    (7, "2025-01-21", "Bologna", "Borussia Dortmund", 2, 1, "FINISHED"),
    (7, "2025-01-21", "Club Brujas", "Juventus", 0, 0, "FINISHED"),
    (7, "2025-01-21", "Estrella Roja", "PSV Eindhoven", 2, 3, "FINISHED"),
    (7, "2025-01-21", "Liverpool", "Lille", 2, 1, "FINISHED"),
    (7, "2025-01-21", "Slovan Bratislava", "Stuttgart", 1, 3, "FINISHED"),
    (7, "2025-01-21", "Benfica", "Barcelona", 4, 5, "FINISHED"),
    (7, "2025-01-22", "Shakhtar Donetsk", "Brest", 2, 0, "FINISHED"),
    (7, "2025-01-22", "RB Leipzig", "Sporting CP", 2, 1, "FINISHED"),
    (7, "2025-01-22", "AC Milan", "Girona", 1, 0, "FINISHED"),
    (7, "2025-01-22", "Sparta Praga", "Inter de Milán", 0, 1, "FINISHED"),
    (7, "2025-01-22", "Arsenal", "Dinamo Zagreb", 3, 0, "FINISHED"),
    (7, "2025-01-22", "Celtic", "Young Boys", 1, 0, "FINISHED"),
    (7, "2025-01-22", "Feyenoord", "Bayern Múnich", 3, 0, "FINISHED"),
    (7, "2025-01-22", "Paris Saint-Germain", "Manchester City", 4, 2, "FINISHED"),
    (7, "2025-01-22", "Real Madrid", "Red Bull Salzburgo", 5, 1, "FINISHED"),

    # Jornada 8 (29 Ene 2025)
    (8, "2025-01-29", "Aston Villa", "Celtic", 4, 2, "FINISHED"),
    (8, "2025-01-29", "Bayer Leverkusen", "Sparta Praga", 2, 0, "FINISHED"),
    (8, "2025-01-29", "Borussia Dortmund", "Shakhtar Donetsk", 3, 1, "FINISHED"),
    (8, "2025-01-29", "Young Boys", "Estrella Roja", 0, 1, "FINISHED"),
    (8, "2025-01-29", "Barcelona", "Atalanta", 2, 2, "FINISHED"),
    (8, "2025-01-29", "Bayern Múnich", "Slovan Bratislava", 3, 1, "FINISHED"),
    (8, "2025-01-29", "Inter de Milán", "AS Mónaco", 3, 0, "FINISHED"),
    (8, "2025-01-29", "Red Bull Salzburgo", "Atlético de Madrid", 1, 4, "FINISHED"),
    (8, "2025-01-29", "Girona", "Arsenal", 1, 2, "FINISHED"),
    (8, "2025-01-29", "Dinamo Zagreb", "AC Milan", 2, 1, "FINISHED"),
    (8, "2025-01-29", "Juventus", "Benfica", 0, 2, "FINISHED"),
    (8, "2025-01-29", "Lille", "Feyenoord", 6, 1, "FINISHED"),
    (8, "2025-01-29", "Manchester City", "Club Brujas", 3, 1, "FINISHED"),
    (8, "2025-01-29", "PSV Eindhoven", "Liverpool", 3, 2, "FINISHED"),
    (8, "2025-01-29", "Sturm Graz", "RB Leipzig", 1, 0, "FINISHED"),
    (8, "2025-01-29", "Sporting CP", "Bologna", 1, 1, "FINISHED"),
    (8, "2025-01-29", "Brest", "Real Madrid", 0, 3, "FINISHED"),
    (8, "2025-01-29", "Stuttgart", "Paris Saint-Germain", 1, 4, "FINISHED"),
]

matches_data = []
for idx, m in enumerate(matches_raw, 1):
    m_day, m_date, h_name, a_name, h_score, a_score, status = m
    h_id = team_map[h_name]
    a_id = team_map[a_name]
    matches_data.append({
        "match_id": idx,
        "matchday": m_day,
        "date": m_date,
        "home_team_id": h_id,
        "away_team_id": a_id,
        "home_team": h_name,
        "away_team": a_name,
        "home_score": h_score,
        "away_score": a_score,
        "status": status
    })

# Exportar teams.csv
teams_csv_path = os.path.join(REPO_DIR, "teams.csv")
with open(teams_csv_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=list(teams_data[0].keys()))
    writer.writeheader()
    writer.writerows(teams_data)

# Exportar matches.csv
matches_csv_path = os.path.join(REPO_DIR, "matches.csv")
with open(matches_csv_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=list(matches_data[0].keys()))
    writer.writeheader()
    writer.writerows(matches_data)

# Calcular Tabla de Posiciones de la Fase de Liga (Standings)
standings = {t["name"]: {
    "team_id": t["team_id"],
    "team": t["name"],
    "country": t["country"],
    "played": 0, "won": 0, "drawn": 0, "lost": 0,
    "goals_for": 0, "goals_against": 0, "goal_diff": 0, "points": 0
} for t in teams_data}

for m in matches_data:
    if m["status"] == "FINISHED":
        ht = m["home_team"]
        at = m["away_team"]
        hs = m["home_score"]
        as_ = m["away_score"]
        
        standings[ht]["played"] += 1
        standings[at]["played"] += 1
        standings[ht]["goals_for"] += hs
        standings[ht]["goals_against"] += as_
        standings[at]["goals_for"] += as_
        standings[at]["goals_against"] += hs

        if hs > as_:
            standings[ht]["won"] += 1
            standings[ht]["points"] += 3
            standings[at]["lost"] += 1
        elif hs < as_:
            standings[at]["won"] += 1
            standings[at]["points"] += 3
            standings[ht]["lost"] += 1
        else:
            standings[ht]["drawn"] += 1
            standings[ht]["points"] += 1
            standings[at]["drawn"] += 1
            standings[at]["points"] += 1

for t in standings.values():
    t["goal_diff"] = t["goals_for"] - t["goals_against"]

standings_list = list(standings.values())
standings_list.sort(key=lambda x: (x["points"], x["goal_diff"], x["goals_for"]), reverse=True)

for i, row in enumerate(standings_list, 1):
    row["position"] = i
    if i <= 8:
        row["qualification"] = "Octavos de Final Directo"
    elif i <= 24:
        row["qualification"] = "Play-offs de Dieciseisavos"
    else:
        row["qualification"] = "Eliminado"

# Exportar standings.csv
standings_csv_path = os.path.join(REPO_DIR, "standings.csv")
with open(standings_csv_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=list(standings_list[0].keys()))
    writer.writeheader()
    writer.writerows(standings_list)

# Crear base de datos SQLite
db_path = os.path.join(REPO_DIR, "champions_league.db")
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Tabla teams
cur.execute("""
CREATE TABLE teams (
    team_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    short_name TEXT NOT NULL,
    country TEXT NOT NULL,
    league TEXT NOT NULL,
    pot INTEGER NOT NULL,
    stadium TEXT NOT NULL,
    city TEXT NOT NULL
);
""")

for t in teams_data:
    cur.execute("""
    INSERT INTO teams (team_id, name, short_name, country, league, pot, stadium, city)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (t["team_id"], t["name"], t["short_name"], t["country"], t["league"], t["pot"], t["stadium"], t["city"]))

# Tabla matches
cur.execute("""
CREATE TABLE matches (
    match_id INTEGER PRIMARY KEY,
    matchday INTEGER NOT NULL,
    date TEXT NOT NULL,
    home_team_id INTEGER NOT NULL,
    away_team_id INTEGER NOT NULL,
    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,
    home_score INTEGER,
    away_score INTEGER,
    status TEXT NOT NULL,
    FOREIGN KEY (home_team_id) REFERENCES teams (team_id),
    FOREIGN KEY (away_team_id) REFERENCES teams (team_id)
);
""")

for m in matches_data:
    cur.execute("""
    INSERT INTO matches (match_id, matchday, date, home_team_id, away_team_id, home_team, away_team, home_score, away_score, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (m["match_id"], m["matchday"], m["date"], m["home_team_id"], m["away_team_id"], m["home_team"], m["away_team"], m["home_score"], m["away_score"], m["status"]))

# Tabla standings
cur.execute("""
CREATE TABLE standings (
    position INTEGER PRIMARY KEY,
    team_id INTEGER NOT NULL,
    team TEXT NOT NULL,
    country TEXT NOT NULL,
    played INTEGER NOT NULL,
    won INTEGER NOT NULL,
    drawn INTEGER NOT NULL,
    lost INTEGER NOT NULL,
    goals_for INTEGER NOT NULL,
    goals_against INTEGER NOT NULL,
    goal_diff INTEGER NOT NULL,
    points INTEGER NOT NULL,
    qualification TEXT NOT NULL,
    FOREIGN KEY (team_id) REFERENCES teams (team_id)
);
""")

for s in standings_list:
    cur.execute("""
    INSERT INTO standings (position, team_id, team, country, played, won, drawn, lost, goals_for, goals_against, goal_diff, points, qualification)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (s["position"], s["team_id"], s["team"], s["country"], s["played"], s["won"], s["drawn"], s["lost"], s["goals_for"], s["goals_against"], s["goal_diff"], s["points"], s["qualification"]))

# Vista detallada de partidos
cur.execute("""
CREATE VIEW v_matches_full AS
SELECT 
    m.match_id,
    m.matchday,
    m.date,
    ht.name AS home_team,
    ht.country AS home_country,
    m.home_score,
    m.away_score,
    at.name AS away_team,
    at.country AS away_country,
    m.status
FROM matches m
JOIN teams ht ON m.home_team_id = ht.team_id
JOIN teams at ON m.away_team_id = at.team_id;
""")

conn.commit()
conn.close()

# Exportar JSON consolidado
full_repo = {
    "tournament": "UEFA Champions League 2024/25",
    "format": "Fase de Liga Unica (36 equipos, 8 jornadas)",
    "total_teams": len(teams_data),
    "total_matches": len(matches_data),
    "teams": teams_data,
    "matches": matches_data,
    "standings": standings_list
}

json_path = os.path.join(REPO_DIR, "champions_league_dataset.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(full_repo, f, ensure_ascii=False, indent=2)

print("Repositorio creado exitosamente:")
print(f"1. Base de Datos SQLite: {db_path}")
print(f"2. CSV Equipos: {teams_csv_path} ({len(teams_data)} equipos)")
print(f"3. CSV Partidos: {matches_csv_path} ({len(matches_data)} partidos)")
print(f"4. CSV Tabla de Posiciones: {standings_csv_path} ({len(standings_list)} equipos)")
print(f"5. JSON Completo: {json_path}")
