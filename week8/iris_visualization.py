import pandas as pd  # Ensure pandas is imported
import seaborn as sns
import matplotlib
matplotlib.use('TkAgg')  # Set the matplotlib backend to 'TkAgg'
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

# Load the iris dataset
iris = load_iris()
iris_data = iris.data
iris_labels = iris.target
iris_feature_names = iris.feature_names

# Create a DataFrame from the Iris dataset
iris_df = pd.DataFrame(data=iris_data, columns=iris_feature_names)
iris_df['Species'] = iris_labels

# Set the Seaborn style
sns.set(style="whitegrid")

# Create a pairplot of the Iris dataset
sns.pairplot(iris_df, hue="Species", markers=["o", "s", "D"])
plt.suptitle("Pairplot of Iris Dataset", y=1.02)
plt.show()

# Create a boxplot of Sepal Length by Species
plt.figure(figsize=(10, 6))
sns.boxplot(x="Species", y="sepal length (cm)", data=iris_df)
plt.title("Boxplot of Sepal Length by Species")
plt.show()

# Create a histogram of Petal Length by Species
plt.figure(figsize=(10, 6))
sns.histplot(iris_df, x="petal length (cm)", hue="Species",
             element="step", stat="density", common_norm=False)
plt.title("Histogram of Petal Length by Species")
plt.show()