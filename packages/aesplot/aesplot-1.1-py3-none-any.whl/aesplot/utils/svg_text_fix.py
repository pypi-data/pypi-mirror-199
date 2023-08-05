import numpy as np

if __name__=='__main__':
    from latex_to_html import StringToHTML
else:
    from .latex_to_html import StringToHTML

class SVGText():

    def __init__(self,
        svg_file='',
        majorx:np.ndarray = np.empty(0),
        minorx:np.ndarray = np.empty(0),
        xlabel = '',
        majory:np.ndarray = np.empty(0),
        minory:np.ndarray = np.empty(0),
        ylabel = '',
        legend:np.ndarray = np.empty(0)):
        def array(value):
            if isinstance(value,list):
                return np.array(value)
            else:
                return value
        self.svg_file = svg_file
        self.xlabel = xlabel
        self.ylabel = ylabel

        self.majorx = array(majorx)
        self.minorx = array(minorx)
        self.majory = array(majory)
        self.minory = array(minory)
        self.legends = array(legend)

        self.conversion = StringToHTML()

    def run(self, params={}):
        with open(f'{self.svg_file}') as file:
            svg = np.array(file.read().split('\n'))
        if self.majorx.shape[0]>0 and self.majory.shape[0]>0:
            svg = self.ticks_to_text(svg, self.majorx, self.minorx, self.majory, self.minory)
        else:
            print('Major ticks for axis were not properly set. Need to include both.')
        if self.legends.shape[0]>0:
            if 'legend_font_size' in params.keys():
                params['font_size'] = params['legend_font_size']
            else:
                params['font_size'] = 18
            svg = self.legend_to_text(svg, self.legends,'legend_1', params)
        else:
            print('No Label was listed')
        if isinstance(self.xlabel, str) and self.xlabel:
            svg = self.label_to_text(svg, [self.xlabel],'matplotlib.axis_1',{'font_size':26})
        else:
            print('No label for the x-axis was given. Leaving as is.')

        if isinstance(self.ylabel, str) and self.ylabel:
            svg = self.label_to_text(svg, [self.ylabel],'matplotlib.axis_2',{'font_size':26})
        else:
            print('No label for the y-axis was given. Leaving as is.')

        self.save_svg_from_numpy(svg)

    def find_id_location(self, full_svg: np.ndarray, string_value:str):
        return np.where(np.char.find(full_svg,string_value)!=-1)[0][0]

    def count_indent(self, string_value:str) -> int:
        indent_counter = 0
        for _counter, stringsplit in enumerate(string_value.split(' ')):
            if stringsplit:
                indent_counter = _counter
                break
        return indent_counter

    def find_closure(self, full_svg: np.ndarray, start_index: int) -> int:
        counter = 0
        for line_index, line in enumerate(full_svg[start_index:]):
            if '</g' in line:
                counter-=1
                if counter==0:
                    return start_index+line_index
            if '<g' in line and not '/>' in line:
                counter+=1
        return full_svg.shape[0]-1

    def grab_by_id(self, full_svg, id_name) -> np.ndarray:
        index = self.find_id_location(full_svg, id_name)
        begin = full_svg[index]
        indent = self.count_indent(begin)
        closure = self.find_closure(full_svg,index)
        partial_svg = full_svg[index:closure+1]
        return partial_svg, index

    def replace(self, full_svg, begin, end, new_list):
        half1 = full_svg[:begin]
        half2 = full_svg[end:]
        new_svg = np.append(half1, new_list, 0)
        new_svg = np.append(new_svg, half2, 0)
        return new_svg

    def make_svg_list(self, new_svg, text, begin_index, value, param={}):
        ##transform is the text alignment
        transform, transform_index = self.grab_by_id(text,'transform')

        ##grab only translation and remove scale or others
        trans_line =  transform[0].strip()
        trans_index = trans_line.strip().find('transform')
        transformations = trans_line[trans_index:].split('"')[1].split(')')
        translate = [tx for tx in transformations if 'translate' in tx]
        translate = translate[0]+')' if translate else ''

        ##grab rotate
        rotate = [rx for rx in transformations if 'rotate' in rx]
        rotate = rotate[0]+')' if rotate else ''

        ##need to change
        font_size = param['font_size'] if 'font_size' in param.keys() else 18
        font_family = param['font_family'] if 'font_family' in param.keys() else 'Times New Roman'
        self.conversion.load_string(string = value)
        t=f'<text font-size="{font_size}px" font-family="{font_family}">{self.conversion.convert()}</text>'
        insert_line = [f'<g transform="{translate} {rotate}">',t,"</g>"]
        begin = begin_index+transform_index
        end = begin+len(transform)
        new_svg = self.replace(new_svg, begin, end, insert_line)
        return new_svg

    def ticks_to_text(self, full_svg, majorx=np.empty(0), minorx=np.empty(0), majory=np.empty(0), minory=np.empty(0), param={}):
        def main_loop(local_svg, totalticks, axis, param={}):
            if axis=='matplotlib.axis_1':
                axis_name='x'
            else:
                axis_name='y'
            new_svg = local_svg
            for index_tick_loop,tick_value in enumerate(totalticks):
                ax_svg, ax_index = self.grab_by_id(new_svg, axis)
                tick, tick_index = self.grab_by_id(ax_svg,f'{axis_name}tick_{index_tick_loop+1}')
                try:
                    text, text_index = self.grab_by_id(tick,'text_')
                except:
                    continue
                begin = ax_index+tick_index+text_index
                new_svg = self.make_svg_list(new_svg, text, begin, tick_value, param={'font_size':13})
            return new_svg

        totalxticks = majorx
        for mx in minorx:
            if mx in totalxticks:
                continue
            totalxticks = np.append(totalxticks, mx)

        totalyticks = majory
        for my in minory:
            if my in totalyticks:
                continue
            totalyticks = np.append(totalyticks, my)

        new_svg = main_loop(full_svg, totalxticks,'matplotlib.axis_1')
        new_svg = main_loop(new_svg, totalyticks,'matplotlib.axis_2')
        return new_svg

    def legend_to_text(self, full_svg, legend, axis_name, param={}):
        def main_loop(local_svg, totallegend, axis='legend_1', param={}):
            new_svg = local_svg
            corr = 0
            for index_legend_loop,legend_value in enumerate(totallegend):
                legend_svg, legend_index = self.grab_by_id(new_svg, axis)
                try:
                    text, text_index = self.grab_by_id(legend_svg[corr:],'text_')
                    text_index+=corr
                    corr = text_index+1
                except:
                    continue
                begin = legend_index+text_index
                new_svg = self.make_svg_list(new_svg, text, begin, legend_value, param=param)
            return new_svg
        new_svg = main_loop(full_svg, legend, axis_name, param=param)
        return new_svg

    def label_to_text(self, full_svg, label, axis_name, param={}):
        def main_loop(local_svg, totallabel, axis, param={}):
            new_svg = local_svg
            if axis=='matplotlib.axis_1':
                axis_name='x'
            else:
                axis_name='y'
            found = True
            tick_counter = 1
            while found:
                #skip ticks if there are any
                ax_svg, ax_index = self.grab_by_id(new_svg, axis)
                try:
                    tick, tick_index = self.grab_by_id(ax_svg,f'{axis_name}tick_{tick_counter}')
                except:
                    found = False
                tick_counter+=1
            for index_label_loop,label_value in enumerate(totallabel):
                label_svg, label_index = self.grab_by_id(new_svg, axis)
                try:
                    text, text_index = self.grab_by_id(label_svg[tick_index+1:],'text_')
                except:
                    continue
                begin = ax_index+tick_index+text_index+1
                new_svg = self.make_svg_list(new_svg, text, begin, label_value, param=param)
            return new_svg
        new_svg = main_loop(full_svg, label, axis_name, param=param)
        return new_svg

    def save_svg_from_numpy(self, full_svg, name='result.svg'):
        with open(name,'w') as file:
            outtext = ''
            for svgl in full_svg:
                outtext += f'{svgl}\n'
            file.write(outtext)
