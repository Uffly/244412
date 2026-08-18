# Records
spine_records = [
    {'variable':'cai','location':0.5,'unit':'mM'}
    ,{'variable':'gluti','location':0.5,'unit':'mM'}
    ,{'variable':'v','location':0.5,'unit':'mV'}
    ,{'variable':'ica','location':0.5,'unit':'mA/cm2'}
    ,{'variable':'iampa','point_process':'AMPA','location':0.5,'unit':'nA'}
    ,{'variable':'U_SE_factor','point_process':'AMPA','location':0.5,'unit':''}
    ,{'variable':'U_SE','point_process':'AMPA','location':0.5,'unit':''}
    ,{'variable':'inmda','point_process':'NMDA','location':0.5,'unit':'nA'}
    ,{'variable':'ica','point_process':'NMDA','location':0.5,'unit':'nA'}
    ,{'variable':'mgb','point_process':'NMDA','location':0.5,'unit':'nA'}
    ,{'variable':'iglut','location':0.5,'unit':'mM'}
    #,{'variable':'RM','point_process':'RMECB','location':0.5,'unit':'mM'}
    #,{'variable':'RMr','point_process':'RMECB','location':0.5,'unit':'mM'}#    ,{'variable':'RMBLKe','point_process':'RMECB','location':0.5,'unit':'??'}
    #,{'variable':'RMBLK','point_process':'RMECB','location':0.5,'unit':'mM'}
    # ,{'variable':'post_intra','point_process':'RMECB','location':0.5,'unit':'mM'}
    # ,{'variable':'proBDNF','point_process':'BDNF','location':0.5,'unit':'mM'}
    # ,{'variable':'fused_vesicles','point_process':'BDNF','location':0.5,'unit':'#'}
    # ,{'variable':'mBDNF','point_process':'BDNF','location':0.5,'unit':'mM'}
    # ,{'variable':'PC','point_process':'BDNF','location':0.5,'unit':'mM'}
    # ,{'variable':'TrkB','point_process':'BDNF','location':0.5,'unit':'mM'}
    # ,{'variable':'intracell_signaling','point_process':'BDNF','location':0.5,'unit':'mM'}
    #,{'variable':'g_factor','point_process':'AMPA','location':0.5,'unit':''}
    ]

Vrest = -70 # mV
Rm = 26000
RmDend = Rm
RaAll= 150
CmDend = 1.4
gna = 0.07
nash = 0
gkdr = 0.055
kdrsh = 0
gc = 1.e-5
gcalbar = 0.5
gcatbar = 0.2
gcanbar = 0.5
temperature = 35 # deg
erev_na = 55 # mV
erev_k = -90 # mV
check = True

IC_delay_to_spike = 1.3 # ms
gc = 52e-5; # gives a BPAP [Ca]i amp = 1.71 uM, from 0.1 to 1.81 uM
nspines = 12
nspines_2 = 5
sp_delay_env = 8

spine_point_processes=[
    # {'label':'RMECB',
    #  'type':'RM_eCB',
    # 'locations':[0.5],
    # 'parameters':{'tau_RM': 7e3, #1800e3, # next 10e3 #ms
    #               'theta_cai_RM': 0.046, # mM this is tuned to distinguish between LTP1:4 deltat=5ms and LTP1:1 deltat=-5ms
    #               'sigma_cai_RM' : 0.01e-3, # mM
    #               'alpha_cai_RMBLK': 1.5e-2, # mM/ms
    #               'theta_cai_RMBLK' : 0.12, # mM
    #               'sigma_cai_RMBLK' : 0.0001, # mM
    #               'tau_RMBLK' : 1e5, # mM
    #               'tau_RMLTP11':1800e3*1.2, # ms
    #               'alpha_RMru':1.1,#1.0,#0.54, 
    #               'theta_RMru':0.15,
    #               'sigma_RMru':0.001,
    #               'tau_RM_RMr':1e3,
    #               'alpha_RM_RMr':1,
    #               'theta_RM_RMr': 0.02,
    #               'sigma_RM_RMr': 0.001
    #               }}, # to get 150% LTP as in Edlmann et al. 2015
    {'label':'AMPA',
     'type':'Wghkampa_preML',
    'locations':[0.5],
    'parameters':{'Pmax':4e-6,
                  'glut_factor': 40}},
    # {'label':'BDNF',
    #  'type':'BDNF',
    # 'locations':[0.5],
    # 'parameters':{'theta_cai_BDNF': 0.1038,
    #               'max_cai_BDNF': 0.16,
    #               'max_BDNF_rel_delay' : 300e3,
    #               'alpha_gAMPA': 1.5, #4.8, 
    #               'theta_gAMPA': 0.01,#0.038,
    #               'sigma_gAMPA': 0.00001,#0.0015,
    #               'shift_gAMPA': 0,
    #               'v_BDNF':0.002*1.0,
    #               'proBDNF_fraction':0.3,
    #               'duration_BDNF_release':1500e3}},
    {'label':'NMDA',
     'type':'ghknmda',
    'locations':[0.5],
    'parameters':{'Pmax':4e-6*4.5,
                  'mg':0.0001,
                  'mgb_k':0.22,
                  'Area': 1.0}}]
# Spike-EPSP envelop
spike_delay_rnd = 8

Block_RMBLK = 0

PPR = True
time_on_initialization = 1e3 # ms 600e3 = 10 min
time_to_begin_induction = 20e3 # ms
nstim = 70
induction_freq = 100 # Hz
BPAP_stimulus_amplitude = 5 # nA
BPAP_stimulus_amplitude_branch = 0.08 # nA
BPAP_dep_stimulus_duration = 2.5 # ms
BPAP_hyp_stimulus_duration = 0 # ms
time_after_induction = 0 # ms
test_freq = 0.05 # Hz = 1/(20sec)
time_start_induction = time_on_initialization + time_to_begin_induction
test_post_point_to_plot_interval = 2*60*1e3 # ms = 2 min see Fig1B of Edelmann2015
time_of_expression = 18e5 # ms = 30 min
activate_LTP_protocol = True
# time_delta =  [-30,-20, -10, -5]
time_delta =  [ -5, -5, -5, -5]
# time_delta =  [-10, -10, -10, -10]
override_tstop = None

ca_tuning = False
if ca_tuning:
    time_on_initialization = 1e3 # ms
    time_to_begin_induction = 100 # ms
    nstim = 35
    induction_freq = 0.5 # Hz
    BPAP_stimulus_amplitude = 0.35 # nA
    BPAP_stimulus_amplitude_branch = 0.08 # nA
    BPAP_dep_stimulus_duration = 3 # ms
    BPAP_hyp_stimulus_duration = 0 # ms
    time_after_induction = 0 # ms
    test_freq = 0.05 # Hz = 1/(20sec)
    time_start_induction = time_on_initialization + time_to_begin_induction
    test_post_point_to_plot_interval = 2*60*1e3 # ms = 2 min see Fig1B of Edelmann2015
    time_of_expression = 1800e3 # ms = 30 min
    activate_LTP_protocol = True
    time_delta =  list(range(-15,16,5))#[-10, -5]#[-20, -15, -10, -5, 0, 5, 10, 15, 20] # ms [-10, -5, 10]#
    override_tstop = 5e3
    
data_file = 'store_multi'

# Settings for Figures
# Figure list
figure_size = (6,6)
panels = {'vm spine':(0.05,0,0.3,0.3),
          'cai':(0.05,0.4,0.3,0.3),
          'use':(0.7,0,0.3,0.3),
          'gfactor':(0.4,0.7,0.3,0.3),
          # 'Spine EPSP':(0.7,0,0.3,0.3),
          # 'Soma EPSP':(0.4,0.7,0.3,0.3),
          # 'fused vesicles':(0.7,0.4,0.3,0.3)
          }
panels_seq = ['vm spine','cai',
              #'Spine EPSP','Soma EPSP',
              'use','gfactor',#'use_trans',
              # 'fused vesicles',None,
              # 'rm','bdnf',
              ]

single_figures = {
    'vm spine':(0.05,0,0.3,0.3),
    'cai':(0.05,0.4,0.3,0.3),
    'Cont EPSP':(0.7,0,0.3,0.3),
    'Pot EPSP':(0.4,0.7,0.3,0.3),
    'U_SE':(0.7,0.4,0.3,0.3),#'fused vesicles':(0.7,0.4,0.3,0.3),
    # 'bdnf':(),
    # 'trkb':(),
    # 'use':(),
    # 'rm':(),
    # 'rmd':(),
    # 'gfactor':()
          }
summary_panels = {'EPSP_sl':[['#DC143C','d',2,14],['#00008B','s',1,14],['g','+',1,14]],
          'STDP':['#DC143C','#00008B']}
# panels = {'vm_spine':(4,3,1),
#           'cai':(4,3,4),
#           'Cont_EPSP':(4,3,7),
#           'Pot_EPSP':(4,3,8),
#           'fused_vesicles':(4,3,10)
#           }
paper_fig_panels = [
    'LTP','vm_branch_pre','vm_branch_post'
    ,'rm','bdnf'
    ]

one_spine = [
    # ['Spine_9/head_9','r'],
    # ['Spine_8/head_8','k'],
    # ['Spine_7/head_7','g'],
    # ['Spine_6/head_6','c'],
    # ['Spine_5/head_5','y'],
    # ['Spine_4/head_4','b'],
    # ['Spine_3/head_3','m'],
    # ['Spine_2/head_2','k'],
    # ['Spine_1/head_1','g'],
    ['Spine_0/head_0','k']
    ]
one_spine_soma = [
    # ['Spine_9/head_9','r'],
    # ['Spine_8/head_8','k'],
    # ['Spine_7/head_7','g'],
    # ['Spine_6/head_6','c'],
    # ['Spine_5/head_5','y'],
    # ['Spine_4/head_4','b'],
    # ['Spine_3/head_3','m'],
    # ['Spine_2/head_2','k'],
    # ['Spine_1/head_1','g'],
    ['Spine_0/head_0','k'],
    ['soma','k']]
all_spines = [
    ['Spine_17/head_17','lightgreen'],
    ['Spine_16/head_16','lightgreen'],
    ['Spine_15/head_15','lightgreen'],
    ['Spine_14/head_14','lightgreen'],
    ['Spine_13/head_13','darkgreen'],
    ['Spine_12/head_12','lightcoral'],
    ['Spine_11/head_11','coral'],
    ['Spine_10/head_10','lime'],
    ['Spine_9/head_9','lime'],
    ['Spine_8/head_8','salmon'],
    ['Spine_7/head_7','g'],
    ['Spine_6/head_6','c'],
    ['Spine_5/head_5','y'],
    ['Spine_4/head_4','b'],
    ['Spine_3/head_3','m'],
    ['Spine_2/head_2','gray'],
    ['Spine_1/head_1','k'],
    ['Spine_0/head_0','r'],
    ]
all_spines_soma = [
    ['Spine_9/head_9','lime'],
    ['Spine_8/head_8','salmon'],
    ['Spine_7/head_7','g'],
    ['Spine_6/head_6','c'],
    ['Spine_5/head_5','y'],
    ['Spine_4/head_4','b'],
    ['Spine_3/head_3','m'],
    ['Spine_2/head_2','gray'],
    ['Spine_1/head_1','k'],
    ['Spine_0/head_0','r'],

    ['soma','r']
    ]
    
figure_list = {
    'cai':{'title':'Spine $\mathrm{[Ca^{2+}]}$',
           'varnames':[['cai','k']],
           'hdf5_section':all_spines,
           'location':0.5,
           'legend':True,
           'time_window':[['first_induction',
                          -40,
                          +80]],
           'xunit':'ms',
           'xlabel':'Time',
           # 'ylim':[0,0.17],
           'ylabel':'Concentration',
           # 'thresholds':[spine_point_processes[0]['parameters']['theta_cai_RM'],
           #               spine_point_processes[0]['parameters']['theta_cai_RMBLK'],
           #               spine_point_processes[2]['parameters']['theta_cai_BDNF']]
           }
    ,'vm spine':{'title':'EPSP + BPAP',
           'varnames':[['v','k']],
           'hdf5_section':one_spine,
           'location':0.5,
           'xunit':'ms',
           'legend':False,
           'xlabel':'Time',
           'ylim':[-72,0],
           'ylabel':'Memb. pot.',
           'time_window':[['first_induction',
                          -40,
                          +80]]
                 }
    ,'Cont EPSP':{'title':'EPSP before LTP',
           'hdf5_section':all_spines_soma,
           'varnames':['vm'],
           'time_window':[['pre_induction',
                          -20,
                          +80]],
           'xlabel':'Time',
           'legend':False,
           'xunit':'ms',
           'ylabel':'Memb. pot.',
            'unit':'mV'}
    ,'Pot EPSP':{'title':'EPSP after LTP',
           'hdf5_section':all_spines_soma,
           'varnames':['vm'],
           'time_window':[['post_expression',
                          -20,
                          +80]],
           'xlabel':'Time',
           'xunit':'ms',
           'ylabel':'Memb. pot.',
            'unit':'mV'}
    ,'Spine EPSP':{'title':'EPSP at spine',
           'hdf5_section':one_spine,
           'varnames':['vm'],
           'time_window':[['pre_induction',
                          -20,
                          +80],
                          ['post_expression',
                          -20,
                          +80]],
           'xlabel':'Time',
           'legend':False,
           'xunit':'ms',
           'ylabel':'Memb. pot.',
            'unit':'mV'}
    ,'Soma EPSP':{'title':'EPSP at soma',
           'hdf5_section':[['soma','k']],
           'varnames':['vm'],
           'time_window':[['pre_induction',
                          -20,
                          +80],
                          ['post_expression',
                          -20,
                          +80]],
           'xlabel':'Time',
           'legend':False,
           'xunit':'ms',
           'ylabel':'Memb. pot.',
            'unit':'mV'}
    # ,'fused vesicles':{'title':'Fused BDNF vesicles',
    #        'varnames':[['fused_vesicles','k']],
    #        'hdf5_section':all_spines,
    #        'location':0.5,
    #        'xunit':'min',
    #        'legend':False,
    #        'xlabel':'Time',
    #        'ylabel':'Count',
    #        # 'ylim':[0,70],
    #        'time_window':[['full',
    #                       -20,
    #                       +80]],
    #                    }
    # ,'vm_branch_pre':{'title':'Memb. pot. in branch',
    #        'varnames':[['branch_base_v','Blues']],
    #        'hdf5_section':['pyr2005'],
    #        'location':0.5,
    #        'time_window':[[
    #            'pre_induction', # period
    #            2, # index
    #            -20, # pre time window
    #            +100]], # post time window
    #        'xunit':'ms',
    #        'legend':False,
    #        'xlabel':'Time',
    #        'ylabel':'Voltage'}
    # ,'vm_branch_post':{'title':'Memb. pot. in branch',
    #        'varnames':[['branch_base_v','Blues']],
    #        'hdf5_section':['pyr2005'],
    #        'location':0.5,
    #        'time_window':[[
    #            'post_expression', # period
    #            -10, # index
    #            -20, # pre time window
    #            +100]], # post time window
    #        'xunit':'ms',
           # 'legend':False,
    #        'xlabel':'Time',
    #        'ylabel':'Voltage'}
    ,'LTP':{'title':'Plasticity',
           'varnames':[],
           'hdf5_section':['pyr2005'],
           'xlabel':'Time',
           'legend':False,
           'ylabel':'Change',
            'unit':'%'}
    ,'STDP':{'title':'STDP',
           'varnames':[],
           'hdf5_section':['Spine_9/head_9'],
           'location':0.5,
           'time_window':[['first_induction',
                          -20,
                          +200]],
           'xunit':'ms',
           'legend':False,
           'xlabel':'Time',
           'ylabel':'Change',
            'unit':'%'}            
    ,'PPR':{'title':'PPR',
           'varnames':[],
           'hdf5_section':['Spine_9/head_9'],
           'location':0.5,
           'time_window':[['first_induction',
                          -20,
                          +200]],
           'xunit':'ms',
           'legend':False,
           'xlabel':'Time',
           'ylabel':'Change',
           'unit':'%'}            
    # ,'rm':{'title':'Presynaptic plasticity chain',
    #        'varnames':[['RM','r'],['RMr','k']],
    #        'hdf5_section':all_spines,
    #        'xunit':'min',
    #        'location':0.5,
    #        'time_window':[['full',
    #                       -20,
    #                       +80]],
    #        'xlabel':'Time',
    #        'legend':False,
    #        'ylabel':'Concentration'}
    # ,'fullrm':{'title':'Presynaptic plasticity chain',
    #        # 'varnames':[['RM','r'],['RMr','k'],['RMBLK','g'],['U_SE','b'],['post_intra','m']],
    #        'varnames':[['RM','r'],['RMr','k'],['post_intra','m']],
    #        'hdf5_section':all_spines,
    #        'xunit':'min',
    #        'location':0.5,
    #        'time_window':[['full',
    #                       -20,
    #                       +80]],
    #        'xlabel':'Time',
    #        'legend':False,
    #        'ylabel':'Concentration'}
    # ,'rmd':{'title':'Presynaptic plasticity chain',
    #        'varnames':[['RMBLK','g']],
    #        'hdf5_section':all_spines,
    #        'xunit':'min',
    #        'location':0.5,
    #        'time_window':[['full',
    #                       -20,
    #                       +80]],
    #        'xlabel':'Time',
    #        'legend':False,
    #        'ylabel':'Concentration'}
    ,'use':{'title':'Glutammate release',
           'varnames':[['U_SE','k']],
           'hdf5_section':all_spines,
           'xunit':'min',
           'yunit':'\%',
           'moltiplier':1000,
           'location':0.5,
           'time_window':[['full',
                          -20,
                          +80]],
           'ylim':[98,162],
           'xlabel':'Time',
           'legend':False,
           'ylabel':'Norm. rel.',
           'numbers':True}
    # ,'bdnf':{'title':'Released BDNF',
    #          'varnames':[['proBDNF','k'],['mBDNF','r'],['PC','b']],
    #          'hdf5_section':all_spines,
    #          'xunit':'min',
    #          'location':0.5,
    #          'time_window':[['full',
    #                         -20,
    #                         +80]],
    #          'xlabel':'Time',
    #          'legend':False,
    #          'thresholds':[spine_point_processes[2]['parameters']['theta_gAMPA']],
    #          'ylabel':'Concentration'}
    # ,'fullbdnf':{'title':'Post synaptic signaling',
    #        'varnames':[['mBDNF','r'],['TrkB','g'],['intracell_signaling','y'],['g_factor','c']],
    #        # 'varnames':[['intracell_signaling','y'],['g_factor','c']],
    #        # 'varnames':[['g_factor','c']],
    #        # 'varnames':[['mBDNF','r'],['TrkB','g'],['g_factor','c']],
    #        'hdf5_section':all_spines,
    #        'xunit':'min',
    #        'location':0.5,
    #        'time_window':[['full',
    #                       -20,
    #                       +80]],
    #        'xlabel':'Time',
    #        # 'ylim':(0,40e-3),
    #        'legend':False,
    #        'ylabel':'Concentration'}
    # ,'trkb':{'title':'Postsynaptic TrkB',
    #        'varnames':[['TrkB','g']],
    #        'hdf5_section':all_spines,
    #        'xunit':'min',
    #        'location':0.5,
    #        'time_window':[['full',
    #                       -20,
    #                       +80]],
    #        'xlabel':'Time',
    #        'legend':False,
    #        'ylabel':'Concentration'}
    ,'gfactor':{'title':'Effective AMPA cond.',
           'varnames':[['g_factor','c']],
           'hdf5_section':all_spines,
           'xunit':'min',
           'yunit':'\%',
           'moltiplier':100,
           'location':0.5,
           'time_window':[['full',
                          -20,
                          +80]],
           'ylim':[98,230],
           'legend':False,
           'xlabel':'Time',
           'ylabel':'Norm. cond.'}
    # ,'Peak_EPSP':{'title':'EPSP Peak',
    #        'varnames':[['v','Blues']],
    #        'hdf5_section':['pyr2005/branch_base'],
    #        'location':0.5,
    #        'time_window':['first_test_post',#'first_induction',
    #                       -60e3*10,
    #                       'end'],
    #        'xunit':'min',
    #        'xlabel':'Time',
    #        'ylabel':'%',
    #        'panel':(4,3,2)}
    ,'syn_eff':{'title':'Synaptic efficacy',
           'varnames':[['U_SE_factor','b'],['g_factor','g']],
           'hdf5_section':['Spine_0/head_0',
                           'Spine_1/head_1',
                           'Spine_2/head_2',
                           'Spine_3/head_3'],
           'location':0.5,
           'time_window':[['first_test_post',#'first_induction',
                          -20e3,
                          'end']],
           'xunit':'min',
           'xlabel':'Time',
           'legend':False,
           'ylabel':'Efficacy',
           'panel':(4,3,5)}
  ,'control':{'title':'NMDA current in control',
           'varnames':[['iampa','b'],['inmda','g']],
           'hdf5_section':['Spine_9/head_9'],
           'location':0.5,
           'time_window':[['second_test_pre',
                          -20,
                          +200]],
           'xunit':'ms',
           'legend':False,
           'xlabel':'Time',
           'ylabel':'Current'}
  ,'post_expression':{'title':'Syn current potentiated',
           'varnames':[['iampa','Blues'],['inmda','Reds']],
           'hdf5_section':['Spine_9/head_9'],
           'location':0.5,
           'time_window':[['first_test_post',
                          -20,
                          +200]],
           'xunit':'ms',
           'legend':False,
           'xlabel':'Time',
           'ylabel':'Current'}
    }

    
protocols = {
    # 'LTP14':{
    #     'BPAP_dep_stimulus_duration':2.5, # ms        
    #     'BPAP_hyp_stimulus_duration':0, # ms
    #     'n_BPAP':4,
    #     'activate_LTP_protocol':True,
    #     'nstim':25,
    #     'repeat_protocol':1,
    #     'color':'r'},
    '1EPSP':{
        'BPAP_dep_stimulus_duration':0, # ms        
        'BPAP_hyp_stimulus_duration':0, # ms        
        'activate_LTP_protocol':True,
        'n_BPAP':0,
        'nstim':1,
        'repeat_protocol':1,
        'color':'#FF4500'}
    # ,'LTP11':{
    #     'BPAP_dep_stimulus_duration':2.5, # ms        
    #     'BPAP_hyp_stimulus_duration':0, # ms        
    #     'n_BPAP':1,
    #     'activate_LTP_protocol':True,
    #     'nstim':70,
    #     'repeat_protocol':1,
    #     'color':'b'}
    # ,'LTP14_RMBLK':{
    #     'BPAP_dep_stimulus_duration':2.5, # ms        
    #     'BPAP_hyp_stimulus_duration':0, # ms
    #     'n_BPAP':4,
    #     'activate_LTP_protocol':True,
    #     'nstim':25,
    #     'Block_RMBLK':True,
    #     'repeat_protocol':1,
    #     'color':'r'}
    # ,'LTP12':{
    #     'BPAP_dep_stimulus_duration':2.5, # ms        
    #     'BPAP_hyp_stimulus_duration':0, # ms        
    #     'n_BPAP':2,
    #     'activate_LTP_protocol':True,
    #     'nstim':50,
    #     'repeat_protocol':1,
    #     'color':'g'}
    # ,'4BPAPs':{
    #     'BPAP_dep_stimulus_duration':2.5, # ms        
    #     'BPAP_hyp_stimulus_duration':0, # ms        
    #     'n_BPAP':4,
    #     'nstim':25,
    #     'activate_LTP_protocol':False,
    #     'color':'r'}
    # ,'2BPAPs':{
    #     'BPAP_dep_stimulus_duration':3, # ms        
    #     'BPAP_hyp_stimulus_duration':0, # ms        
    #     'n_BPAP':2,
    #     'nstim':0,
    #     'activate_LTP_protocol':False,
    #     'color':'r'}
    # ,'1BPAP':{
    #     'BPAP_dep_stimulus_duration':4, # ms        
    #     'BPAP_hyp_stimulus_duration':0, # ms        
    #     'activate_LTP_protocol':False,
    #     'n_BPAP':1,
    #     'nstim':0,
    #     'repeat_protocol':1,
    #     'color':'k'}
          }

print((list(protocols.keys())))
    

# deltaT = 10 ms  = post - pre 
# blue = LTP14
# verde = LTP11
# rossa = solo 4 BPAPs, calcio da VGCC
# nera = solo 1 BPAP, calcio da VGCC
# arancio = solo 1 EPSP, calcio da NMDA
