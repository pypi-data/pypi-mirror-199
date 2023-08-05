# Aesplot
Aesthetic for Matplotlib and Python Framework for data analysis

# Aesthetics
To use only the aesthetics and not the framework simply use
```python
import aesplot

#before any plot use
PlotLikeR().plot_cfg()        ##This will set your plt.rcParams by
PlotLikeR().plot_cfg_grid()   ##using plt.rcParams.update()

#you can further update the params if you dislike some
plt.rcParams.update({
  'font.family': 'serif',
  'font.serif': 'DejaVu Serif',
  'mathtext.fontset': 'dejavuserif',
  'font.size':18,
  'axes.labelsize': 26,
  'axes.grid': True,
  'axes.facecolor':'#EBEBEB',
  'text.usetex': True,
  'text.latex.preamble': '\\usepackage{amsmath}\n \\usepackage[dvipsnames]{xcolor}'
})
```
In the matplotlib documentation it is possible to find a description of each individual parameter. The majority of which, in the Aesplot library, are set as the default. For more check [this link](https://matplotlib.org/stable/tutorials/introductory/customizing.html#the-default-matplotlibrc-file).


# Framework
Use a separate python file to create the basic framework structure
```python
from aesplot import Framework

#Use this below to get a new frame file
Framework.create_framework_file(path='./',
                file_name='basic_framework.py')

#Or use this to get the string equivalent
frame_string = grab_basic_framework()
print(frame_string)
```
Modify the new file or string to make your analysis.

# Utils
### Fixing the SVG export from matplotlib
When saving the matplotlib figure as SVG, the syntax used doesn't contain any &lt;text&gt;&lt;/text&gt;. Instead, matplotlib opts for creating there own letters as mathematical curves. This can be an issue due to the "low resolution" aspect of these curves. To solve this, an utility tool was developed to find and replace the curves for letters.

Additionally, when using LaTex equations in labels and/or legends, some elements can also be converted into HTML syntax.

### Converting LaTex to HTML
Some mathematical notation is usually used when plotting graphs such as square root, superscript, index and many others. And, since matplotlib supports LaTex interpretation/compilation, it is useful to have a translation from one markup language to another.

Using utils.SVGText() allows the transformation from:

| | | | |
| --- | --- | --- | --- |
| \\text{} | \\textit{} | \\textb{} | \\left |
| \\right | \\sqrt | \\sqrt[3] | \\sqrt[4] |
| ^ | ^{} | _ | _{} |

into the equivalent &lt;tspan&gt;&lt;/tspan&gt; around the tag. More LaTex markups will be added in the future

# Dependencies
  - [Numpy](https://numpy.org)
  - [Matplotlib](https://matplotlib.org)
  - [Pandas](https://pandas.pydata.org)
  - [Scipy](https://scipy.org)
  - [Miktex](https://miktex.org) or other latex compiler

# To-dos
  - Expand the latex functions that can be interpreted and translated
  - Develop tests
  - Create data examples and plot examples
