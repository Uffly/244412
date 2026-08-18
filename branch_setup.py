from neuron import h, gui
import nrnutils_ss as nu
import toolbox as tb
from Spine import Spine
import pyr_2005 as pyr
from random import sample,choice
import numpy as np
# import ipdb

class Spiny_branch():

    def __init__(self,
                 p,
                 rank=0):
    
        h.celsius = p['temperature']

        # Load the branch 93 with its channels
        self.cell = pyr.cell(records=[
            {'section':'soma',
             'variable':'v',
             'location':0.5,
             'unit':'mV'},
            {'section':'branch_base',
             'variable':'v',
             'location':0.5,
             'unit':'mV'},
             {'section':'branch37_base',  #Bez kolców
             'variable':'v',
             'location' : 0.5,
             'unit' : 'mV'}]
                             )

        # # Set branhc erev
        # for sec in self.cell.branch_sl:
        #     sec.ena = p['erev_na']
        #     sec.ek = p['erev_k']
        #     if p['check']:
        #         print sec.ena,sec.ek

        # ipdb.set_trace()
        # self.cell.balance_currents(p['Vrest'], check = p['check'])


        # Spine mechanisms
        self.cad = nu.Mechanism('cad', depth = 0.05, tauca = 12, cainf = 100e-6) # depth in um, tau in ms, cainf in mM
        self.pas = nu.Mechanism('pas', e=p['Vrest'], g=1./p['Rm'])
        self.cal = nu.Mechanism ('cal', gcalbar=p['gcalbar'])
        self.can = nu.Mechanism ('can', gcanbar=p['gcanbar'])
        self.cat = nu.Mechanism ('cat', gcatbar=p['gcatbar'])
        
        h.use_mcell_ran4()
        self.MCell_Ran4_lowindex = 42
        h.mcell_ran4_init(self.MCell_Ran4_lowindex)
        self.noiseRandObj = h.Random() #Provides NOISE with random stream
        self.MCell_Ran4_highindex = [self.noiseRandObj.MCellRan4(12345)]
        self.noiseRandObj.uniform(0,1)

        self.branch_segments = [[sec, seg] for sec in list(self.cell.branch38.values()) for seg in sec]
        #self.branch_segments_2 = [[sec, seg] for sec in list(self.cell.branch8.values()) for seg in sec]
        #self.branch_segments_3 = [[sec, seg] for sec in list(self.cell.branch37.values()) for seg in sec]

        self.seg_indexes = [-1,-1,-1,-1,-7,-6,-5,-15,-14,-13,-20,-22] # 12 spines [0:11]
        #self.seg_indexes_2 =[-22,-21,-20,-22,-21,-20] # 6 extra spines [12:17]


        # Seg_indexes are saved in the sim data file.
        self.spine_segments = [self.branch_segments[idx] for idx in self.seg_indexes]
        #self.spine_segments.extend([self.branch_segments_2[idx] for idx in self.seg_indexes_2])
        print([str(sn) for sn in self.spine_segments])

        # Spines
        self.spines = []
        for i,s in enumerate(self.spine_segments):
            self.spines.append(Spine('Spine_%g'%i,p,
                                neck_mechanisms=[self.pas],
                                connection_point = 0,
                                parent = s,
                                head_mechanisms=[self.cad,
                                                 self.pas,
                                                 self.cal, self.can,
                                                 self.cat],
                                noiseRandObj = self.noiseRandObj,
                                     balance_currents=True,
                                     highindex=self.MCell_Ran4_highindex[-1]))
            self.MCell_Ran4_highindex.append(self.noiseRandObj.MCellRan4())
                      
    def plot_branch(self,
                    variable,
                    type='mech',
                    label='',
                    location=0.5,
                    tmin=0,
                    tmax=5,
                    xmin=-80,
                    xmax=40,
                    view=None,
                    show=1,
                    color='k',
                    line=1,
                    graph=None):

        # Convert color to number
        colors = {'r':2,'k':1,'g':4,'b':3,'o':5,'mr':7,'m':9,'y':8}
        color = colors[color]
        import neuron.gui
        if graph is None:
            self.graph = h.Graph(show)
            graph = self.graph
            h.graphList[0].append(graph)
            graph.size(tmin, tmax, xmin, xmax)
            if view is not None:
                graph.view(view[0],view[1],view[2],
                           view[3],view[4],view[5],view[6],view[7])
        if not label:
            label = variable
        if 'mech' in type:
            graph.addvar('%s(%g)'%(label,location),
                         '%s(%g)' % (variable, location),
                         color, line, sec=self.cell.branch_base)
        if 'pp' in type:
            graph.addvar('%s(%g)'%(label,location),
                         getattr(getattr(self,variable[0]),
                                 '_ref_'+variable[1]),
                         color, line, sec=self.cell.branch_base)

        return graph
    
    def plot_soma(self,
                  variable,
                  type='mech',
                  label='',
                  location=0.5,
                  tmin=0,
                  tmax=5,
                  xmin=-80,
                  xmax=40,
                  view=None,
                  show=1,
                  color='k',
                  line=1,
                  graph=None,
                  position=None):

        # Convert color to number
        colors = {'r':2,'k':1,'g':4,'b':3,'o':5,'mr':7,'m':9,'y':8,
                  '1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}
        color = colors[str(color)]
        if position is None:
            position = [0.8,0.9]
        import neuron.gui
        if graph is None:
            self.graph = h.Graph(show)
            graph = self.graph
            h.graphList[0].append(graph)
            graph.size(tmin, tmax, xmin, xmax)
            if view is not None:
                graph.view(view[0],view[1],view[2],
                           view[3],view[4],view[5],view[6],view[7])
        if not label:
            label = variable
        if 'mech' in type:
            graph.addvar('%s(%g)'%(label,location),
                         '%s(%g)' % (variable, location),
                         color, line, sec=self.cell.soma)
        if 'pp' in type:
            graph.addvar('%s(%g)'%(label,location),
                         getattr(getattr(self,variable[0]),
                                 '_ref_'+variable[1]),
                         color, line, sec=self.cell.branch_base)

        graph.flush()
        return graph
