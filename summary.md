# Game Success Prediction

## 1. PROBLEM

Independent game developers invest significant time and resources into game development, but only a small percentage achieve commercial success. This project aims to predict whether an indie game will succeed on Steam based on early indicators.

**Research Question:** Can we predict game success using game features and community data?

**Success Definition:** Games with ≥85% positive reviews AND (≥1000 recommendations OR ≥100k owners)

---

## 2. DATA

**Two Independent Sources:**

- **Steam Games Dataset** (Kaggle - 111,452 games)
  - Game metadata, pricing, reviews, player behavior
  - Source: Steam Web API

- **Twitch Game Data** (Kaggle - 21,000 records, 2016)
  - Streaming metrics, viewership, streamer counts
  - Source: Twitch API

**Data Integration:** Merged by game name → 1,189 games matched

**Final Dataset:** 1,189 games × 17 features
  - Steam features: 10 (quality, pricing, engagement)
  - Twitch features: 5 (marketing, visibility)
  - Engineered features: 2 (combined metrics)

---

## 3. MODEL

**Models Trained:**
1. Decision Tree (baseline)
2. Random Forest (required)
3. Naive Bayes (comparison)
4. XGBoost (bonus)

**Best Model:** XGBoost
  - Test Accuracy: 97.9%
  - F1-Score: 0.979
  - AUC: 0.995

**Why XGBoost?**
  - Handles feature interactions
  - Robust to outliers
  - Best performance across all metrics

---

## 4. RESULTS

**Model Performance:**
  - 97.9% accuracy on test set
  - Only 5 errors out of 238 predictions
  - Balanced performance (FP: 2, FN: 3)

**Key Findings:**

1. **Top Success Factors:**
   - Player satisfaction (positive_ratio): Most important
   - Word-of-mouth (Recommendations): Critical threshold
   - Community engagement: Strong predictor

2. **The Twitch Paradox:** 
   - High Twitch views correlate NEGATIVELY with success
   - Free games dominate Twitch but only 19.5% succeed vs 54.1% paid games
   - "Watchability" ≠ "Playability"

3. **Success Pattern:**
   - Quality > Marketing
   - 85%+ positive reviews essential
   - 1000+ recommendations needed
   - Pricing: Successful games avg $22, failures avg similar

---

## 5. LIMITATIONS

**Data Constraints:**
  • Time mismatch: Twitch data from 2016, Steam data more recent
  • Platform: Only Steam, excludes console/mobile
  • Sample bias: Only games with both Steam and Twitch presence

**Model Constraints:**
  • Success definition is binary (doesn't capture degrees of success)
  • Missing factors: Marketing budget, team size, release timing
  • Cannot predict "lightning in a bottle" viral successes

**Generalization:**
  • Model trained on 2016-era games
  • Gaming market evolves rapidly
  • May not apply to emerging genres

---

## 6. NEXT STEPS

**Improvements:**
  1. Add more recent Twitch data (2023-2024)
  2. Include developer reputation as a feature
  3. Incorporate release timing (seasonality)
  4. Add genre-specific models
  5. Real-time prediction API for developers
  
**Practical Application:**
  1. Web app for indie developers to test game concepts
  2. Investment decision tool for publishers
  3. Market analysis dashboard for platform holders

---

**Project by:** [Nan Gao] | Northeastern University | December 2025
**Repository:** [https://github.com/77652189/GameSuccessPrediction]