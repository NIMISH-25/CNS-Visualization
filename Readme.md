# Visualization generator Web Application

This project demonstrates a web application that dynamically executes visualization code written in Python or R and displays the resulting chart or graph. The application is designed to support a mix of static, interactive, and 3D visualizations using a couple of popular libraries in each language.

## Overview
The application is split into two main parts:

## Frontend:
Developed with React, it provides:

A dropdown menu to select the scripting language (Python or R)

A text area where users can write or paste their visualization code

A "Generate" button that submits the code to the backend

An embedded component (iframe or similar) to display the generated visualization

## Backend:
Built with Flask (Python), it:

Exposes an API endpoint that accepts a JSON payload containing the user code and selected language

Executes the submitted code in a secure, isolated environment (ensuring only designated libraries are used)

Saves the generated visualizations in a dedicated output (static) folder and serves them via a public URL or directly returns the content to be embedded

## Supported Visualization Types and Libraries
### Static Visualizations:

1) Python: Matplotlib

2) R: ggplot2

### Interactive Visualizations:

1) Python: Plotly

2) R: Plotly

### 3D Visualizations:

1) Python: Plotly

2) R: Plotly

***Important:
When writing your code scripts, only supply the output filename (e.g., "test.png", "interactive.html"). Do not include folder directories (such as "static/test.png") since the application automatically saves files in the static folder.***

## Installation
1. Clone the Repository
Clone the project repository and navigate to the project root:

```
git clone https://github.com/NIMISH-25/CNS-Visualization
```

2. Backend Setup (Flask + R)
***Python Setup***
Navigate to the backend folder:

```
cd backend
```

Ensure Python 3.x is installed.
Create and activate a virtual environment:
On Windows (using PowerShell):

```
python -m venv venv
.\venv\Scripts\Activate
```

Install the required Python packages:

```
pip install flask flask-cors matplotlib plotly pandas
```

***R Setup***
Download and install R from CRAN: https://cran.r-project.org

Install the required R packages:

Open the R console (or RStudio) and run:

```
install.packages("ggplot2", repos="http://cran.rstudio.com")
install.packages("plotly", repos="http://cran.rstudio.com")
install.packages("htmlwidgets", repos="http://cran.rstudio.com")
Install Pandoc:

If you do not have RStudio (which bundles Pandoc), download Pandoc from the official site: https://pandoc.org/ and add its folder (e.g., C:\Program Files\Pandoc) to your system PATH.
```

3. Frontend Setup
Navigate to the frontend folder from the project root:

```
cd frontend
```

Install the frontend dependencies:

```
npm install
```

## Running the Application
Start the Backend
In your project root, ensure the virtual environment is active.

Run the Flask application:

```
python app.py
```
The backend service should start (typically accessible at http://localhost:5000).

Start the Frontend
Navigate to the frontend directory:

```
npm start
```
The frontend will launch in your web browser, allowing you to input code, select your scripting language, and see the visualizations rendered dynamically.

## Sample Testing Codes
### Python Samples
***Static Visualization Using Matplotlib:***

```
import matplotlib.pyplot as plt
plt.figure()
plt.bar([1, 2, 3], [4, 5, 6])
plt.title("Bar Chart")
plt.savefig("test.png")
```

***Interactive Visualization Using Plotly:***

```
import plotly.express as px
import plotly.offline as pyo

df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", 
                 title="Interactive Iris Scatter Plot")
# Save the interactive visualization as an HTML file
pyo.plot(fig, filename="interactive.html", auto_open=False)
```

***3D Visualization Using Plotly:***

```
import plotly.express as px
import plotly.offline as pyo

df = px.data.iris()
fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_length', 
                    color='species', title="3D Iris Scatter Plot")
# Save the 3D interactive visualization as an HTML file
pyo.plot(fig, filename="3d_scatter.html", auto_open=False)
```

### R Samples
***Static Visualization Using ggplot2:***

```
library(ggplot2)
data(iris)
p <- ggplot(iris, aes(x = Sepal.Width, y = Sepal.Length, fill = Species)) +
     geom_bar(stat = "identity", position = "dodge") +
     ggtitle("Static Bar Chart")
ggsave(filename = "static_bar_chart.png", plot = p, width = 6, height = 4)
```

***Interactive Visualization Using Plotly:***

```
library(plotly)
library(htmlwidgets)
data(iris)
p <- plot_ly(data = iris, 
             x = ~Sepal.Width, 
             y = ~Sepal.Length, 
             color = ~Species,
             type = 'scatter', 
             mode = 'markers') %>% 
     layout(title = "Interactive Scatter Plot")
saveWidget(as_widget(p), file = "interactive_scatter.html")
```

***3D Visualization Using Plotly:***

```
library(plotly)
library(htmlwidgets)
data(iris)
p <- plot_ly(data = iris, 
             x = ~Sepal.Length, 
             y = ~Sepal.Width, 
             z = ~Petal.Length,
             color = ~Species, 
             type = 'scatter3d', 
             mode = 'markers') %>% 
     layout(title = "3D Scatter Plot")
saveWidget(as_widget(p), file = "interactive_3d_scatter.html")
```

## Additional Notes
1) Filename Restrictions:
When saving visualizations (using methods like plt.savefig in Python or ggsave/saveWidget in R), supply only the filename (e.g., "test.png", "interactive.html"). Do not include directory paths—the application automatically saves files in the static folder.

2) Output Folder:
All generated visualization files are stored in the static folder located in the project root.

3) Environment Variables:
If any environment variables are changed (e.g., adding Pandoc to your PATH), make sure to restart your application or terminal session to apply the changes.

### Recording
https://www.loom.com/share/66f2a54823b4462da3936c7cd5532a75?sid=0aca0a78-95d6-4b2f-ae10-28579db5ef2a