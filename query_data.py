import os
import sys
import sqlite3
import argparse

DB_PATH = os.path.join(os.path.dirname(__file__), "champions_league.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def show_standings(limit=36):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"""
    SELECT position, team, country, played, won, drawn, lost, goals_for, goals_against, goal_diff, points, qualification
    FROM standings
    ORDER BY position ASC
    LIMIT {limit}
    """)
    rows = cur.fetchall()
    conn.close()

    header = f"{'Pos':<4} {'Equipo':<22} {'País':<12} {'PJ':<4} {'G':<3} {'E':<3} {'P':<3} {'GF':<4} {'GC':<4} {'DG':<5} {'Pts':<4} {'Clasificación'}"
    print("\n" + "=" * len(header))
    print(" TABLA DE POSICIONES - UEFA CHAMPIONS LEAGUE (FASE DE LIGA)")
    print("=" * len(header))
    print(header)
    print("-" * len(header))
    for r in rows:
        print(f"{r[0]:<4} {r[1]:<22} {r[2]:<12} {r[3]:<4} {r[4]:<3} {r[5]:<3} {r[6]:<3} {r[7]:<4} {r[8]:<4} {r[9]:<+5} {r[10]:<4} {r[11]}")
    print("=" * len(header) + "\n")

def show_team_matches(team_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT matchday, date, home_team, home_score, away_score, away_team, status
    FROM matches
    WHERE LOWER(home_team) LIKE LOWER(?) OR LOWER(away_team) LIKE LOWER(?)
    ORDER BY matchday ASC
    """, (f"%{team_name}%", f"%{team_name}%"))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print(f"\n[!] No se encontraron partidos para '{team_name}'.\n")
        return

    print(f"\nPartidos para '{team_name}' ({len(rows)} encontrados):")
    print("-" * 65)
    print(f"{'Jor':<4} {'Fecha':<12} {'Local':<20} {'Res':^7} {'Visitante':<20}")
    print("-" * 65)
    for r in rows:
        res = f"{r[3]} - {r[4]}" if r[3] is not None and r[4] is not None else "vs"
        print(f"{r[0]:<4} {r[1]:<12} {r[2]:<20} {res:^7} {r[5]:<20}")
    print("-" * 65 + "\n")

def show_matchday(m_day):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT match_id, date, home_team, home_score, away_score, away_team
    FROM matches
    WHERE matchday = ?
    ORDER BY date ASC, match_id ASC
    """, (m_day,))
    rows = cur.fetchall()
    conn.close()

    print(f"\nPartidos de la Jornada {m_day} ({len(rows)} partidos):")
    print("-" * 65)
    for r in rows:
        res = f"{r[3]} - {r[4]}" if r[3] is not None and r[4] is not None else "vs"
        print(f"[{r[1]}] {r[2]:<22} {res:^7} {r[5]:<22}")
    print("-" * 65 + "\n")

def show_stats():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM matches WHERE status='FINISHED'")
    total_played = cur.fetchone()[0]
    cur.execute("SELECT SUM(home_score + away_score) FROM matches WHERE status='FINISHED'")
    total_goals = cur.fetchone()[0]
    cur.execute("SELECT team, goals_for FROM standings ORDER BY goals_for DESC LIMIT 3")
    top_scoring = cur.fetchall()
    cur.execute("SELECT team, goals_against FROM standings ORDER BY goals_against ASC LIMIT 3")
    best_defense = cur.fetchall()
    conn.close()

    avg_goals = total_goals / total_played if total_played else 0
    print("\n" + "=" * 50)
    print(" ESTADÍSTICAS GLOBALES DEL TORNEO")
    print("=" * 50)
    print(f"Total Partidos jugados:      {total_played}")
    print(f"Total Goles convertidos:     {total_goals}")
    print(f"Promedio de goles/partido:   {avg_goals:.2f}")
    print("\nEquipos más goleadores:")
    for t in top_scoring:
        print(f"  - {t[0]}: {t[1]} goles")
    print("\nMejores defensas (menos goles recibidos):")
    for t in best_defense:
        print(f"  - {t[0]}: {t[1]} goles recibidos")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Explorador de Datos de UEFA Champions League")
    parser.add_argument("--standings", action="store_true", help="Mostrar tabla de posiciones")
    parser.add_argument("--team", type=str, help="Consultar partidos de un equipo")
    parser.add_argument("--matchday", type=int, help="Consultar partidos de una jornada (1 a 8)")
    parser.add_argument("--stats", action="store_true", help="Mostrar estadísticas globales")
    
    args = parser.parse_args()
    if len(sys.argv) == 1:
        show_standings(8)
        show_stats()
        print("Tip: Usa 'python query_data.py --help' para ver más opciones de consulta.")
    else:
        if args.standings:
            show_standings()
        if args.team:
            show_team_matches(args.team)
        if args.matchday:
            show_matchday(args.matchday)
        if args.stats:
            show_stats()
