# Book Recommendations

![](images/alfons-morales-YLSwjSy7stw-unsplash-crop1.jpg)

The goal of this project is to build a recommender system that suggests relevant books based on the person's interests.

The Streamlit app takes a user ID as input and displays a list of 10 recommended books.

## Dataset

I used the [goodbooks-10k](https://github.com/zygmuntz/goodbooks-10k) dataset created by Zygmunt Zając.
        
Data includes: 
- 10,000 books (different editions of the book have the same book ID)
- 53,424 users
- 6M ratings (ratings are whole numbers from 1 to 5)

## Approach

1. Data Exploration
2. Modeling - collaborative filtering using [Surprise](http://surpriselib.com/) library
    - Compare different Surprise algorithms on the training set (cross-validation)
    - Evaluate shortlisted models on the test set and choose the final model
3. Create and deploy a Streamlit app that recommends 10 books for the user

## Models

1. [**Normal Predictor**](https://surprise.readthedocs.io/en/stable/basic_algorithms.html#surprise.prediction_algorithms.random_pred.NormalPredictor) (random predictions based on rating distribution) - as a baseline model
    - Test MAE = **1.05**

2. [**SVD++**](https://surprise.readthedocs.io/en/stable/matrix_factorization.html#surprise.prediction_algorithms.matrix_factorization.SVDpp) - chosen as a final model
    - Test MAE = **0.63**
    - The Mean Absolute Error on the test set has been reduced by 40% compared to the Normal Predictor (from 1.05 to 0.63)
    - On average, the rating predictions by SVD++ model are off by 16% (mean rating = 3.92)

#### The SVD++ model is used in the app (streamlit_app.py) to predict unknown ratings for the user. Then the books with the highest predicted ratings are included in the recommendation list.
