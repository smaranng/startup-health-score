import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the scored data
df = pd.read_csv("outputs/final_scores.csv")

st.set_page_config(page_title="Startup Health Scoring", layout="wide")

st.title("🚀 Startup Health Scoring Dashboard")

# Sidebar filters
st.sidebar.header("📊 Filters")
top_bottom_option = st.sidebar.selectbox("View", ["All", "Top 10", "Bottom 10"])

# Filtered DataFrame
# New filtering based only on Top/Bottom selector
if top_bottom_option == "Top 10":
    filtered_df = df.sort_values(by="score", ascending=False).head(10)
elif top_bottom_option == "Bottom 10":
    filtered_df = df.sort_values(by="score", ascending=True).head(10)
else:
    filtered_df = df

# Dynamic heading above table based on filter selection
if top_bottom_option == "Top 10":
    st.subheader("📋 Showing Top 10 Startups by Score")
elif top_bottom_option == "Bottom 10":
    st.subheader("📋 Showing Bottom 10 Startups by Score")
else:
    st.subheader("📋 Showing All Startups")

st.dataframe(filtered_df, use_container_width=True)

# Score Distribution
st.subheader("📈 Score Distribution")
fig, ax = plt.subplots()
sns.histplot(df["score"], bins=20, kde=True, ax=ax)
ax.set_xlabel("Score")
st.pyplot(fig)

# Bar chart - Top 20
st.subheader("🏆 Top 20 Startups")
top20 = df.sort_values(by="score", ascending=False).head(20)
fig2, ax2 = plt.subplots(figsize=(12, 5))
sns.barplot(x="startup_id", y="score", data=top20, ax=ax2)
plt.xticks(rotation=45)
st.pyplot(fig2)

# Optional: Load full feature data if needed (merge with scores)
df_full = pd.read_csv("notebook/Startup_Scoring_Dataset.csv")
df_full = df_full.merge(df, on="startup_id")

# Correlation Heatmap
st.subheader("🧠 Correlation Between Features")

import numpy as np

# Select only numeric columns for correlation
numeric_cols = ['team_experience', 'market_size_million_usd', 'monthly_active_users',
                'monthly_burn_rate_inr', 'funds_raised_inr', 'valuation_inr']

# Compute correlation matrix
corr = df_full[numeric_cols].corr()

# Plot heatmap
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax3)
ax3.set_title("Feature Correlation Heatmap")
st.pyplot(fig3)
# Download button
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download Final Scores CSV", data=csv, file_name="startup_scores.csv", mime="text/csv")