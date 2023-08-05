'''
# Aesplot
Aesthetic for Matplotlib and Python Framework for data analysis

# Aesthetics
To use only the aesthetics and not the framework simply use create a class instance and call for PlotLikeR().plot_cfg() and/or PlotLikeR().plot_cfg_grid() methods.
In the matplotlib documentation it is possible to find a description of each individual parameter. The majority of which, in the Aesplot library, are set as the default. For more check [this link](https://matplotlib.org/stable/tutorials/introductory/customizing.html#the-default-matplotlibrc-file).

# Framework
Use a separate python file to create the basic framework structure.
Modify the new file or string to make your analysis.

# Utils
### Fixing the SVG export from matplotlib
When saving the matplotlib figure as SVG, the syntax used doesn't contain any &lt;text&gt;&lt;/text&gt;. Instead, matplotlib opts for creating there own letters as mathematical curves. This can be an issue due to the "low resolution" aspect of these curves. To solve this, an utility tool was developed to find and replace the curves for letters.

Additionally, when using LaTex equations in labels and/or legends, some elements can also be converted into HTML syntax.

### Converting LaTex to HTML
Some mathematical notation is usually used when plotting graphs such as square root, superscript, index and many others. And, since matplotlib supports LaTex interpretation/compilation, it is useful to have a translation from one markup language to another.

Using utils.SVGText() replaces markups, such as /textbf{}, into an equivalent &lt;tspan&gt;&lt;/tspan&gt; around the tag. More LaTex markups will be added in the future.

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

'''

from setuptools import setup, find_packages
##python setup.py sdist bdist_wheel
##twine upload dist/*
VERSION = '0.0'
DESCRIPTION = 'Aesplot - Aesthetics and Framework'
LONG_DESCRIPTION = __doc__
setup(
        name="aesplot",
        version=VERSION,
        author="Heitor Gessner",
        author_email="<lab.metabio@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        python_requires='>=3.0, <4',
        install_requires=['numpy', 'matplotlib','scipy', 'pandas'],
        keywords=['R', 'statistics', 'latex', 'html', 'aesthetics'],
        classifiers= [
            'Development Status :: 4 - Beta',
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: Unix"
        ],
        project_urls={
        'Source':'https://github.com/hmynssen/Aesplot'
    }
)
