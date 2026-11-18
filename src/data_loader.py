import pandas as pd
import numpy as np

def load_data(filepath="data/ronaldo_goals_kaggle_ready.csv"):
    df = pd.read_csv(filepath)
    df["match_date"] = pd.to_datetime(df["match_date"], format="mixed", errors="coerce")
    
    def season_start(value):
        if pd.isna(value): return np.nan
        try: return int(str(value).split("/")[0])
        except: return np.nan
    df["season_start"] = df["season"].apply(season_start)
    
    if "home_away" in df.columns and df["home_away"].notna().any():
        df["home_away_clean"] = df["home_away"].map({"Home": "Дома", "Away": "В гостях"})
    else:
        df["home_away_clean"] = df["is_home_goal"].map({1: "Дома", 0: "В гостях"})

    def parse_bucket(bucket):
        if pd.isna(bucket) or str(bucket) == "": return np.nan
        s = str(bucket).strip()
        if "+" in s: return 90.0
        parts = s.split('-')
        if len(parts) == 2:
            try: return (int(parts[0]) + int(parts[1])) / 2
            except ValueError: return np.nan
        return np.nan
    df["minute_approx"] = df["goal_minute_bucket"].apply(parse_bucket)
        
       
    method_map = {
        "Right-footed shot": "Удар правой",
        "Penalty": "Пенальти",
        "Left-footed shot": "Удар левой",
        "Header": "Игра головой",
        "Direct free kick": "Штрафной удар",
        "Tap-in": "Добивание",
        "Long distance kick": "Дальний удар",
        "Counter attack goal": "Контратака",
        "Not reported": "Нет данных",
        "Penalty rebound": "Добивание с пенальти",
        "Solo run": "Сольный проход",
        "Deflected shot on goal": "Рикошет"
    }
    if "goal_method" in df.columns:
        df["goal_method"] = df["goal_method"].replace(method_map)

    comp_map = {
        "La Liga": "Ла Лига",
        "UEFA Champions League": "Лига Чемпионов",
        "Premier League": "АПЛ",
        "Serie A": "Серия А",
        "International": "Сборная",
        "FIFA World Cup": "ЧМ",
        "UEFA European Championship": "ЧЕ"
    }
    if "competition" in df.columns:
        df["competition"] = df["competition"].replace(comp_map)

    return df