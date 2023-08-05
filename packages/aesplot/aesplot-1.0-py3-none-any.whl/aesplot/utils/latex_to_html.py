import re

class StringToHTML:
    def __init__(self, string = ''):

        self.text_str = str(string)
        self.special_charecters = {
            'square-root':'&#8730',
            'cube-root':'&#8731',
            'fourth-root':'&#8732',
            'sum':'&#8721',
            'minus-or-plus':'&#8723', #rotate(-90) for plus or minus
            'approx':'&#8773'
        }
        self.supported_latex = [
            r'\text',
            r'\left',
            r'\right',
            r'^',
            r'_',
            r'\textit',
            r'\textb',
            r'\sqrt',
            r'\sqrt[3]',
            r'\sqrt[4]'
        ]
        self.special_latex = [
            r'\left',
            r'\right',
            r'^',
            r'_'
        ]
        self.latex_to_html = {
            r'\text' : ['','','',''],
            r'\left' : [r'<tspan font-size="1.2em">',r'</tspan>','<tspan font-size="1em">',r'</tspan>'],
            r'\right' : ['<tspan font-size="1.2em">',r'</tspan>','<tspan font-size="1em">',r'</tspan>'],
            r'^' : ['<tspan dy="-7" font-size=".7em">',r'</tspan>','<tspan dy="7" font-size="1em">',r'</tspan>'],
            r'_' : ['<tspan dy="7" font-size=".7em">',r'</tspan>','<tspan dy="-7" font-size="1em">',r'</tspan>'],
            r'\textit' : ['<tspan  font-style="italic">',r'</tspan>','<tspan font-style="normal">',r'</tspan>'],
            r'\textb' : ['<tspan font-weight="bold">',r'</tspan>','<tspan font-weight=100>',r'</tspan>'],
            r'\sqrt' : [self.special_charecters['square-root'],'','',''],
            r'\sqrt[3]' : [self.special_charecters['cube-root'],'','',''],
            r'\sqrt[4]' : [self.special_charecters['fourth-root'],'','','']
        }

    def load_string(self, string = ''):
        self.text_str = str(string)

    def find_closure(self,string):
        '''
        Note that some special keys won't go throught this criteria
        '''
        counter = 1
        for s_index,s in enumerate(string):
            if s=="{":
                counter+=1
            if s=="}":
                counter-=1
            if not counter:
                return s_index, counter
        return s_index, counter

    def convert(self):
        '''
        The logic is to find latex operations and replace it with (A LOT OF) tspan
        There must be a more efficient way of doing this but using:
            self.latex_to_html
            self.special_latex
            self.supported_latex
            self.special_charecters
        as they are, it is much easier to expand and maintain.
        '''
        text_str = self.text_str
        if text_str[0]=='$' and text_str[-1]=='$':
            text_str = text_str[1:-1]
            for sl in self.supported_latex:
                begin = text_str.find(sl)
                thislist = [m.start() for m in re.finditer(f'\{sl}', text_str)]
                correction = 0
                for begin in thislist:
                    if begin>=0 and thislist:
                        if not sl in self.special_latex:
                            end = self.find_closure(text_str[begin+len(sl)+1-correction:])
                        else:
                            if (sl=='^' or sl=='_') and text_str[begin+len(sl)-correction]=='{':
                                end = self.find_closure(text_str[begin+len(sl)+1-correction:])
                            else:
                                end=begin+len(sl)+1-correction,0

                        if end[1]:
                            print('Error in Latex Syntax')
                            exit()

                        ## Here strats the wrapping around
                        ##also there is a concern about the removal of elements from
                        ##the original string. The correction int keeps track of this
                        ##alterations.
                        before = text_str[:begin-correction]
                        if not sl in self.special_latex:
                            index_cut = begin+len(sl)+1-correction
                            inside = self.latex_to_html[sl][0] + text_str[index_cut:index_cut+end[0]] + self.latex_to_html[sl][1]
                            after = self.latex_to_html[sl][2] + text_str[index_cut+1+end[0]:] + self.latex_to_html[sl][3]
                            correction += 2
                        else:
                            if (sl=='^' or sl=='_') and text_str[begin+len(sl)-correction]=='{':
                                index_cut = begin+len(sl)+1-correction
                                inside = self.latex_to_html[sl][0] + text_str[index_cut:index_cut+end[0]] + self.latex_to_html[sl][1]
                                after = self.latex_to_html[sl][2] + text_str[index_cut+1+end[0]:] + self.latex_to_html[sl][3]
                                correction += 2
                            else:
                                inside = self.latex_to_html[sl][0] + text_str[end[0]-1-correction] + self.latex_to_html[sl][1]
                                after = self.latex_to_html[sl][2] + text_str[end[0]-correction:] + self.latex_to_html[sl][3]

                        correction += len(self.latex_to_html[sl][0]) \
                                    + len(self.latex_to_html[sl][1]) \
                                    + len(self.latex_to_html[sl][2]) \
                                    + len(self.latex_to_html[sl][3])
                        correction+=len(sl)
                        text_str = before+inside+after
        return text_str
