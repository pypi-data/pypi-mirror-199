'''
PlotLikeR is an attempt to facilitate the transition from R to Python
Not only it trys to mimic the aesthetics of the plots in ggplot2 but
also it offers the framework based on python to simplify codes

If one only wants to use the basic aesthetics, simply run PlotLikeR.plot_cfg()

Note that the user might still need to set the grid options with

    matplotlib.pyplot.grid(
        c="white",
        lw=0.6,
        ls='-',
        which='minor',
        alpha=0.5)
    matplotlib.pyplot.grid(
        c="white",
        lw=1.,
        ls='-',
        which='minor',
        alpha=0.75)


Heitor Gessner,
19/03/2023
'''

import os
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy

if __name__=='__main__':
    from utils import SVGText
else:
    from .utils import SVGText

class PlotLikeR():
    def __init__(self, file=None):
        self.data=0
        self.plot_cfg_bool = False
        self.plot_cfg_grid_bool = False
        self.is_legend = False
        self.plot_names = []
        self.numerical_results = {}
        self.supported_fig_types = ['png', 'svg', 'pdf', 'eps']
        if isinstance(file,str):
            self.load_data(file)

    def load_data(self, file_path, x=None, y=None, type='csv'):
        with open(file_path) as file:
            if type=='csv':
                self.data = pd.read_csv(file_path)
        if x:
            self.data = self.data.rename(columns={f'{x}':'x'})
            self.data['x'] = pd.to_numeric(self.data['x'].str.replace(',','.'))
            self.lowx = np.min(self.data['x'])
            self.highx = np.max(self.data['x'])
        if y:
            self.data = self.data.rename(columns={f'{y}':'y'})
            self.data['y'] = pd.to_numeric(self.data['y'].str.replace(',','.'))

    def select_plot(self, groups, params_keys=False):
        '''
            Expect dict like:
                keys = {
                'Parameter1':'x',
                'Parameter2':'y'
                }
                groups = {
                'key_name_to_group':[{
                    'group1':'Tag1',
                    'group2':'Tag2'
                    }]
                }
            NOTE:
                keys sorted as:
                    dict -> key:value
                group sorted as:
                    dict -> key:list -> dict -> key:value

            Example:
                keys = {
                'Body weigth (kg)':'x',
                'Height (cm)':'y'
                }
                groups = {
                'Sex':[{
                    'man':'Male'},
                    'women':'Female'
                    }]
                }
        '''
        if params_keys:
            self.data = self.data.rename(columns=params_keys)
            self.data['x'] = pd.to_numeric(self.data['x'].str.replace(',','.'))
            self.lowx = np.min(self.data['x'])
            self.highx = np.max(self.data['x'])
            self.data['y'] = pd.to_numeric(self.data['y'].str.replace(',','.'))
        if not params_keys:
            if not 'x' in self.data.keys() and not 'y' in self.data.keys():
                raise "x and y not defined"
        for g in groups.keys():
            for each_data in groups[g]:
                var = list(each_data.keys())[0]
                self.plot_names.append(var)
                value = each_data[var]
                if not g in self.data.keys():
                    raise 'Group name doesnt exist'
                if isinstance(value,str):
                    exec(f'self.{var} = self.data[self.data["{g}"]=="{value}"]')
                if isinstance(value,list):
                    first = True
                    for v in value:
                        if first:
                            exec(f'self.{var} = self.data[self.data["{g}"]=="{v}"]')
                            first = False
                        else:
                            exec(f'self.{var} =  pd.concat([self.{var},self.data[self.data["{g}"]=="{v}"]])')

    def filter_sub_data(self, filter, remove=True):
        '''
            expect dict like:
            keys = {
                'name_already_created_variable' : {'key':['value']}
            }
            NOTE:
            key -> dict -> dict -> list
        '''
        for f in filter.keys():
            for k in filter[f].keys():
                for v in filter[f][k]:
                    if remove:
                        exec(f'self.{f} = self.{f}[self.{f}["{k}"]!="{v}"]')
                    else:
                        exec(f'self.{f} = self.{f}[self.{f}["{k}"]=="{v}"]')

    def plot_cfg(self, mat_params:dict={}):
        if not self.plot_cfg_bool:
            plt.rcParams.update({
                'font.family': 'serif',
                'font.serif': 'DejaVu Serif',
                'mathtext.fontset': 'dejavuserif',
                'font.size':18,
                'axes.labelsize': 26,
                'axes.grid': True,
                'axes.grid.which': 'both',
                'xtick.labelsize':13,
                'xtick.minor.size': 0,
                'ytick.labelsize':13,
                'ytick.minor.size': 0,
                'axes.linewidth':0,
                'axes.axisbelow':True,
                'axes.facecolor':'#EBEBEB',
                'text.usetex': True,
                'text.latex.preamble': '\\usepackage{amsmath}\n \\usepackage[dvipsnames]{xcolor}'
            })
        grab_params = list(plt.rcParams.keys())
        for key in mat_params.keys():
            if not key in grab_params:
                continue
            plt.rcParams.update({
                f'{key}':f'{mat_params[key]}'
            })
        self.plot_cfg_bool = True

    def plot_cfg_grid(self, grid_params:dict={}):
        if not self.plot_cfg_grid_bool:
            plt.rcParams.update({
                'axes.grid':True, # display grid or not
                'axes.grid.axis':'both', # which axis the grid should apply to
                'axes.grid.which':'both', # grid lines at {major, minor, both} ticks
                'grid.color':"white", # grid color
                'grid.linestyle':'-', # solid
                'grid.linewidth':0.8, # in points
                'grid.alpha':1.0, # transparency, between 0.0 and 1.0
            })
        grab_params = list(plt.rcParams.keys())
        for key in grid_params.keys():
            if not key in grab_params:
                continue
            plt.rcParams.update({
                f'{key}':f'{mat_params[key]}'
            })
        self.plot_cfg_grid_bool = True

    def plot(self, params:dict={}, figsize:tuple=(10.5, 7.75), grid_minor_params:dict = {}, grid_major_params:dict = {}):
        '''
            The grid params are not the ticks!
            Default minor params:
                grid_minor_params = {
                    'c': "white",
                    'lw': 0.6,
                    'ls': '-',
                    'alpha': 0.5
                }

            Default major params:
                grid_major_params = {
                    'c': "white",
                    'lw': 1.5,
                    'ls': '-',
                    'alpha': 0.75
                }
        '''
        if not self.plot_cfg_bool:
            self.plot_cfg()
        selected_names = self.plot_names
        selected = []
        for name in selected_names:
            aux = eval(f"self.{name}[['x','y']]")
            if aux.isnull().values.any():
                aux = aux.dropna()
                print(f'NaN value ecountered in {name}')
                print(f'Removed row with pandas.dropna() to proceed')
            selected.append(aux)
        self.figure = plt.figure(figsize=figsize)
        self.ax = self.figure.add_subplot()
        for index,(s,name) in enumerate(zip(selected,selected_names)):
            x = s['x']
            y = s['y']

            if not name in params.keys():
                print(f'{name} is not set in params FrameWork\nSkipping {name}\'s plot')
                continue
            par = params[name]
            if 'label' in par.keys() and not par['label']=='':
                self.is_legend = True

            if 'plot_linear' in par.keys() and par['plot_linear']:
                global_range = par['global'] if 'global' in par.keys() else False
                x2,y2 = self._compute_lin_reg(x, y, name, global_range=global_range)
                self._plot(x2, y2, par, index)
                if 'rib' in par.keys() and par['rib']:
                    ts = abs(scipy.stats.t.ppf(1-(1-0.95)/2, len(x)-2))
                    self._plot_ci_manual(ts, len(x), x, y, x2, y2,
                                col=par["cci"] if "cci" in par.keys() else "ligthgrey",
                                zorder=par['zorder'] if 'zorder' in par.keys() else 0)

            if 'plot_fit_to' in par.keys():
                local_function = par['plot_fit_to'] #grabs the string
                if par['plot_fit_to'] in dir(self) and callable(eval(f'self.{local_function}')):
                    local_function = eval(f'self.{local_function}') #eval returns self.func_name
                    global_range = par['global'] if 'global' in par.keys() else False
                    x2,y2 = self._compute_best_fit(x, y, name, local_function, global_range=global_range)
                    self._plot(x2, y2, par, index)
                    if 'rib' in par.keys() and par['rib']:
                        ts = abs(scipy.stats.t.ppf(1-(1-0.95)/2, len(x)-2))
                        self._plot_ci_manual(ts, len(x), x, y, x2, y2,
                                    col=par["cci"] if "cci" in par.keys() else "ligthgrey",
                                    zorder=par['zorder'] if 'zorder' in par.keys() else 0)
                else:
                    err_msg = '''
                        Make sure you added the function to be fitted to the MatPlot() class

                        Here's an example:
                            def my_func(x,a,b):
                                return a*x + b

                            my_example = MyPlot()
                            myexample.my_func = my_func

                        Also make sure that you have the same name/string when plotting
                        your group of choice:
                        params = {
                            'my_group' = {
                                'plot_fit_to':'my_func'
                            }
                        }
                    '''
                    raise err_msg

            if 'scatter_plot' in par.keys() and par['scatter_plot']:
                self.ax.scatter(x,y,
                    c=par["cs"] if 'cs' in par.keys() else 'black',
                    marker=par["marker"] if 'marker' in par.keys() else 'o',
                    s=par['s'] if 's' in par.keys() else 5,
                    label=par['label'] if 'label' in par.keys() else '',
                    zorder=3*index+2)
        if self.is_legend:
            self.legend = plt.legend()

        if not self.plot_cfg_grid_bool:
            gmp = grid_minor_params
            self.ax.grid(c=gmp['c'] if 'c' in gmp.keys() else "white",
                lw=gmp['lw'] if 'lw' in gmp.keys() else 0.6,
                ls=gmp['ls'] if 'ls' in gmp.keys() else '-',
                which='minor',
                alpha=gmp['alpha'] if 'alpha' in gmp.keys() else 0.5)

            gmp = grid_major_params
            self.ax.grid(c=gmp['c'] if 'c' in gmp.keys() else "white",
                lw=gmp['lw'] if 'lw' in gmp.keys() else 1.5,
                ls=gmp['ls'] if 'ls' in gmp.keys() else '-',
                which='major',
                alpha=gmp['alpha'] if 'alpha' in gmp.keys() else 0.75)
        else:
            gmp = grid_minor_params
            self.ax.grid(lw=gmp['lw'] if 'lw' in gmp.keys() else 0.6,
                ls=gmp['ls'] if 'ls' in gmp.keys() else '-',
                which='minor',
                alpha=gmp['alpha'] if 'alpha' in gmp.keys() else 0.5)

            gmp = grid_major_params
            self.ax.grid(lw=gmp['lw'] if 'lw' in gmp.keys() else 1.5,
                ls=gmp['ls'] if 'ls' in gmp.keys() else '-',
                which='major',
                alpha=gmp['alpha'] if 'alpha' in gmp.keys() else 0.75)


    def set_legend_marker(self, params):
        if not self._check_plot_exists():
            return
        if 's' in params.keys():
            if isinstance(params['s'], list):
                l_size = self.legend.legend_handles.shape[0]
                if not l_size==len(params['s']):
                    raise f"Can not set {l_size} legend marker(s) size with list of size {params['s']}"
                for handle, s in zip(self.legend.legend_handles,params['s']):
                    handle._sizes = [s]
            if isinstance(params['s'], int):
                size = params['s']
                for handle in self.legend.legend_handles:
                    handle._sizes = [size]

    def set_axis_label(self, x='', y=''):
        if not self._check_plot_exists():
            return
        if isinstance(x, str) and x:
            local = self.ax.set_xlabel(x)
        if isinstance(y, str) and y:
            self.ax.set_ylabel(y)

    def set_xlim(self, x1, x2=False):
        if not self._check_plot_exists():
            return
        if not x2:
            self.ax.xlim(x1)
        else:
            self.ax.xlim(x1,x2)
    def set_ylim(self, y1, y2=False):
        if not self._check_plot_exists():
            return
        if not y2:
            self.ax.ylim(y1)
        else:
            self.ax.ylim(y1,y2)

    def set_xticks(self,low=False,high=False,interval=False,arange=False,which='major'):
        '''
        Prefer to use ticks instead of limits since ticks
        will also set the limits
        '''
        if not self._check_plot_exists():
            return

        if not isinstance(arange, np.ndarray):
            if isinstance(low,bool) or isinstance(high,bool):
                print("Not setting xticks; no argument was passed")
                return
            if isinstance(low,float) and not isinstance(high,float):
                print('High limit for xticks was never set')
                return
            if isinstance(high,float) and not isinstance(low,float):
                print('Low limit for xticks was never set')
                return
            if isinstance(high, flaot) and isinstance(low,float):
                if not isinstance(interval,float):
                    print('Interval was not set or is not a number')
                    interval = (high-low)%4
                    print(f'Automatic interval generate: every {interval}')
                local_arange = np.arange(low,high+interval,interval)
        else:
            local_arange = arange

        if which=='major':
            self.ax.set_xticks(local_arange)
        if which=='minor':
            self.ax.set_xticks(local_arange,minor=True)

        if not which=='major' and not which=='minor':
            print(f'Cannot set ticks for {which}')
    def set_yticks(self,low=False,high=False,interval=False,arange=False,which='major'):
        '''
        Prefer to use ticks instead of limits since ticks
        will also set the limits
        '''
        if not self._check_plot_exists():
            return

        if not isinstance(arange, np.ndarray):
            if isinstance(low,bool) or isinstance(high,bool):
                print("Not setting yticks; no argument was passed")
                return
            if isinstance(low,float) and not isinstance(high,float):
                print('High limit for yticks was never set')
                return
            if isinstance(high,float) and not isinstance(low,float):
                print('Low limit for yticks was never set')
                return
            if isinstance(high, flaot) and isinstance(low,float):
                if not isinstance(interval,float):
                    print('Interval was not set for yticks or is not a number')
                    interval = (high-low)%4
                    print(f'Automatic interval generate: every {interval}')
                local_arange = np.arange(low,high+interval,interval)
        else:
            local_arange = arange

        if which=='major':
            self.ax.set_yticks(local_arange)
        if which=='minor':
            self.ax.set_yticks(local_arange,minor=True)

        if not which=='major' and not which=='minor':
            print(f'Cannot set ticks for {which}')

    def show(self):
        plt.show()

    def apply_to_x(self, fun, data_name='data'):
        if not 'x' in self.data.keys():
            raise f'x has not been specified yet. Could not apply {fun} to x'
        exec(f"self.{data_name}['x'] = fun(self.{data_name}['x'])")
        self.lowx = np.min(self.data['x'])
        self.highx = np.max(self.data['x'])
    def apply_to_y(self, fun, data_name='data'):
        if not 'y' in self.data.keys():
            raise f'y has not been specified yet. Could not apply {fun} to y'
        exec(f"self.{data_name}['y'] = fun(self.{data_name}['y'])")

    def save_results(self, path='', file='results.json'):
        '''
            For linear regression:
                -intercept
                -intercept_stderr
                -pvalue
                -rvalue
                -slope
                -stderr
                -DOF
            For generic function:
                -each parameter
                -each error
                -DOF
            No p-value nor R-squared for generic regressions
        '''
        if not file[-5:]=='.json':
            file+='.json'
        if path and not path[-1]=='/':
            path+='/'
        with open(f'{path}{file}','w') as output:
            outputtext = json.dumps(self.numerical_results, indent=2)
            output.write(outputtext)

    def save_plots(self,type='png',path='', file='results'):
        def fix_svg(path,file):
            #For svg only
            majorx = [v._x for v in self.ax.get_xmajorticklabels()]#majorx #x ticks
            minorx = [v._x for v in self.ax.get_xminorticklabels()] #only if minor ticks have numbers
            xlabel = self.ax.get_xlabel()
            majory = [v._y for v in self.ax.get_ymajorticklabels()] #y ticks
            minory= [v._y for v in self.ax.get_yminorticklabels()] #only if minor ticks have numbers
            ylabel = self.ax.get_ylabel()
            if self.is_legend:
                l = []
                for label in self.legend.legend_handles:
                    l.append(label.get_label())
                legends = l
            else:
                legends = ['']
            svg = utils.SVGText(svg_file=f'{path}{file}',
                                majorx = majorx, #x ticks
                                minorx = minorx, #only necessary if minor ticks have numbers
                                xlabel = xlabel,
                                majory = majory, #y ticks
                                minory= minory, #only necessary if minor ticks have numbers
                                ylabel = ylabel,
                                legend = legends)
            params = {
                'legend_font_size':18,
            }
            svg.run()

        if path and not path[-1]=='/':
            path+='/'
        if not isinstance(file,str):
            raise 'File name for saving images has to be a single string'
        ending = file.split('.')


        if len(ending)<2:
            pass
        else:
            if len(ending)>2:
                pass
            else:
                if ending[1] in self.supported_fig_types and not isinstance(type,list):
                    plt.savefig(f"{path}{file}",bbox_inches='tight')
                    if ending[1]=='svg':
                        fix_svg(path,file)
                    return
                else:
                    raise f'Cannot save {ending[1]} images, please use:\n{self.supported_fig_types}'
        if isinstance(type,str):
            t = type
            if t in self.supported_fig_types:
                plt.savefig(f"{path}{file}.{t}",bbox_inches='tight')
                if t=='svg':
                    fix_svg(path,f'{file}.{t}')
            else:
                print(f'Canont save figure in format {t}')
        if isinstance(type,list):
            for t in type:
                if t in self.supported_fig_types:
                    plt.savefig(f"{path}{file}.{t}",bbox_inches='tight')
                    if t=='svg':
                        fix_svg(path,f'{file}.{t}')
                else:
                    print(f'Canont save figure in format {t}')

    def _low_key_sum(self, y, x=False):
        '''
        ZAR, J. H. Biostatistical Analysis 5th by Jerrold H. Zar. 5th edition. Noida: PIE, 2009.

        This refers to the summantion with lower key, for example,
            \sum{x}
        instead of
            \sum{X}

        It is used in example 17.1 and 17.2
        '''
        if isinstance(x, bool):
            return (y**2).sum()-(y.sum()**2)/y.shape[0]
        else:
            return (x*y).sum()-(x.sum()*y.sum())/y.shape[0]

    def _plot_ci_manual(self, t, n, x, y, x2, y2, col="lightred", zorder=0):
        '''
        ZAR, J. H. Biostatistical Analysis 5th by Jerrold H. Zar. 5th edition. Noida: PIE, 2009.

        It is used in example 17.2 onward. Special attention to example 17.5 (p. 344).
        '''
        rss =  self._low_key_sum(y,x)**2/self._low_key_sum(x)
        tss = self._low_key_sum(y)
        sy=(tss-rss)/(n-2)
        frac = ((x2 - x.mean())**2)/self._low_key_sum(x)
        ci = t * np.sqrt(sy) * np.sqrt(1/n + frac)
        self.ax.fill_between(x2, y2 - ci, y2 + ci,
                        color=col,
                        facecolor=col,
                        edgecolor=col,
                        zorder=zorder)

    def _compute_lin_reg(self, x, y, name, global_range=False):
        res = scipy.stats.linregress(x, y)
        if global_range:
            x2 = np.linspace(self.lowx, self.highx, len(x))
        else:
            x2 = np.linspace(np.min(x), np.max(x), len(x))
        y2 = res.intercept + res.slope*x2
        results = {}
        keys = ['intercept', 'intercept_stderr', 'pvalue', 'rvalue', 'slope', 'stderr']
        for k in keys:
            results[k] = eval(f'res.{k}')
        results['DOF'] = x.shape[0]-2
        self.numerical_results[f'{name}'] = {'lin_reg':results}
        return x2,y2

    def _compute_best_fit(self, x, y, name, fit_func, global_range=False):
        res, pcov = scipy.optimize.curve_fit(fit_func,x,y)
        perr = np.sqrt(np.diag(pcov))
        if global_range:
            x2 = np.linspace(self.lowx, self.highx, len(x))
        else:
            x2 = np.linspace(np.min(x), np.max(x), len(x))
        y2 = fit_func(x2,*res)
        # results = {}
        # for k in keys:
        #     results[k] = eval(f'res.{k}')
        # results['DOF'] = x.shape[0]-2
        # self.numerical_results[f'{name}'] = {'lin_reg':results}
        return x2,y2

    def _plot(self, x, y, par, index):
        self.ax.plot(x, y,
            ls=par['lsp'] if 'lsp' in par.keys() else '-',
            lw=par['lwp'] if 'lwp' in par.keys() else 1.,
            c=par['cp'] if 'cp' in par.keys() else 'black',
            alpha=par['alphap'] if 'alphap' in par.keys() else 1.,
            zorder=3*index+1)

    def _check_plot_exists(self):
        if hasattr(self, 'ax') and hasattr(self, 'figure'):
            return True
        return False
