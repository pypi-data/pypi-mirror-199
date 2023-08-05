from correlation_functions import weighted_pearson, weighted_cramer
from fc_means import symbolized_var
import numpy as np
import pandas as pd

def correlation_matrix(data, types, weights = None):
    """ Generate weighted correlation matrix for a given dataframe.

    :param data: data set
    :type data: Pandas Dataframe
    :param types: attribute types (including outcome class)
    :type types: Numpy array
    :param weights: instance weights
    :type weights: Numpy array
    :return: correlation matrix
    :rtype: Pandas Dataframe
    """

    # if weights is not specified, set weights to 1 for all instances
    if weights is None:
        weights = np.ones(len(data))

    # attributes in data
    attributes = data.columns

    # Remove outcome class
    X = data.iloc[:,:-1]
    

    # Create dataset with symbolic values for numerical features
    if "nominal" in types[:-1]:

        symb_X = X.copy()
        for col in range(len(types)):
            if types[col] == "numeric":
                
                symb_X[symb_X.columns[col]] = symbolized_var(X, X.columns[col])


    
    # Initiate array to store correlations
    correlation_matrix = np.zeros(shape=[len(attributes)-1, len(attributes)-1])

    # Loop over all attributes and calculate correlation for every combination
    for x in range(len(attributes)-1):
        correlation_matrix[x,x] = 1
        for y in range(len(attributes)-1):
            if x != y and y > x:
                if types[x] == "numeric" and types[y] == "numeric":
                    # Pearson if both attributes are numerical
                    correlation_matrix[x,y] = correlation_matrix[y,x] = weighted_pearson(X, attributes[x], attributes[y], weights)
                elif types[x] == "nominal" and types[y] == "nominal":
                    # Crámer's V if both attributes are nominal
                    correlation_matrix[x,y] = correlation_matrix[y,x] = weighted_cramer(X, attributes[x], attributes[y], weights)

                elif types[x] == "numeric" and types[y] == "nominal":
                    # Crámer's V with numerical feature transformed into nominal
                    correlation_matrix[x,y] = correlation_matrix[y,x] = weighted_cramer(symb_X, attributes[y], attributes[x], weights)

                elif types[x] == "nominal" and types[y] == "numeric":
                    # Same as previous condition, with reversed attribute type order
                    correlation_matrix[x,y] = correlation_matrix[y,x] = weighted_cramer(symb_X, attributes[x], attributes[y], weights)

    correlation_matrix =  np.abs(correlation_matrix)

    correlation_matrix = pd.DataFrame(correlation_matrix, columns = attributes[:-1], index = attributes[:-1])

    correlation_matrix.to_csv("correlation_matrix.csv", index=False)

    return correlation_matrix



