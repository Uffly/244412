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
             'unit':'mV'}]
                             )

        # # Set branhc erev
        # for sec in self.cell.branch_sl:
        #     sec.ena = p['erev_na']
        #     sec.ek = p['erev_k']
        #     if p['check']:
        #         print sec.ena,sec.ek

        # ipdb.set_trace()
        # self.cell.balance_currents(p['Vrest'], check = p['check'])
        # done in the hoc file
        # self.cell.record(['vm','spikes'])

        # Spine mechanisms
        self.cad = nu.Mechanism('cad', depth = 0.05, tauca = 12, cainf = 100e-6) # depth in um, tau in ms, cainf in mM
        self.pas = nu.Mechanism('pas', e=p['Vrest'], g=1./p['Rm'])
        self.cal = nu.Mechanism ('cal', gcalbar=p['gcalbar'])
        self.can = nu.Mechanism ('can', gcanbar=p['gcanbar'])
        self.cat = nu.Mechanism ('cat', gcatbar=p['gcatbar'])
        # self.kad = nu.Mechanism ('kad', gkabar=0)
        # self.na3 = nu.Mechanism ('na3', gbar=0)
        # self.kdr = nu.Mechanism ('kdr', gkdrbar=0)
        
        h.use_mcell_ran4()
        self.MCell_Ran4_lowindex = 42
        h.mcell_ran4_init(self.MCell_Ran4_lowindex)
        self.noiseRandObj = h.Random() #Provides NOISE with random stream
        self.MCell_Ran4_highindex = [self.noiseRandObj.MCellRan4(12345)]
        self.noiseRandObj.uniform(0,1)

        self.branch_segments = [[sec,seg] for sec in list(self.cell.branch38.values()) for seg in sec]
        self.branch_segments_2 = [[sec,seg] for sec in list(self.cell.branch8.values()) for seg in sec]
        self.branch_segments_3 = [[sec,seg] for sec in list(self.cell.branch37.values()) for seg in sec]
        # self.spine_segments = sample(self.branch_segments,p['nspines'])
        # self.spine_segments = self.branch_segments[0:len(self.branch_segments):3]

        # # Some spines potentiate before others, thus we set those spines to be at the dendritic tip where
        # # the BPAP has larger amplitud yielding a larger Ca2+ transient, more fused vesicles, more pro/mBDNF in the syn cleft
        # # with a resulting earlier/faster potentiation.
        # self.spine_segments = [self.branch_segments[-1],
        #                        self.branch_segments[-1],
        #                        self.branch_segments[-1],
        #                        self.branch_segments[-1]]# 4 spines at the branch tip
        # self.spine_segments.extend(self.branch_segments[-7:-4]) # 3 spines in the middle
        # self.spine_segments.extend(self.branch_segments[-15:-12]) # 4 near the branching point
        # self.spine_segments.extend([self.branch_segments[-20]])
        # self.spine_segments.extend([self.branch_segments[-22]])
        # # print len(self.branch_segments), self.branch_segments[-22:-19]
        # self.spine_segments.extend(self.branch_segments_2[-22:-19])
        # self.spine_segments.extend(self.branch_segments_2[-22:-19])
        # # self.spine_segments.extend([self.branch_segments[-25]])
        # # self.spine_segments.extend([self.branch_segments[-26]])
        # # self.spine_segments.extend([self.branch_segments_3[-1]])
        # # self.spine_segments.extend([self.branch_segments_3[-3]])
        # print "LENGTH",len(self.spine_segments)
        
        self.seg_indexes = [-1,-1,-1,-1,-7,-6,-5,-15,-14,-13,-20,-22] # 12 spines [0:11]
        self.seg_indexes_2 =[-22,-21,-20,-22,-21,-20] # 6 extra spines [12:17]

        # # Generate randomly selected set
        # # self.seg_indexes = sample(range(0,len(self.branch_segments)-15),p['nspines'])
        # self.seg_indexes = np.random.choice(range(len(self. branch_segments)),size=p['nspines'])
        # self.seg_indexes_2 = np.random.choice(range(len(self.branch_segments_2)),size=p['nspines_2'])
        # Seg_indexes are saved in the sim data file.
        self.spine_segments = [self.branch_segments[idx] for idx in self.seg_indexes]
        self.spine_segments.extend([self.branch_segments_2[idx] for idx in self.seg_indexes_2])
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
        # Set specific RM11 and RMD time constants        
        self.spines[0].head.RMECB.tau_RMLTP11 = self.spines[0].head.RMECB.tau_RMLTP11/3
        self.spines[1].head.RMECB.tau_RMLTP11 = self.spines[0].head.RMECB.tau_RMLTP11
        self.spines[2].head.RMECB.tau_RMLTP11 = self.spines[0].head.RMECB.tau_RMLTP11
        
        self.spines[3].head.RMECB.tau_RMLTP11 = self.spines[3].head.RMECB.tau_RMLTP11
        self.spines[4].head.RMECB.tau_RMLTP11 = self.spines[3].head.RMECB.tau_RMLTP11

        self.spines[5].head.RMECB.tau_RMLTP11 = self.spines[3].head.RMECB.tau_RMLTP11 * 1.5

        self.spines[6].head.RMECB.tau_RMLTP11 = self.spines[3].head.RMECB.tau_RMLTP11 * 1.5

        self.spines[7].head.RMECB.tau_RMLTP11 = self.spines[7].head.RMECB.tau_RMLTP11 * 1.7
        self.spines[8].head.RMECB.tau_RMLTP11 = self.spines[7].head.RMECB.tau_RMLTP11
        self.spines[9].head.RMECB.tau_RMLTP11 = self.spines[7].head.RMECB.tau_RMLTP11

        self.spines[10].head.RMECB.tau_RMLTP11 = self.spines[3].head.RMECB.tau_RMLTP11 * 2
        self.spines[11].head.RMECB.tau_RMLTP11 = self.spines[3].head.RMECB.tau_RMLTP11

        # # Set specific BDNF  constants        
        # for s_i,s in enumerate(self.spines[12:18]):
        #     s.head.BDNF.theta_cai_BDNF = 0.045 # set a low cai threshold these spines on branch8
        #     s.head.internal_nc.threshold = s.head.BDNF.theta_cai_BDNF
        #     s.head.RMECB.theta_cai_RMBLK = 0.052 # set a low cai threshold these spines on branch8
        #     s.head.RMECB.theta_cai_RM = 0.006 # set a low cai threshold these spines on branch8
        #     s.head.BDNF.theta_gAMPA = 0.02 # set a normal threshold for test
        #     s.head.BDNF.alpha_gAMPA = 1.5 # set a high LTP
        #     s.head.BDNF.v_BDNF = 0.002*1.0 # Increase BDNF release at these spines
        # self.spines[12].head.BDNF.theta_gAMPA = 0.06
        # self.spines[13].head.BDNF.theta_gAMPA = 0.05
        # self.spines[14].head.BDNF.theta_gAMPA = 0.075
        # self.spines[15].head.BDNF.theta_gAMPA = 0.075
        # self.spines[16].head.BDNF.theta_gAMPA = 0.08
        # self.spines[17].head.BDNF.theta_gAMPA = 0.11
        
        for s_i,s in enumerate(self.spines):
            print(("spine ", s_i, s.head.BDNF.theta_gAMPA))
            
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
