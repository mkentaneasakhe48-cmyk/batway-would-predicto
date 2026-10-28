import streamlit as st
import math

st.set_page_config(page_title="World Match Predictor", layout="wide")
st.title("🌍 Worldwide Match Predictor")
st.caption("For ALL leagues - PSL, EPL, LaLiga, UCL, etc | 18+ | Educational Only - Gamble Responsibly")

col1, col2 = st.columns(2)
with col1:
    home = st.text_input("Home Team", "Mamelodi Sundowns")
    home_goals_scored = st.number_input(f"{home} Avg Goals Scored (last 10)", 0.0, 5.0, 1.8, 0.1)
    home_goals_conceded = st.number_input(f"{home} Avg Goals Conceded (last 10)", 0.0, 5.0, 0.9, 0.1)
    home_wins = st.slider(f"{home} Wins last 10 games", 0, 10, 6)

with col2:
    away = st.text_input("Away Team", "Kaizer Chiefs")
    away_goals_scored = st.number_input(f"{away} Avg Goals Scored (last 10)", 0.0, 5.0, 1.2, 0.1)
    away_goals_conceded = st.number_input(f"{away} Avg Goals Conceded (last 10)", 0.0, 5.0, 1.4, 0.1)
    away_wins = st.slider(f"{away} Wins last 10 games", 0, 10, 3)

st.divider()

if st.button("🔮 PREDICT MATCH", type="primary"):
    # Simple worldwide model: Attack vs Defence + Form
    home_attack = home_goals_scored / max(0.5, away_goals_conceded)
    away_attack = away_goals_scored / max(0.5, home_goals_conceded)
    
    home_form = home_wins / 10
    away_form = away_wins / 10
    home_advantage = 1.2  # home is 20% stronger worldwide avg

    home_strength = (home_attack * 0.6 + home_form * 0.4) * home_advantage
    away_strength = (away_attack * 0.6 + away_form * 0.4)
    
    total = home_strength + away_strength + 0.6  # 0.6 = draw factor
    home_prob = (home_strength / total) * 100
    away_prob = (away_strength / total) * 100
    draw_prob = 100 - home_prob - away_prob

    # Expected goals for Betway Over/Under
    exp_home_goals = (home_goals_scored + away_goals_conceded) / 2
    exp_away_goals = (away_goals_scored + home_goals_conceded) / 2
    exp_total = exp_home_goals + exp_away_goals

    # Decide signal
    if home_prob > 55:
        signal = f"✅ PREDICTION: {home} WIN"
        conf = home_prob
        risk = "LOW RISK" if home_prob > 65 else "MEDIUM RISK"
    elif away_prob > 55:
        signal = f"✅ PREDICTION: {away} WIN"
        conf = away_prob
        risk = "LOW RISK" if away_prob > 65 else "MEDIUM RISK"
    elif draw_prob > 33:
        signal = "⚠️ PREDICTION: DRAW"
        conf = draw_prob
        risk = "HIGH RISK - Draws are risky"
    else:
        signal = "⚠️ PREDICTION: CLOSE GAME - AVOID"
        conf = max(home_prob, away_prob)
        risk = "HIGH RISK"

    c1, c2, c3 = st.columns(3)
    c1.metric(f"{home} Win", f"{home_prob:.1f}%")
    c2.metric("Draw", f"{draw_prob:.1f}%")
    c3.metric(f"{away} Win", f"{away_prob:.1f}%")

    st.subheader(signal)
    st.write(f"**Confidence: {conf:.1f}% | {risk}**")
    st.write(f"**Expected Score:** {home} {exp_home_goals:.1f} - {exp_away_goals:.1f} {away}")
    st.write(f"**Expected Total Goals:** {exp_total:.1f} -> {'OVER 1.5 Goals' if exp_total > 1.5 else 'UNDER 1.5'} | {'OVER 2.5' if exp_total > 2.5 else 'UNDER 2.5'}")

    st.progress(int(conf))

    if conf < 55:
        st.warning("Confidence below 55% - DO NOT BET. Model says too risky.")
    elif conf >= 70:
        st.success(f"High Confidence {conf:.0f}% but still gamble responsibly - no guarantee!")

    st.divider()
    st.info("How it works: Worldwide average - Home advantage 20% + Attack strength + Last 10 form. For education only. Does NOT guarantee Betway win.")

st.divider()
st.caption("Disclaimer: This is statistical prediction only. Football is unpredictable. 18+ Gamble Responsibly. Try on demo. If you need help, contact South Africa Responsible Gambling: 0800 006 008")
