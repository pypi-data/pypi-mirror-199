# Patatas 

[https://pypi.org/project/patatas/](https://pypi.org/project/patatas/)


Patatas is a Python package that provides tools for preprocessing and modeling data using machine learning algorithms.

## Installation

You can install Patatas using pip:

pip install patatas


## Installation

### Usage
Encoding categorical columns
To encode all categorical (object) columns of a pandas DataFrame using Label Encoding, you can use the fritas() function:
```bash

from patatas import fritas
import pandas as pd

# Create a sample DataFrame with categorical columns
df = pd.DataFrame({'Color': ['Red', 'Green', 'Blue'], 'Size': ['Small', 'Medium', 'Large']})

# Encode categorical columns using Label Encoding
df_encoded = fritas(df)

# Show the encoded DataFrame
print(df_encoded)
```


Finding the best value of k for K-NN regression
To find the best value of k (number of neighbors) for K-NN regression based on the mean squared error, you can use the bravas() function:


```bash
from patatas import bravas
import pandas as pd

# Load a sample dataset
df = pd.read_csv('my_dataset.csv')

# Find the best value of k for K-NN regression
best_k = bravas(df, 'target_column')
print(f'The best value of k is {best_k}')
Contributing
Contributions to Patata Poderosa are welcome! To contribute, please follow these steps:
```

Fork the repository and create a new branch for your feature or bug fix.
Write tests for your changes.
Implement your feature or bug fix.
Run the tests and ensure they pass.
Submit a pull request.
License
Patatas is released under the MIT License. See the LICENSE file for more details.

