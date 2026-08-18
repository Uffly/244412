import h5py as h5
import toolbox as tb
from glob import glob as listdir

p = {}
exec(compile(open('parameters.py').read(), 'parameters.py', 'exec'),p)

store = h5.File(p['data_file']+'_pulled.hdf5', 'w')
# tb.dig_dict_save('Parameters',p,store.create_group('Parameters'))
fd = store.require_group('Simulation_data')

ls = listdir(p['data_file']+'_*.hdf5')

for idx,f in enumerate(ls):
    if 'pulled' not in f:
        fs = h5.File(f, 'r')
        print(idx)
        if not idx:
            fs.copy('Parameters', store)
        for gs_n,gs in list(fs['Simulation_data'].items()):
            fdd = fd.require_group(gs_n)
            print((gs_n,list(gs.keys())))
            for gss_n, gss in list(gs.items()):
                fdd[gss_n] = gs[gss_n][:]
        fs.close()
store.close()
