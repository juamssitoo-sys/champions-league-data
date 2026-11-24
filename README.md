# 🏆 Repositorio de Datos de la UEFA Champions League (Fase de Liga)

Repositorio estructurado de datos de los **36 clubes participantes** y los **144 partidos oficiales** de la Fase de Liga de la UEFA Champions League.

---

## 📁 Estructura del Repositorio

El repositorio se encuentra ubicado en:
`c:\Users\rexxd\Downloads\champions_league_data_repo\`

| Archivo | Formato | Descripción |
| :--- | :---: | :--- |
| `champions_league.db` | **SQLite** | Base de datos relacional completa con tablas `teams`, `matches`, `standings` y vistas SQL preconfiguradas. |
| `teams.csv` | **CSV** | Información detallada de los 36 clubes (ID, nombre, código, país, liga doméstica, bombo de sorteo, estadio y ciudad). |
| `matches.csv` | **CSV** | 144 partidos oficiales (Jornadas 1 a 8), fechas, equipos local/visitante, marcadores y estado. |
| `standings.csv` | **CSV** | Tabla de posiciones consolidada (PJ, G, E, P, GF, GC, DG, Puntos y criterio de clasificación: Directo a 8vos, Play-offs o Eliminado). |
| `champions_league_dataset.json` | **JSON** | Exportación completa en formato JSON jerárquico listo para APIs web o consumo frontend/NoSQL. |
| `build_repository.py` | **Python** | Script generador y constructor del repositorio a partir de datos estructurados. |
| `query_data.py` | **Python** | Herramienta CLI interactiva para consultar estadísticas, jornadas y partidos por equipo. |

---

## 📊 Esquema de la Base de Datos (`champions_league.db`)

### 1. Tabla `teams`
* `team_id` (INTEGER, PK): Identificador único del club.
* `name` (TEXT): Nombre oficial del club.
* `short_name` (TEXT): Código de 3 letras (ej. RMA, MCI, BAR).
* `country` (TEXT): País de procedencia.
* `league` (TEXT): Liga doméstica (LaLiga, Premier League, Serie A, etc.).
* `pot` (INTEGER): Bombo de sorteo UEFA (1 al 4).
* `stadium` (TEXT): Nombre del estadio local.
* `city` (TEXT): Ciudad sede.

### 2. Tabla `matches`
* `match_id` (INTEGER, PK): Identificador del partido.
* `matchday` (INTEGER): Jornada de la fase de liga (1 a 8).
* `date` (TEXT): Fecha del encuentro (formato YYYY-MM-DD).
* `home_team_id` (INTEGER, FK): ID del club local.
* `away_team_id` (INTEGER, FK): ID del club visitante.
* `home_team` (TEXT): Nombre del club local.
* `away_team` (TEXT): Nombre del club visitante.
* `home_score` (INTEGER): Goles del club local.
* `away_score` (INTEGER): Goles del club visitante.
* `status` (TEXT): Estado del partido (`FINISHED`, `SCHEDULED`).

### 3. Tabla `standings`
* `position` (INTEGER, PK): Posición en la tabla única (1 al 36).
* `team_id` (INTEGER, FK): ID del club.
* `team` (TEXT): Nombre del club.
* `country` (TEXT): País.
* `played` / `won` / `drawn` / `lost`: Partidos jugados, ganados, empatados y perdidos.
* `goals_for` / `goals_against` / `goal_diff`: Estadísticas de goles.
* `points`: Puntos acumulados.
* `qualification`: Estado clasificatorio (`Octavos de Final Directo`, `Play-offs de Dieciseisavos`, `Eliminado`).

---

## 🚀 Ejemplos de Uso

### 1. Consultas rápidas desde la terminal con `query_data.py`
```bash
# Ver los partidos de un equipo específico:
python query_data.py --team "Barcelona"
python query_data.py --team "Real Madrid"
python query_data.py --team "Manchester City"

# Ver todos los partidos de una jornada (del 1 al 8):
python query_data.py --matchday 5

# Ver la tabla de posiciones general:
python query_data.py --standings

# Ver estadísticas globales del torneo:
python query_data.py --stats
```

### 2. Consultas SQL comunes (SQLite)
```sql
-- Obtener los 8 clasificados directos a octavos:
SELECT position, team, points, goal_diff 
FROM standings 
WHERE position <= 8;

-- Obtener todos los partidos donde hubo más de 4 goles:
SELECT matchday, date, home_team, home_score, away_score, away_team
FROM matches
WHERE (home_score + away_score) >= 5
ORDER BY (home_score + away_score) DESC;

-- Rendimiento de los equipos por país:
SELECT t.country, COUNT(DISTINCT t.team_id) as total_equipos, SUM(s.points) as puntos_totales
FROM teams t
JOIN standings s ON t.team_id = s.team_id
GROUP BY t.country
ORDER BY puntos_totales DESC;
```
