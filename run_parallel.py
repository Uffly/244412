# import ipdb
from neuron import h, gui
import numpy as np
from glob import glob as listdir
import os
from branch_setup import *
import h5py as h5
from protocol import *
import sys

def safe_array(seq):
    try:
        return np.array(seq, dtype=float)
    except (ValueError, TypeError):
        # Konwersja obiektów NEURON i wyrównanie list o różnych długościach
        clean = [list(x) if hasattr(x, '__iter__') else [x] for x in seq]
        max_len = max((len(x) for x in clean), default=0)
        return np.array([x + [np.nan] * (max_len - len(x)) for x in clean])


def superrun(xxx_todo_changeme):

    (run_index,delta_t, dep_dur, hyp_dur, n_BPAP, conf_n, activate_LTP,nstim,blk_RMBLK) = xxx_todo_changeme
    global protocol, p , cell, rank
    if p['check']:
        print(('Started simulation %s run %g on CPU %g'%(conf_n, run_index,rank)))

    # print protocol.stimulators['IC_dep'][0][0].delay,protocol.stimulators['IC_dep'][0][0].amp

    for ic_idx,(dc,hc) in enumerate(zip(protocol.stimulators['IC_dep'],protocol.stimulators['IC_hyp'])):
        if ic_idx < p['protocols'][conf_n]['nstim']:
            for dcc,hcc in zip(dc,hc):
                dcc.dur = dep_dur
                hcc.dur = hyp_dur
                hcc.delay = dcc.delay + dcc.dur # ms
            if n_BPAP == 1:
                for i in [1,2,3]:
                    dc[i].dur = 0
                    hc[i].dur = 0
            if n_BPAP == 2:
                for i in [2,3]:
                    dc[i].dur = 0
                    hc[i].dur = 0
        else:
            for i in [0,1,2,3]:
                dc[i].dur = 0
                hc[i].dur = 0
            
    if activate_LTP:
        protocol.stim.number = nstim
        if p['check']:
            print(('Stimulation is %s for %g times.'%(conf_n,nstim))) 
    else:
        protocol.stim.number = 0
        
    if p['check']:
        print(("Running for delta_t = %g"%delta_t))
    protocol.stim.start = p['time_start_induction_stimuli'] + delta_t # ms
    if p['check']:
        print(('Initializing on run %g on CPU %g'%(run_index,rank)))
    if p['override_tstop'] is not None:
        h.tstop = p['override_tstop']
    else:
        h.tstop = protocol.p['tstop']#p['time_on_initialization']+p['time_to_begin_induction'] + 1000
    if p['check']:
        print(('Running for %g ms'%h.tstop))

    # for seg in dend:
    #     mec = getattr(seg,'na3')
    #     mec.gbar = 0
    # for dc in protocol.stimulators['IC_dep']:
    #     for d in dc:
    #         d.amp = 0
    # for dc in protocol.stimulators['IC_hyp']:
    #     for d in dc:
    #         d.amp = 0
        # print conf_n, dc[0].amp, dc[0].dur
    # for s in cell.spines:
    #     print s.head.BDNF.alpha_gAMPA, s.head.BDNF.theta_gAMPA, s.head.BDNF.sigma_gAMPA
    #     print s.parent_sec,s.parent_seg
    #     s.head.AMPA.Pmax = 0
    #     s.head.NMDA.Pmax = 0
    h.init()
    
    if h.tstop > 1e3:
        while h.t < h.tstop:
            h.continuerun(h.t+5e3)
            print((h.t))
            sys.stdout.flush()
    else:
        h.run()
    for s in cell.spines:
        print((s.name, s.head.AMPA.Pmax, s.head.AMPA.g_factor, s.head.AMPA.glut_factor, 'lowindex', cell.MCell_Ran4_lowindex, 'cell highindex', cell.MCell_Ran4_highindex, 'delta t', delta_t))

    store = h5.File(p['data_file']+'_%g.hdf5'%run_index, 'w')
    # print "Opened data file on cpu %g"%rank
    # Group for sim data
    sim_data = store.create_group('Simulation_data')
    conf_data = sim_data.create_group(conf_n)
    # Group for single iteration
    run_iteration = conf_data.create_group('delta_t_%g_%g'%(delta_t,run_index))
    run_iteration.create_dataset('branches indexes',data=cell.seg_indexes)
    run_iteration.create_dataset('branches indexes 2',data=cell.seg_indexes_2)
    run_iteration.create_dataset('branch names',data=[str(ss) for ss in cell.branch_segments])
    run_iteration.create_dataset('spiny branch names',data=[str(ss) for ss in cell.spine_segments])
    run_iteration.create_dataset('delta_t',data=delta_t)
    run_iteration.create_dataset('test_pre_spike_times',
                                data=safe_array(protocol.stimulators['test_pre_spike_times']))
    run_iteration.create_dataset('induction_spikes',
                                data=safe_array(protocol.stimulators['induction_spikes']))
    run_iteration.create_dataset('test_during_spike_times',
                                data=safe_array(protocol.stimulators['test_during_spike_times']))
    run_iteration.create_dataset('test_post_spike_times',
                                data=safe_array(protocol.stimulators['test_post_spike_times']))
    run_iteration.create_dataset('induction_injection_times',
                                data=safe_array(protocol.stimulators['IC_delays']))

    if p['check']:
        for spine_index,spine in enumerate(cell.spines):
            print((conf_n, spine.name, 'delta_t_%g'%delta_t, list(run_iteration.keys())))
    for spine_index,spine in enumerate(cell.spines):
        # Single spine group
        # if spine.name in run_iteration.keys():
        spine_group = run_iteration.create_group(spine.name)
        spine.head.save_records(spine_group,
                                spine_index,
                                write_datasets = True)
        spine.neck.save_records(spine_group,
                                spine_index,
                                write_datasets = True)
    cell.cell.save_records(run_iteration, write_datasets = True)
    tb.dig_dict_save('Parameters',p,store.create_group('Parameters'))
    store.close()
    return 'Completed sim on run %g on CPU %g time %g'%(run_index,rank,h.t)

pc = h.ParallelContext()
rank = int(pc.id())
CVOde = h.cvode
CVOde.active(1)
# h.nrnmainmenu()

p = {}
exec(compile(open('parameters.py').read(), 'parameters.py', 'exec'),p)

# global cell
cell = Spiny_branch(p,rank=rank)
# for s in cell.spines:
#     print s.head.BDNF.alpha_gAMPA, s.head.BDNF.theta_gAMPA, s.head.BDNF.sigma_gAMPA
# global protocol
protocol = stim_protocol(cell, p, rank=rank)


pc.runworker()
print(('Starting %g'%rank))

sim_list = []
if rank == 0:
    # Remove old data files
    ls = listdir(p['data_file']+'_*.hdf5')
    for f in ls:
        if 'pulled' not in f:
            os.remove(f)

    # nnodes = world.size
    run_index = 0
    for conf_n,conf in list(p['protocols'].items()):

        for delta_t in p['time_delta']:

            blk_RMBLK = conf['Block_RMBLK'] if 'Block_RMBLK' in list(conf.keys()) else False
            # print "Submitting jobs", delta_t
            args = [
                run_index,
                delta_t,
                conf['BPAP_dep_stimulus_duration'],
                conf['BPAP_hyp_stimulus_duration'],
                conf['n_BPAP'],
                conf_n,
                conf['activate_LTP_protocol'],
                conf['nstim'],
                blk_RMBLK]
            # print(args)
            sim_list.append(args)
            run_index += 1
            pc.submit(superrun, args)

while pc.working():
    print((pc.pyret()))
pc.done()


