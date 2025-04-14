# Visualization generator Web Application

This project demonstrates a web application that dynamically executes visualization code written in Python or R and displays the result. The backend is built with Flask, and the application supports:

- **Static Visualizations:** Created using Matplotlib (Python) or ggplot2 (R)
- **Interactive Visualizations:** Created using Plotly (both Python and R)
- **3D Visualizations:** Created using Plotly (both Python and R)

**Important:**  
When writing your code, only provide the output filename (e.g., "test.png" or "interactive.html"). Do not include a folder directory (such as "static/test.png") because the application automatically saves files in the static folder.

---

## Installation

### Python

1. **Install Python 3.x.**

2. **Create and Activate a Virtual Environment:**
```
   On Windows (using PowerShell):

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
```

3. **Install Required Python and R Packages:**

Python
```
pip install flask flask-cors matplotlib plotly
```


R
Install R:

Download and install R from CRAN.

Install Required R Packages:

Open the R console (or RStudio) and run:

```
install.packages("ggplot2", repos="http://cran.rstudio.com")
install.packages("plotly", repos="http://cran.rstudio.com")
install.packages("htmlwidgets", repos="http://cran.rstudio.com")
```

Install Pandoc:

If you do not have RStudio installed or Pandoc bundled, download Pandoc from Pandoc’s official site.

Install it and add its folder (e.g., C:\Program Files\Pandoc) to your system PATH.


Running the Application
Start the Flask Backend:

In your project root, run:
```
python app.py
The backend will start (typically on http://localhost:5000).
(Make sure the virtual environment for Python is activated.)
```

Access the Frontend:

```
cd frontend
npm install
npm start
```

Sample Code
Python Samples
1. Static Visualization Using Matplotlib
python
Copy
import matplotlib.pyplot as plt
plt.figure()
plt.bar([1, 2, 3], [4, 5, 6])
plt.title("Bar Chart")
plt.savefig("test.png")
2. Interactive Visualization Using Plotly
python
Copy
import os
import plotly.express as px
import plotly.offline as pyo

df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", 
                 title="Interactive Iris Scatter Plot")
# Save the interactive visualization as an HTML file
pyo.plot(fig, filename="interactive.html", auto_open=False)
3. 3D Visualization Using Plotly
python
Copy
import os
import plotly.express as px
import plotly.offline as pyo

df = px.data.iris()
fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_length', 
                    color='species', title="3D Iris Scatter Plot")
# Save the 3D interactive visualization as an HTML file
pyo.plot(fig, filename="3d_scatter.html", auto_open=False)
R Samples
1. Static Visualization Using ggplot2
r
Copy
# Static sample using ggplot2
library(ggplot2)
data(iris)
p <- ggplot(iris, aes(x = Sepal.Width, y = Sepal.Length, fill = Species)) +
     geom_bar(stat = "identity", position = "dodge") +
     ggtitle("Static Bar Chart")
# Save the plot using the provided filename (only provide the filename)
ggsave(filename = "static_bar_chart.png", plot = p, width = 6, height = 4)
2. Interactive Visualization Using Plotly
r
Copy
# Interactive sample using Plotly
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
# Save the interactive plot as an HTML file (only provide the filename)
saveWidget(as_widget(p), file = "interactive_scatter.html")
3. 3D Visualization Using Plotly
r
Copy
# 3D sample using Plotly
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
# Save the 3D interactive plot as an HTML file (only provide the filename)
saveWidget(as_widget(p), file = "interactive_3d_scatter.html")
Important Notes
Filenames Only:
When saving visualizations (using plt.savefig in Python or ggsave / saveWidget in R), supply only the filename (e.g., "test.png", "interactive.html"). Do not include a folder path. The application automatically saves files in the static folder.

Output Folder:
All generated visualization files are stored in the static folder (located in the project root).

Environment Variables:
Ensure that if any changes are made to environment variables (e.g., adding Pandoc to PATH), you restart your application or terminal so the changes are effective.