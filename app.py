import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.data_loader import load_data

st.set_page_config(
    page_title="Ronaldo: EDA Dashboard",
    page_icon="",
    layout="wide" 
)

sns.set_theme(style="whitegrid", palette="muted")


df = load_data()


st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg", use_container_width=True)
st.sidebar.header(" Фильтры")

competitions = sorted(df["competition"].dropna().unique())
selected_comps = st.sidebar.multiselect(
    "Выберите турниры:",
    options=competitions,
    default=competitions
)

venues = ["Дома", "В гостях"]
selected_venues = st.sidebar.multiselect(
    "Где забивал:",
    options=venues,
    default=venues
)

filtered_df = df[
    (df["competition"].isin(selected_comps)) & 
    (df["home_away_clean"].isin(selected_venues))
]


st.title(" Анализ голов Криштиану Роналду")
st.markdown(f"**Выбрано голов:** {len(filtered_df)} из 816.")

if filtered_df.empty:
    st.warning(" По выбранным фильтрам нет данных. Попробуйте изменить параметры в боковой панели.")
    st.stop() 


col1, col2, col3, col4 = st.columns(4)
penalties = len(filtered_df[filtered_df["goal_method"].str.contains("Penalty", case=False, na=False)])
top_opponent = filtered_df["opponent"].mode()[0] if not filtered_df["opponent"].mode().empty else "-"
top_interval = filtered_df["goal_minute_bucket"].mode()[0] if not filtered_df["goal_minute_bucket"].mode().empty else "-"

with col1: st.metric("Всего голов", len(filtered_df))
with col2: st.metric("Голы с пенальти", penalties)
with col3: st.metric("Любимый соперник", top_opponent)
with col4: st.metric("Любимое время", f"{top_interval} мин")

st.divider() 


row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader(" Голы по сезонам")
    season_goals = (
        filtered_df.dropna(subset=["season_start"])
        .groupby(["season_start", "season"]).size().reset_index(name="goals")
        .sort_values("season_start")
    )
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=season_goals, x="season", y="goals", color="#1f77b4", ax=ax1)
    ax1.tick_params(axis='x', rotation=45)
    sns.despine(ax=ax1)
    st.pyplot(fig1, clear_figure=True)

with row1_col2:
    st.subheader(" Способы голов")
    method_counts = filtered_df["goal_method"].fillna("Unknown").value_counts().reset_index()
    method_counts.columns = ["method", "goals"]
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=method_counts, y="method", x="goals", hue="method", palette="crest", legend=False, ax=ax2)
    sns.despine(ax=ax2)
    st.pyplot(fig2, clear_figure=True)

st.divider()


row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader(" Голы по интервалам минут")
    interval_counts = filtered_df["goal_minute_bucket"].value_counts().reset_index()
    interval_counts.columns = ["interval", "goals"]
    interval_counts = interval_counts.sort_values("interval") 
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=interval_counts, x="interval", y="goals", hue="interval", palette="rocket", legend=False, ax=ax3)
    sns.despine(ax=ax3)
    st.pyplot(fig3, clear_figure=True)

with row2_col2:
    st.subheader(" Топ-10 соперников")
    opp_counts = filtered_df["opponent"].value_counts().head(10).reset_index()
    opp_counts.columns = ["opponent", "goals"]
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=opp_counts, y="opponent", x="goals", hue="opponent", palette="magma", legend=False, ax=ax4)
    sns.despine(ax=ax4)
    st.pyplot(fig4, clear_figure=True)

st.divider()


row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    st.subheader(" Дома или в гостях?")
    home_away_counts = filtered_df["home_away_clean"].value_counts().reset_index()
    home_away_counts.columns = ["venue", "goals"]
    
    fig5, ax5 = plt.subplots(figsize=(6, 5))
    sns.barplot(data=home_away_counts, x="venue", y="goals", hue="venue", palette="Set2", legend=False, ax=ax5)
    
    ax5.set_xlabel("") 
    ax5.set_ylabel("Количество голов") 
    
    
    for container in ax5.containers:
        ax5.bar_label(container, fontsize=10, padding=3)
        
    sns.despine(ax=ax5)
    st.pyplot(fig5, clear_figure=True)

with row3_col2:
    st.subheader(" Корреляция признаков")
    numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols = [c for c in numeric_cols if filtered_df[c].notna().sum() > 0 and c != "goal_minute"]
    
    if len(numeric_cols) >= 2:
        corr = filtered_df[numeric_cols].corr()
        rename_dict = {"is_home_goal": "Дома/В гостях", "season_start": "Сезон", "minute_approx": "Минута"}
        corr = corr.rename(index=rename_dict, columns=rename_dict)
        
        fig6, ax6 = plt.subplots(figsize=(6, 5))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, square=True, linewidths=1, ax=ax6)
        st.pyplot(fig6, clear_figure=True)
    else:
        st.info("Недостаточно данных для корреляции.")

st.divider()


st.subheader(" Тепловая карта: Сезон × Интервал минут")
pivot = pd.crosstab(index=filtered_df["season"], columns=filtered_df["goal_minute_bucket"])


season_order = (
    filtered_df.dropna(subset=["season", "season_start"])
    .drop_duplicates("season").sort_values("season_start")["season"].tolist()
)
pivot = pivot.reindex([s for s in season_order if s in pivot.index])


minute_order = ['01-15', '16-30', '31-45', '46-60', '61-75', '76-90', '90+']
pivot = pivot[[col for col in minute_order if col in pivot.columns]]

fig7, ax7 = plt.subplots(figsize=(14, 7))
sns.heatmap(pivot, cmap="YlOrRd", linewidths=0.4, annot=True, fmt="d", cbar_kws={"label": "Голов"}, ax=ax7)
ax7.set_xlabel("Интервал минуты")
ax7.set_ylabel("Сезон")
st.pyplot(fig7, clear_figure=True)


st.divider()
with st.expander(" Посмотреть сырые данные (таблица)"):
    st.dataframe(
        filtered_df[["match_date", "competition", "opponent", "goal_minute_bucket", "goal_method"]]
        .sort_values("match_date", ascending=False),
        use_container_width=True
    )