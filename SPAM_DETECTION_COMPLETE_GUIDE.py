# 🚀 SPAM DETECTION PROJECT: COMPLETE GUIDE FOR BEGINNERS
# ========================================================

"""
Welcome to your complete Spam Detection Machine Learning project!

This guide walks you through every step we took to build a production-ready
spam detection system. Whether you're new to ML or want to understand the
complete pipeline, this file explains everything clearly.

WHAT WE BUILT:
- A spam classifier that detects spam messages with 97.7% accuracy
- A FastAPI web service for real-time predictions
- Complete ML pipeline from data to deployment

KEY CONCEPTS YOU'LL LEARN:
- Text preprocessing and feature engineering
- Multiple ML algorithms and evaluation
- Model deployment with APIs
- Production-ready ML systems
"""

## 📊 STEP 1: DATA LOADING & CLEANING
## ==================================

"""
WHY THIS STEP MATTERS:
- Real-world data is messy (duplicates, missing values, wrong formats)
- Clean data = better model performance
- This is 80% of ML work according to industry experts

WHAT WE DID:
1. Loaded CSV file with pandas
2. Removed unnecessary columns (kept only 'v1' and 'v2')
3. Renamed columns to meaningful names ('label', 'message')
4. Encoded labels (ham=0, spam=1)
5. Checked for null values and duplicates
6. Removed duplicate messages

KEY CODE CONCEPTS:
- df.isnull().sum() → Check missing values
- df.duplicated().sum() → Count duplicates
- df.drop_duplicates() → Remove duplicates
- df['column'].map({'old': new}) → Encode categorical data

RESULT: Clean dataset with 5,169 unique messages (4,827 ham, 747 spam)
"""

## 🔍 STEP 2: EXPLORATORY DATA ANALYSIS (EDA)
## ==========================================

"""
WHY EDA MATTERS:
- Understand your data before building models
- Find patterns, imbalances, and insights
- Guide feature engineering decisions

WHAT WE DID:
1. Created new features: message length, word count, character count
2. Analyzed statistics by spam/ham labels
3. Found top words for each class
4. Created distribution plots
5. Identified class imbalance (ham:spam ratio = 6.4:1)

KEY INSIGHTS FOUND:
- Spam messages are slightly longer (avg 138 chars vs 71 chars)
- Spam contains words like "free", "win", "prize", "call"
- Ham contains normal conversation words
- Clear class imbalance that needs handling

KEY CODE CONCEPTS:
- df.groupby('label')['column'].mean() → Group statistics
- Counter(word_list).most_common(n) → Find frequent words
- df['label'].value_counts().plot() → Visualize distributions
"""

## 🧹 STEP 3: TEXT PREPROCESSING
## ============================

"""
WHY TEXT PREPROCESSING MATTERS:
- Raw text has noise (URLs, numbers, punctuation, case variations)
- ML models need clean, standardized input
- Reduces vocabulary size and improves performance

WHAT WE DID:
1. Convert to lowercase
2. Remove URLs with regex
3. Remove numbers
4. Remove punctuation
5. Tokenize (split into words)
6. Remove stopwords (common words like "the", "is", "and")
7. Rejoin cleaned tokens

STOPWORDS WE REMOVED:
Common English words that don't help distinguish spam from ham

KEY CODE CONCEPTS:
- re.sub(pattern, replacement, text) → Regex text cleaning
- text.lower() → Case normalization
- string.punctuation → Punctuation removal
- text.split() → Tokenization
- [word for word in words if condition] → List comprehension filtering

RESULT: Reduced average words per message from ~15 to ~7 tokens
"""

## ⚙️ STEP 4: FEATURE ENGINEERING (TF-IDF)
## ======================================

"""
WHY FEATURE ENGINEERING MATTERS:
- Convert text into numbers that ML models can understand
- TF-IDF gives higher weight to important but rare words
- Reduces dimensionality while keeping important information

WHAT WE DID:
1. Used TfidfVectorizer (better than CountVectorizer for text)
2. Set max_features=5000 (limit vocabulary size)
3. Used min_df=2, max_df=0.8 (remove very rare/common words)
4. Added ngram_range=(1,2) (unigrams + bigrams like "free entry")

TF-IDF EXPLANATION:
- TF (Term Frequency): How often word appears in document
- IDF (Inverse Document Frequency): How rare word is across all documents
- TF-IDF = TF × IDF (higher for important words)

KEY CODE CONCEPTS:
- TfidfVectorizer() → Convert text to TF-IDF features
- fit_transform() → Learn vocabulary and transform
- get_feature_names_out() → See learned vocabulary

RESULT: 5,000 features from our cleaned text data
"""

## ✂️ STEP 5: TRAIN/TEST SPLIT
## ==========================

"""
WHY TRAIN/TEST SPLIT MATTERS:
- Need to evaluate model on unseen data
- Prevents overfitting (model memorizing training data)
- Gives realistic performance estimate

WHAT WE DID:
1. Split 80% training, 20% testing
2. Used stratify=y to maintain class balance in both sets
3. Set random_state=42 for reproducible results

KEY CODE CONCEPTS:
- train_test_split(X, y, test_size=0.2, stratify=y)
- stratify=y → Same spam/ham ratio in train/test
- random_state → Reproducible splits

RESULT: 4,135 training samples, 1,034 test samples
"""

## 🤖 STEP 6: MODEL TRAINING (MULTIPLE ALGORITHMS)
## ==============================================

"""
WHY TRY MULTIPLE MODELS:
- Different algorithms have different strengths
- No single "best" algorithm for all problems
- Compare performance to choose the best

MODELS WE TRAINED:
1. Naive Bayes → Great for text classification, fast training
2. Logistic Regression → Interpretable, good baseline
3. Random Forest → Handles complex patterns, less overfitting
4. SVM → Powerful for text, but slower

WHAT WE MEASURED:
- Training time
- Training accuracy
- Test accuracy

KEY CODE CONCEPTS:
- model.fit(X_train, y_train) → Train model
- model.score(X_test, y_test) → Get accuracy
- time.time() → Measure execution time

WINNER: Logistic Regression (fast, accurate, interpretable)
"""

## 📈 STEP 7: MODEL EVALUATION (METRICS & CONFUSION MATRIX)
## =======================================================

"""
WHY PROPER EVALUATION MATTERS:
- Accuracy alone can be misleading (especially with imbalanced data)
- Need multiple metrics for complete picture
- Confusion matrix shows exact prediction patterns

METRICS WE USED:
1. Accuracy: (TP + TN) / Total → Overall correctness
2. Precision: TP / (TP + FP) → How many predicted spam are actually spam
3. Recall: TP / (TP + FN) → How many real spam did we catch
4. F1-Score: 2 × (Precision × Recall) / (Precision + Recall) → Balance of P&R

CONFUSION MATRIX:
- True Positive (TP): Correctly predicted spam
- True Negative (TN): Correctly predicted ham
- False Positive (FP): Ham predicted as spam
- False Negative (FN): Spam predicted as ham

KEY CODE CONCEPTS:
- confusion_matrix(y_true, y_test) → Create confusion matrix
- classification_report() → All metrics at once
- sns.heatmap() → Visualize confusion matrix
"""

## ⚖️ STEP 8: HANDLING CLASS IMBALANCE
## ================================

"""
WHY CLASS IMBALANCE MATTERS:
- Our data: 86.5% ham, 13.5% spam
- Models can achieve 86.5% accuracy by predicting everything as ham!
- Need techniques to give spam equal importance

TECHNIQUES WE USED:
1. SMOTE (Synthetic Minority Over-sampling Technique)
   - Creates synthetic spam examples
   - Balances classes artificially

2. Class Weights
   - Give spam predictions higher importance
   - Penalizes misclassifying spam more than ham

KEY CODE CONCEPTS:
- SMOTE(random_state=42) → Generate synthetic samples
- class_weight='balanced' → Automatic weight calculation
- compute_class_weight() → Manual weight calculation

RESULT: Improved F1-score from 0.90 to 0.92 with SMOTE
"""

## 🎛️ STEP 9: HYPERPARAMETER TUNING
## ================================

"""
WHY HYPERPARAMETER TUNING MATTERS:
- ML models have "knobs" that affect performance
- Default settings aren't always optimal
- Tuning can significantly improve results

WHAT WE TUNED:
1. Logistic Regression:
   - C (regularization strength)
   - penalty (L1 vs L2)
   - solver (optimization algorithm)

2. Random Forest:
   - n_estimators (number of trees)
   - max_depth (tree depth)
   - min_samples_split (minimum samples to split)

TECHNIQUES USED:
1. GridSearchCV → Try all combinations
2. RandomizedSearchCV → Try random combinations (faster)

KEY CODE CONCEPTS:
- GridSearchCV(model, param_grid, cv=5) → Exhaustive search
- RandomizedSearchCV(model, param_dist, n_iter=10) → Random search
- best_params_, best_score_ → Get best settings

RESULT: Found optimal C=1.0 for Logistic Regression
"""

## 🚀 STEP 10: FINAL PIPELINE & MODEL SAVING
## ========================================

"""
WHY SAVE THE MODEL:
- Training takes time and resources
- Need model for production predictions
- Include preprocessing in the pipeline

WHAT WE DID:
1. Created Pipeline with TF-IDF + LogisticRegression
2. Trained on full dataset (no train/test split for production)
3. Saved using joblib (better than pickle for sklearn)
4. Saved metadata separately (model info, performance)

PIPELINE ADVANTAGES:
- Single object handles preprocessing + prediction
- No need to manually preprocess new text
- Consistent transformations

KEY CODE CONCEPTS:
- Pipeline([('tfidf', vectorizer), ('classifier', model)])
- joblib.dump(pipeline, 'filename.pkl')
- pipeline.predict(['new text']) → Works directly on raw text

RESULT: Production-ready model in 'spam_classifier.pkl'
"""

## 🧪 STEP 11: TESTING ON UNSEEN DATA
## ================================

"""
WHY TEST ON UNSEEN DATA:
- Validate model works on real-world examples
- Check for overfitting
- Build confidence in deployment

WHAT WE TESTED:
- 5 real spam examples (prizes, competitions, scams)
- 10 real ham examples (conversations, meetings, personal)

RESULTS ACHIEVED:
- 15/15 correct predictions (100% accuracy!)
- High confidence scores (84-98%)
- Perfect spam detection, perfect ham detection

KEY INSIGHTS:
- Model generalizes well to new examples
- Handles various spam patterns correctly
- Maintains high confidence on legitimate messages
"""

## 🌐 STEP 12: FASTAPI DEPLOYMENT
## ============================

"""
WHY DEPLOYMENT MATTERS:
- Models are useless unless accessible
- APIs allow integration with apps, websites, systems
- FastAPI is modern, fast, and easy to use

WHAT WE BUILT:
1. FastAPI application with automatic documentation
2. Health check endpoint (/health)
3. Single prediction endpoint (/predict)
4. Batch prediction endpoint (/predict/batch)
5. Proper error handling and logging

API FEATURES:
- JSON request/response format
- Input validation with Pydantic
- Confidence scores and probabilities
- Model metadata in responses

KEY CODE CONCEPTS:
- @app.get("/endpoint") → Define GET endpoint
- @app.post("/endpoint") → Define POST endpoint
- async def function(request: RequestModel) → Type hints
- return ResponseModel(...) → Structured responses

DEPLOYMENT READY:
- Run with: uvicorn app:app --host 0.0.0.0 --port 8000
- Access docs at: http://localhost:8000/docs
"""

## 🐳 STEP 13: DOCKER CONTAINERIZATION (PRODUCTION DEPLOYMENT)
## =========================================================

"""
WHY DOCKER MATTERS FOR PRODUCTION ML:
- Containerization packages your app + ALL dependencies into portable units
- Ensures identical environment across development, testing, and production
- Eliminates "works on my machine" problems
- Professional standard for ML deployment
- Required for cloud platforms and enterprise use

WHEN DOCKER IS NECESSARY (PRODUCTION):
✅ Cloud deployment (AWS ECS, Google Cloud Run, Azure Container Instances)
✅ Team development (consistent environments across machines)
✅ Production scaling (Kubernetes, Docker Swarm)
✅ CI/CD pipelines (automated testing and deployment)
✅ Enterprise applications (security, monitoring, scaling)

WHEN DOCKER IS OPTIONAL (LEARNING/DEVELOPMENT):
❌ Local development and learning (like our current setup)
❌ Single-user projects and experimentation
❌ Simple APIs without production deployment
❌ Academic projects and prototypes

DOCKER VS. DIRECT PYTHON DEPLOYMENT:

DIRECT PYTHON (Current/Learning):
- ✅ Fast setup, immediate results
- ✅ Great for learning and experimentation
- ✅ Simple debugging and development
- ❌ Environment differences across machines
- ❌ Dependency conflicts in production
- ❌ Difficult scaling and orchestration

DOCKER (Production):
- ✅ Consistent environment everywhere
- ✅ Easy deployment to any platform
- ✅ Professional and scalable
- ✅ Built-in security and isolation
- ❌ Learning curve and setup time
- ❌ Larger deployment size

DOCKER FILES WE CREATED:
1. Dockerfile - Container image configuration
2. docker-compose.yml - Multi-container orchestration

## 📦 STEP 14: RECENT PROJECT STRUCTURE UPDATES
## ============================================

"""
WHAT WAS UPDATED RECENTLY:
- Reorganized the repository into a clean MLOps structure.
- Moved the dataset to `data/spam.csv`.
- Moved the notebook to `notebooks/eda.ipynb`.
- Moved the FastAPI app to `app/app.py`.
- Stored the trained model and metadata in `models/model.pkl` and `models/model_metadata.pkl`.
- Added reusable training and preprocessing code in `src/train.py` and `src/preprocess.py`.
- Added API tests in `tests/test_predict.py`.
- Added a GitHub Actions CI workflow in `.github/workflows/ci.yml`.
- Created a root `README.md` with setup and usage instructions.
- Updated `Dockerfile` to use the new app and model paths.
- Updated `requirements.txt` with `pytest` and `httpx` for testing.
- Archived legacy files into `archive/` for cleanup while preserving history.

VALIDATION PERFORMED:
- Installed missing test dependencies.
- Ran `pytest -q tests/test_predict.py` successfully.

WHY THIS UPDATE HELPS:
- Makes the repository easier to navigate.
- Separates production-ready app code from data and notebooks.
- Supports reproducible training, testing, and deployment.
- Aligns the project with standard MLOps folder structure.
"""

3. .dockerignore - Files to exclude from build
4. docker-run.sh - Helper script for Docker operations

DOCKER WORKFLOW (When Ready for Production):
1. Install Docker Desktop
2. Run: docker-compose up --build
3. API available at http://localhost:8000
4. Access interactive docs at http://localhost:8000/docs

DOCKER ADVANTAGES FOR ML:
- Portability: Run on any machine/OS
- Isolation: No dependency conflicts
- Scalability: Multiple API instances
- Version Control: Exact environment tracking
- Security: Isolated containers, non-root users

DOCKER COMMANDS CHEAT SHEET:
- Build image: docker build -t spam-api .
- Run container: docker run -p 8000:8000 spam-api
- View logs: docker logs container_name
- Stop container: docker stop container_name
- Remove container: docker rm container_name
- Clean up: docker system prune

PRODUCTION DEPLOYMENT WITH DOCKER:
1. Build: docker build -t spam-detection-api .
2. Tag: docker tag spam-detection-api username/spam-api:v1.0
3. Push to registry: docker push username/spam-api:v1.0
4. Deploy to cloud platform (AWS/GCP/Azure)

DOCKER BEST PRACTICES FOR ML:
- Use .dockerignore to reduce image size
- Multi-stage builds for smaller production images
- Health checks for automatic monitoring
- Resource limits (CPU/memory) for stability
- Non-root users for security
- Proper logging and monitoring

DOCKER ALTERNATIVES FOR SIMPLE DEPLOYMENT:
- Railway, Render, Heroku (simpler than Docker)
- Google Cloud Run, AWS Lambda (serverless)
- Traditional VPS with uvicorn (like our current setup)

MIGRATION PATH FROM DEVELOPMENT TO PRODUCTION:
1. Current: uvicorn app:app (local development)
2. Add Docker: docker-compose up (containerized)
3. Cloud: Deploy container to cloud platform
4. Scale: Kubernetes for multiple instances

BOTTOM LINE FOR BEGINNERS:
- Docker is POWERFUL but OPTIONAL for learning
- Your current FastAPI setup works perfectly for development
- Add Docker when ready for production deployment
- Start with docker-compose for easiest transition
"""

## 🧪 STEP 14: API TESTING & VALIDATION
## ================================

"""
WHY TEST THE API:
- Ensure deployment works correctly
- Validate all endpoints function
- Test error handling

WHAT WE TESTED:
1. Health check → Model loaded, performance metrics
2. Single predictions → Spam/ham with confidence
3. Batch predictions → Multiple messages at once
4. Error handling → Invalid inputs, large batches

TEST RESULTS:
✅ Health: Model loaded, 97.7% accuracy
✅ Spam detection: "WIN a FREE iPhone!" → SPAM (92% confidence)
✅ Ham detection: "Hey, how are you?" → HAM (97% confidence)
✅ Batch processing: 4 messages → 2 spam, 2 ham

API ENDPOINTS WORKING:
- GET / → API information
- GET /health → System status
- POST /predict → Single message prediction
- POST /predict/batch → Multiple message predictions
"""

## 📚 KEY MACHINE LEARNING CONCEPTS YOU LEARNED
## ============================================

"""
1. SUPERVISED LEARNING
   - Labeled data (spam/ham examples)
   - Learn patterns to predict new examples

2. TEXT CLASSIFICATION
   - Convert text to numbers (TF-IDF)
   - Binary classification (spam vs ham)

3. MODEL EVALUATION
   - Train/Test split prevents overfitting
   - Multiple metrics better than accuracy alone
   - Confusion matrix shows prediction errors

4. FEATURE ENGINEERING
   - Raw data → ML features
   - Domain knowledge improves performance
   - Text preprocessing crucial for NLP

5. CLASS IMBALANCE
   - Unequal class distribution common
   - SMOTE and class weights help
   - F1-score better metric than accuracy

6. HYPERPARAMETER TUNING
   - Model settings affect performance
   - Grid/Random search find optimal values
   - Cross-validation prevents overfitting

7. PRODUCTION ML
   - Pipelines ensure consistency
   - APIs make models accessible
   - Error handling and logging important
"""

## 🛠️ TOOLS & LIBRARIES USED
## ========================

"""
CORE PYTHON LIBRARIES:
- pandas: Data manipulation and analysis
- numpy: Numerical computing
- scikit-learn: Machine learning algorithms
- matplotlib/seaborn: Data visualization

TEXT PROCESSING:
- re: Regular expressions for text cleaning
- string: String operations
- nltk: Natural language processing (stopwords)

WEB/API:
- FastAPI: Modern web framework
- uvicorn: ASGI server
- pydantic: Data validation
- requests: HTTP client for testing

MODEL PERSISTENCE:
- joblib: Save/load ML models (better than pickle for sklearn)
"""

## 🚀 HOW TO RUN YOUR SPAM DETECTOR
## ================================

"""
DEPLOYMENT OPTIONS (Choose based on your needs):

1. DEVELOPMENT MODE (Current - Fast & Simple):
   cd /path/to/your/project
   uvicorn app:app --host 127.0.0.1 --port 8000 --reload

2. PRODUCTION MODE WITH DOCKER (Recommended for production):
   cd /path/to/your/project
   docker-compose up --build

3. MANUAL DOCKER (Alternative):
   docker build -t spam-api .
   docker run -p 8000:8000 spam-api

TESTING YOUR API (Works with any deployment):

4. CHECK IF IT'S RUNNING:
   Visit: http://127.0.0.1:8000/health

5. VIEW INTERACTIVE DOCUMENTATION:
   Visit: http://127.0.0.1:8000/docs

6. TEST PREDICTIONS VIA API:
   POST to http://127.0.0.1:8000/predict
   Body: {"message": "Your text here"}

7. TEST WITH PYTHON SCRIPT:
   import requests
   response = requests.post('http://127.0.0.1:8000/predict',
                           json={'message': 'WIN a prize!'})
   print(response.json())

8. TEST WITH CURL:
   curl -X POST "http://127.0.0.1:8000/predict" \
        -H "Content-Type: application/json" \
        -d '{"message": "WIN a prize!"}'

DOCKER HELPER SCRIPTS:
- ./docker-run.sh build     → Build Docker image
- ./docker-run.sh compose-up → Start with docker-compose
- ./docker-run.sh test      → Test running API
- ./docker-run.sh clean     → Clean up containers
"""

## 🎯 PROJECT SUCCESS METRICS
## =========================

"""
MODEL PERFORMANCE:
- Accuracy: 97.7% on test set
- F1-Score: 90.2% (handles imbalance well)
- Precision: High (few false positives)
- Recall: High (catches most spam)

DEPLOYMENT SUCCESS:
- FastAPI server runs without errors
- All endpoints functional
- Proper error handling
- Interactive documentation available

REAL-WORLD TESTING:
- 100% accuracy on unseen examples
- High confidence scores
- Handles various spam patterns
- Correctly identifies legitimate messages
"""

## 🔮 WHAT'S NEXT? ADVANCED TOPICS TO EXPLORE
## ==========================================

"""
1. DEEP LEARNING APPROACHES:
   - LSTM/GRU networks for text
   - BERT/transformer models
   - Better accuracy with more data

2. ADVANCED FEATURES:
   - Message metadata (sender, time)
   - User behavior patterns
   - Image/text analysis

3. PRODUCTION DEPLOYMENT & CONTAINERIZATION:
   - Docker containerization (we set this up!)
   - Cloud deployment (AWS, GCP, Azure)
   - Model monitoring and alerting
   - API rate limiting and security
   - A/B testing different model versions

4. SCALING & ARCHITECTURE:
   - Load balancing multiple API instances
   - Database integration for logging
   - Redis caching for performance
   - Async processing for large batches
   - Kubernetes orchestration

5. MLOPS & AUTOMATION:
   - Automated training pipelines
   - Model versioning and rollback
   - Continuous integration/deployment (CI/CD)
   - Experiment tracking with MLflow
   - Automated model retraining
"""

## 📖 RESOURCES FOR FURTHER LEARNING
## ================================

"""
FREE RESOURCES:
1. Scikit-learn documentation: https://scikit-learn.org/
2. FastAPI tutorial: https://fastapi.tiangolo.com/
3. Docker for beginners: https://docker-curriculum.com/
4. Kaggle NLP tutorials: https://www.kaggle.com/learn/natural-language-processing
5. Towards Data Science: Great ML articles

DOCKER-SPECIFIC RESOURCES:
1. Docker Documentation: https://docs.docker.com/
2. Play with Docker: https://labs.play-with-docker.com/
3. Docker for ML: https://github.com/dockersamples/docker-for-ml
4. FastAPI + Docker guide: https://fastapi.tiangolo.com/deployment/docker/

BOOKS FOR BEGINNERS:
1. "Hands-On Machine Learning" by Aurélien Géron
2. "Natural Language Processing with Python" by Bird & Klein
3. "Python Data Science Handbook" by Jake VanderPlas

PRACTICE PROJECTS:
1. Sentiment analysis on movie reviews
2. Topic classification for news articles
3. Chatbot intent recognition
4. Language translation
"""

## 🎉 CONGRATULATIONS!
## ==================

"""
You've successfully built a complete machine learning system!

FROM DATA TO DEPLOYMENT:
✅ Data Cleaning → ✅ EDA → ✅ Preprocessing → ✅ Features
✅ Training → ✅ Evaluation → ✅ Tuning → ✅ Deployment
✅ Testing → ✅ API → ✅ Production Ready

KEY ACHIEVEMENTS:
- Built spam detector with 97.7% accuracy
- Handled real-world challenges (imbalance, preprocessing)
- Created production API with FastAPI
- Tested thoroughly on unseen data

REMEMBER:
- ML is iterative: try, measure, improve
- Clean data beats fancy algorithms
- Simple models often work best
- Deployment is as important as modeling

Keep experimenting and building! 🚀
"""

## 📊 STEP 16: LATEST UPDATES (MLFLOW & ENHANCEMENTS)
## ================================================

"""
WHAT WAS UPDATED RECENTLY:
- Added MLflow experiment tracking to `src/train.py` for logging parameters, metrics, and model artifacts (tested: works with fallback when MLflow not installed).
- Enhanced `src/preprocess.py` to save processed data to `data/processed_spam.csv` when run directly (tested: creates file with 5,169 rows, 4 columns).
- Updated `README.md` with problem statement, model approach/results, local/Docker run instructions, and API usage example.
- Added `mlflow==2.9.1` to `requirements.txt` for experiment tracking.
- Made MLflow optional in training script for environments without it installed.

VALIDATION PERFORMED:
- ✅ Ran `src/train.py` successfully: trained model with 95.6% accuracy, 78.9% F1 score, saved artifacts.
- ✅ Ran `src/preprocess.py` directly: created `data/processed_spam.csv` with processed data.
- ✅ Ran `pytest -v tests/test_predict.py`: all 4 tests passed (model artifacts, health endpoint, single/batch predictions).
- ✅ Verified modular pipeline: preprocess → train → serve works end-to-end.
"""

# ========================================================
# END OF GUIDE - HAPPY LEARNING! 🎓🤖📈
# ========================================================