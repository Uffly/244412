import h5py as h5
import toolbox as tb
from glob import glob as listdir

p = {}
exec(compile(open('parameters.py').read(), 'parameters.py', 'exec'),p)

store = h5.File(p['data_file']+'_pulled.hdf5', 'w')
# tb.dig_dict_save('Parameters',p,store.create_group('Parameters'))
fd = store.require_group('Simulation_data')

ls = listdir(p['data_file']+'_*.hdf5')

for idx, f in enumerate(ls):
    if 'pulled' not in f:
        fs = h5.File(f, 'r')
        print(idx)
        if not idx:
            fs.copy('Parameters', store)
        for gs_n in list(fs['Simulation_data'].keys()):
            fdd = fd.require_group(gs_n)
            gs = fs['Simulation_data'][gs_n]
            print((gs_n, list(gs.keys())))
            for gss_n in list(gs.keys()):
                if gss_n not in fdd:
                    fs.copy(f'Simulation_data/{gs_n}/{gss_n}', fdd)
        fs.close()
store.close()
