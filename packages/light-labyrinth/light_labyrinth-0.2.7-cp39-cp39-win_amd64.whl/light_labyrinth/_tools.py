import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder


class _SmartOneHotEncoder:
    """Standard One-Hot Encoder, but it allows to transform 1D arrays without reshaping.
    Example:
    [1,2,1,1,2] -> [[1,0], [0,1], [1,0], [1,0], [0,1]]
    """
    def __init__(self):
        self._encoder = OneHotEncoder()

    def fit(self, X):
        self._org_shape = [-1, *X.shape[1:]]
        return self._encoder.fit(X.reshape((-1, 1)))

    def transform(self, X):
        return self._encoder.transform(X.reshape((-1, 1))).todense()

    def fit_transform(self, X):
        self._org_shape = [-1, *X.shape[1:]]
        return self._encoder.fit_transform(X.reshape((-1, 1))).todense()

    def inverse_transform(self, X):
        return self._encoder.inverse_transform(X).reshape(self._org_shape)

    def get_classes(self):
        return self._encoder.categories_[0]


class _LightLabyrinthOutputTransformer:
    """Transforms any array into output intensities for n-level (n >= 1) Light Labyrinth
    with 2 outputs on each level. Used for regression as well as multi-label classification.
    """
    def __init__(self, depth=None):
        self._depth = depth

    def fit(self, X):
        # by default labyrinth's depth is given by the number of features (columns)
        if self._depth is None:
            self._depth = X.shape[1]

        # fit min-max scaler
        self._scaler = MinMaxScaler((0, 1/self._depth)).fit(X)
        return self

    def transform(self, X):
        # by default labyrinth's depth is given by the number of features (columns)
        n_columns = X.shape[1]
        if self._depth is None:
            self._depth = n_columns

        # transform X using min-max scaler (now each feature is scaled to [0 - 1/depth])
        transformed = self._scaler.transform(X)

        # sum of both outputs on each level should add up to 1/depth
        rest = 1/self._depth - transformed

        # create output order (pairs of outputs on each level should be next to each other) 
        output_order = sum([[i, i + n_columns] for i in range(n_columns)], [])

        # combine positive and negative outputs and reorder them
        prepared = np.hstack((transformed, rest))[:, output_order]
        return prepared

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)

    def inverse_transform(self, X):
        # calculate sum of pairs of outputs on every level
        denominator = X[:, 0::2] + X[:, 1::2]

        # if a given pair adds up to 0, set the denominator to 1 (for numerical safety)
        zero_indices = denominator == 0
        denominator[zero_indices] = 1

        # take the relevant (positive) output probability of each pair
        nominator = X[:, 0::2]

        # set output probability of omitted outputs to 0.5
        nominator[zero_indices] = 0.5

        # compute the ratio
        positive_ratio = nominator / denominator

        # scale outputs back to the original domain
        positive_ratio /= self._depth
        inverse_transformed = self._scaler.inverse_transform(positive_ratio)
        return inverse_transformed


class  _MixedOutputTransformer:
    """Used to prepare output for MixedOutputLightLabyrinth
    """
    def __init__(self, cat_col_names, num_col_names, depth=None):
        self._cat_col_names = cat_col_names
        self._num_col_names = num_col_names
        self._depth = depth

    @property
    def depth(self):
        return self._depth

    def fit(self, X):
        # create lists of numerical nad categorical columns
        cat_cols = [X[i].astype("category") for i in self._cat_col_names]
        num_cols = [X[i] for i in self._num_col_names]

        # calculate depth of the labyrinth and create global min-max scaler
        self._depth = len(num_cols) + sum(len(i.cat.categories) for i in cat_cols)
        self._global_scaler = MinMaxScaler((0, 1/self._depth))

        # prepare mappings holding information which output belongs to which target column
        self._cat_mappings = {col.name: dict(enumerate(col.cat.categories)) for col in cat_cols}
        self._num_mappings = {i: col.name for i, col in enumerate(num_cols)}

        # fit LightLabyrinthOutputTransformer to transform numerical columns into a matrix
        # where each pair of columns (even and odd) adds up to column of ones
        self._num_scaler = _LightLabyrinthOutputTransformer(depth=1).fit(X[self._num_col_names].to_numpy())

        return self
    
    def transform(self, X):
        # transform numerical columns (if there are any)
        if self._num_col_names:
            np_num_cols = X[self._num_col_names].to_numpy()
            np_num_transformed_cols = self._num_scaler.transform(np_num_cols)

        # one-hot encode and transform categorical columns (if there are any)
        if self._cat_col_names:
            np_cat_cols = np.hstack([X[i].astype('category').cat.codes for i in self._cat_col_names]).reshape((len(self._cat_col_names), -1)).T
            np_cat_encoded_cols = np.asarray(np.hstack([_SmartOneHotEncoder().fit_transform(col) for col in np_cat_cols.T]))
            np_cat_transformed_cols = _LightLabyrinthOutputTransformer(depth=1).fit_transform(np_cat_encoded_cols)

        # merge numerical and categorical columns
        if self._num_col_names and self._cat_col_names:
            merged = np.hstack((np_num_transformed_cols, np_cat_transformed_cols))
        elif self._num_col_names:
            merged = np_num_transformed_cols
        elif self._cat_col_names:
            merged = np_cat_transformed_cols
        else:
            raise RuntimeError("X is empty")

        # min-max scale merged columns to range [0 - 1/depth]
        return self._global_scaler.fit_transform(np.asarray(merged))

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)

    def inverse_transform(self, X):
        # scale back the matrix to the original domain
        inverse_transformed = self._global_scaler.inverse_transform(X)

        # select numerical part of the matrix (columns from 0 to 2*len(self._num_col_names))
        # and inverse transform it to the original domain
        num_part = self._num_scaler.inverse_transform(inverse_transformed[:, 0:2*len(self._num_col_names)])

        # assign numerical column values to the original column names
        df = pd.DataFrame()
        for i,name in self._num_mappings.items():
            df[name] = num_part[:,i]

        # find offset where the categorical columns start
        start_offset = len(self._num_mappings)
        offset = 2*start_offset

        # for each original categorical column
        for name, inverse_mapping in self._cat_mappings.items():
            # check how many categories it has (how many labyrinth levels 
            # were responsible for this multi-class target)
            cat_length = len(inverse_mapping)

            # find positive values for each category (the even ones)
            nominators = X[:, offset:offset+2*cat_length:2]
            # find sum of intensities for each category (odd + even)
            denominators = nominators + X[:, offset+1:offset+2*cat_length:2]
            # calculate the ratio
            proportions = nominators/denominators
            # selected category is the one with the highest positive to negative ratio
            codes = proportions.argmax(axis=1)
            # assign selected category to the original target column
            df[name] = [inverse_mapping[i] for i in codes]

            # move the offset
            offset += 2*cat_length

        return df

        