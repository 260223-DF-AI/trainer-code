# matplotlib

## Learning Objectives

- Create basic plots with matplotlib
- Customize plot appearance
- Create different chart types
- Save plots to files

## Why This Matters

Data visualization is essential for understanding and communicating insights from data. matplotlib is Python's foundational plotting library - most other visualization tools build on it. Being able to create clear, informative charts is a key skill for data analysis and reporting.

## Concept

### What Is matplotlib?

matplotlib is Python's primary plotting library. It creates:

- Line plots
- Bar charts
- Scatter plots
- Histograms
- Pie charts
- And many more

### Installing matplotlib

```bash
pip install matplotlib
```

### Basic Line Plot

```python
import matplotlib.pyplot as plt

# Data
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# Create plot
plt.plot(x, y)

# Display
plt.show()
```

### Adding Labels and Title

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.plot(x, y)
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
plt.title("My First Plot")
plt.show()
```

### Customizing Lines

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# Color, style, marker
plt.plot(x, y, color="red", linestyle="--", marker="o")
plt.show()

# Shorthand notation: 'color marker linestyle'
plt.plot(x, y, "r--o")  # red, dashed, circles
```

### Multiple Lines

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y1 = [2, 4, 6, 8, 10]
y2 = [1, 3, 5, 7, 9]

plt.plot(x, y1, label="Line 1")
plt.plot(x, y2, label="Line 2")
plt.legend()
plt.show()
```

### Bar Charts

```python
import matplotlib.pyplot as plt

categories = ["A", "B", "C", "D"]
values = [25, 40, 30, 55]

plt.bar(categories, values)
plt.xlabel("Category")
plt.ylabel("Value")
plt.title("Bar Chart Example")
plt.show()
```

**Horizontal bars:**

```python
plt.barh(categories, values)
```

### Scatter Plots

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.random.rand(50)
y = np.random.rand(50)
sizes = np.random.rand(50) * 100
colors = np.random.rand(50)

plt.scatter(x, y, s=sizes, c=colors, alpha=0.5)
plt.colorbar()
plt.show()
```

### Histograms

```python
import matplotlib.pyplot as plt
import numpy as np

data = np.random.randn(1000)  # Normal distribution

plt.hist(data, bins=30, edgecolor="black")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.title("Histogram")
plt.show()
```

### Pie Charts

```python
import matplotlib.pyplot as plt

sizes = [30, 25, 20, 15, 10]
labels = ["Category A", "Category B", "Category C", "Category D", "Category E"]

plt.pie(sizes, labels=labels, autopct="%1.1f%%")
plt.title("Pie Chart Example")
plt.show()
```

### Subplots

Create multiple plots in one figure:

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# Top left
axes[0, 0].plot([1, 2, 3], [1, 4, 9])
axes[0, 0].set_title("Line Plot")

# Top right
axes[0, 1].bar(["A", "B", "C"], [3, 7, 5])
axes[0, 1].set_title("Bar Chart")

# Bottom left
axes[1, 0].scatter([1, 2, 3], [1, 4, 2])
axes[1, 0].set_title("Scatter Plot")

# Bottom right
axes[1, 1].hist([1, 2, 2, 3, 3, 3, 4, 4, 5])
axes[1, 1].set_title("Histogram")

plt.tight_layout()
plt.show()
```

### Saving Plots

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.plot(x, y)
plt.title("My Plot")

# Save to file
plt.savefig("my_plot.png")
plt.savefig("my_plot.pdf")  # Vector format
plt.savefig("my_plot.png", dpi=300)  # High resolution
```

### Styling

```python
import matplotlib.pyplot as plt

# Use a built-in style
plt.style.use("seaborn")
# Other options: 'ggplot', 'dark_background', 'bmh', etc.

# See available styles
print(plt.style.available)
```

### Practical Example

```python
import matplotlib.pyplot as plt
import numpy as np

# Sales data
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
product_a = [120, 150, 170, 160, 180, 200]
product_b = [90, 110, 100, 130, 140, 150]

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Line plot
ax1.plot(months, product_a, marker="o", label="Product A")
ax1.plot(months, product_b, marker="s", label="Product B")
ax1.set_xlabel("Month")
ax1.set_ylabel("Sales")
ax1.set_title("Monthly Sales Trend")
ax1.legend()
ax1.grid(True, alpha=0.3)

# Bar chart comparison
x = np.arange(len(months))
width = 0.35
ax2.bar(x - width/2, product_a, width, label="Product A")
ax2.bar(x + width/2, product_b, width, label="Product B")
ax2.set_xlabel("Month")
ax2.set_ylabel("Sales")
ax2.set_title("Sales Comparison")
ax2.set_xticks(x)
ax2.set_xticklabels(months)
ax2.legend()

plt.tight_layout()
plt.savefig("sales_report.png", dpi=150)
plt.show()
```

## Summary

matplotlib creates visualizations from data. Import with `import matplotlib.pyplot as plt`. Create plots with `plt.plot()`, `plt.bar()`, `plt.scatter()`, `plt.hist()`, etc. Add labels with `xlabel()`, `ylabel()`, `title()`. Use `legend()` for multiple series. Create multiple plots with `subplots()`. Save with `savefig()`. Apply styles with `plt.style.use()`. matplotlib is the foundation for more advanced visualization libraries.

## Resources

- [matplotlib Documentation](https://matplotlib.org/stable/index.html)
- [matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [Real Python: matplotlib Guide](https://realpython.com/python-matplotlib-guide/)
