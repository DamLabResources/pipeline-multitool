# Quick and dirty hyperparam opt, no preprocessing needed
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import nni

if __name__ == '__main__':
    
    SEED = 255

    X, y = load_diabetes(return_X_y=True, as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2, random_state = SEED)

    PARAMS = nni.get_next_parameter()
    rf = RandomForestRegressor(random_state = SEED, **PARAMS)

    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)

    nni.report_final_result(mse)