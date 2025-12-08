import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Game Success Predictor",
    page_icon="🎮",
    layout="wide"
)

# Title
st.title("🎮 Game Success Prediction")
st.markdown("### Predict if your game will succeed on Steam")
st.markdown("---")


# Load model
@st.cache_resource
def load_model():
    model = joblib.load('../Model/best_model.pkl')
    features = joblib.load('../Model/feature_columns.pkl')
    model_info = joblib.load('../Model/model_info.pkl')
    return model, features, model_info


try:
    model, feature_columns, model_info = load_model()

    st.sidebar.success("✅ Model Loaded Successfully")
    st.sidebar.info(f"**Model:** {model_info['model_name']}")
    st.sidebar.metric("Test Accuracy", f"{model_info['accuracy'] * 100:.1f}%")
    st.sidebar.metric("F1-Score", f"{model_info['f1_score']:.3f}")

except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Tabs
tab1, tab2, tab3 = st.tabs(["📤 Upload & Predict", "🎯 Manual Input", "📊 About"])

# ===== Tab 1: CSV Upload =====
with tab1:
    st.header("Upload CSV for Batch Prediction")

    st.markdown("""
    **CSV Format Required:**
    Your CSV must include these columns: `Price`, `positive_ratio`, `total_reviews`, 
    `Recommendations`, `Achievements`, `Metacritic_score`, `platform_count`, `is_free`,
    `Average_playtime_forever`, `Peak_CCU`, `Hours_watched`, `Avg_viewers`, 
    `Peak_viewers`, `Streamers`, `watch_per_stream_hour`, `streaming_popularity`, 
    `community_engagement`

    Optional: `Name` column for game identification
    """)

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)

            st.success(f"✅ File uploaded: {len(df_upload)} games")

            # Check if required features exist
            missing_features = [f for f in feature_columns if f not in df_upload.columns]

            if missing_features:
                st.error(f"❌ Missing required columns: {missing_features}")
            else:
                # Make predictions
                X_upload = df_upload[feature_columns]
                predictions = model.predict(X_upload)
                probabilities = model.predict_proba(X_upload)[:, 1]

                # Add results to dataframe
                df_results = df_upload.copy()
                df_results['Predicted_Success'] = predictions
                df_results['Success_Probability'] = probabilities
                df_results['Prediction'] = df_results['Predicted_Success'].map({
                    0: '❌ Failure',
                    1: '✅ Success'
                })

                # Display results
                st.subheader("📊 Prediction Results")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Games", len(df_results))
                with col2:
                    success_count = (predictions == 1).sum()
                    st.metric("Predicted Success", success_count)
                with col3:
                    failure_count = (predictions == 0).sum()
                    st.metric("Predicted Failure", failure_count)

                # Show table
                st.dataframe(
                    df_results[['Name', 'Prediction', 'Success_Probability']]
                    if 'Name' in df_results.columns
                    else df_results[['Prediction', 'Success_Probability']],
                    use_container_width=True
                )

                # Download results
                csv = df_results.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Predictions",
                    data=csv,
                    file_name='predictions.csv',
                    mime='text/csv'
                )

                # Visualization
                st.subheader("📈 Prediction Distribution")
                fig = px.histogram(df_results, x='Success_Probability',
                                   nbins=30,
                                   color='Prediction',
                                   title='Success Probability Distribution')
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error processing file: {e}")

# ===== Tab 2: Manual Input =====
with tab2:
    st.header("🎮 Predict Single Game Success")

    st.markdown("Enter your game's expected metrics:")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Steam Metrics")
        price = st.number_input("Price ($)", min_value=0.0, max_value=200.0, value=9.99, step=0.99)
        positive_ratio = st.slider("Expected Positive Review %", 0, 100, 85) / 100
        total_reviews = st.number_input("Expected Total Reviews", min_value=0, value=500, step=50)
        recommendations = st.number_input("Expected Recommendations", min_value=0, value=500, step=50)
        achievements = st.number_input("Number of Achievements", min_value=0, value=20, step=5)
        metacritic = st.slider("Expected Metacritic Score", 0, 100, 70)
        playtime = st.number_input("Expected Avg Playtime (minutes)", min_value=0, value=300, step=30)
        peak_ccu = st.number_input("Expected Peak CCU", min_value=0, value=100, step=10)
        platform_count = st.selectbox("Platforms Supported", [1, 2, 3], index=0)
        is_free = st.checkbox("Free-to-play game")

    with col2:
        st.subheader("Twitch/Marketing Metrics")
        hours_watched = st.number_input("Expected Twitch Hours Watched", min_value=0, value=10000, step=1000)
        avg_viewers = st.number_input("Expected Avg Viewers", min_value=0, value=50, step=10)
        peak_viewers = st.number_input("Expected Peak Viewers", min_value=0, value=100, step=10)
        streamers = st.number_input("Expected Streamers", min_value=0, value=10, step=5)

        # Calculated fields
        watch_per_stream = hours_watched / max(1, streamers * 24)  # Rough estimate
        streaming_pop = np.log1p(hours_watched)
        community_eng = np.log1p(total_reviews) * np.log1p(avg_viewers)

    # Create input dataframe
    input_data = pd.DataFrame({
        'Price': [price],
        'positive_ratio': [positive_ratio],
        'total_reviews': [total_reviews],
        'Recommendations': [recommendations],
        'Achievements': [achievements],
        'Metacritic_score': [metacritic],
        'platform_count': [platform_count],
        'is_free': [int(is_free)],
        'Average_playtime_forever': [playtime],
        'Peak_CCU': [peak_ccu],
        'Hours_watched': [hours_watched],
        'Avg_viewers': [avg_viewers],
        'Peak_viewers': [peak_viewers],
        'Streamers': [streamers],
        'watch_per_stream_hour': [watch_per_stream],
        'streaming_popularity': [streaming_pop],
        'community_engagement': [community_eng]
    })
    # FIX
    # Python
    # 确保 input_data 的列与训练时的特征严格一致（相同列名且顺序相同）
    missing = [c for c in feature_columns if c not in input_data.columns]
    if missing:
        st.error(f"❌ 模型需要这些列但输入缺失: {missing}")
    else:
        # 以训练时的列顺序重排数据
        input_data = input_data[feature_columns]
        # 确保类型一致（可根据需要调整）
        if 'is_free' in input_data.columns:
            input_data['is_free'] = input_data['is_free'].astype(int)

        # 然后安全地预测
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0, 1]

    # Predict button
    if st.button("🔮 Predict Success", type="primary"):
        try:
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0, 1]

            st.markdown("---")
            st.subheader("🎯 Prediction Result")

            # Display result with color
            if prediction == 1:
                st.success(f"## ✅ SUCCESS PREDICTED")
                st.metric("Success Probability", f"{probability * 100:.1f}%")
            else:
                st.error(f"## ❌ FAILURE PREDICTED")
                st.metric("Failure Probability", f"{(1 - probability) * 100:.1f}%")

            # Confidence level
            if probability > 0.9 or probability < 0.1:
                confidence = "Very High"
            elif probability > 0.7 or probability < 0.3:
                confidence = "High"
            else:
                confidence = "Moderate"

            st.info(f"**Confidence Level:** {confidence}")

            # Gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=probability * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Success Probability"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkgreen" if prediction == 1 else "darkred"},
                    'steps': [
                        {'range': [0, 40], 'color': "lightgray"},
                        {'range': [40, 60], 'color': "lightyellow"},
                        {'range': [60, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 50
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

            # Recommendations
            st.markdown("### 💡 Recommendations")

            if prediction == 1:
                st.success("""
                **Your game shows strong success potential!**
                - Maintain quality standards (85%+ positive reviews)
                - Continue building community engagement
                - Monitor player feedback closely
                """)
            else:
                st.warning("""
                **Your game needs improvement:**
                """)

                if positive_ratio < 0.85:
                    st.write("❌ **Quality Issue:** Aim for 85%+ positive review ratio")
                if recommendations < 1000:
                    st.write("❌ **Community Issue:** Need more word-of-mouth (1000+ recommendations)")
                if total_reviews < 500:
                    st.write("⚠️ **Visibility Issue:** Low review count suggests limited reach")

                st.info("**Suggested Actions:** Focus on quality improvement and community building before launch")

        except Exception as e:
            st.error(f"Prediction error: {e}")

# ===== Tab 3: About =====
with tab3:
    st.header("📖 About This Project")

    st.markdown("""
    ### 🎯 Project Goal
    Predict indie game success on Steam using machine learning, combining game quality metrics 
    with streaming/marketing data.

    ### 📊 Dataset
    - **1,189 games** analyzed
    - **2 data sources:** Steam (game data) + Twitch (streaming data)
    - **17 features** including quality, pricing, engagement, and visibility metrics

    ### 🤖 Model
    - **XGBoost Classifier**
    - **97.9% accuracy** on test data
    - Trained on balanced dataset (50/50 success/failure)

    ### 🔑 Key Insights

    **Success Formula:**
    - 85%+ positive review ratio
    - 1,000+ player recommendations
    - Strong community engagement

    **The Twitch Paradox:**
    - High streaming views don't guarantee success
    - Quality gameplay > Watchability
    - Free games dominate Twitch but have lower success rates

    ### 👨‍💻 Created By
    [Nan Gao]  
    Northeastern University  
    Data Science Project - Fall 2025

    ### 📚 Technologies Used
    - Python, Pandas, Scikit-learn, XGBoost
    - Streamlit, Plotly
    - Data from Kaggle (Steam & Twitch APIs)
    """)


# Footer
st.markdown("---")
st.markdown("*Game Success Prediction System | Data Science Project 2025*")