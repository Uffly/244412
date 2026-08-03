"""
Wrapper classes to make working with NEURON easier.

Author: Andrew P. Davison, UNIC, CNRS
"""

nu__version__ = "0.3.0"

from neuron import nrn, h, hclass
import h5py as h5
import numpy as np
from functools import reduce

h.load_file('stdrun.hoc')

PROXIMAL = 0
DISTAL = 1

class Mechanism(object):
    """
    Examples:
    >>> leak = Mechanism('pas', {'e': -65, 'g': 0.0002})
    >>> hh = Mechanism('hh')
    """
    def __init__(self, name, **parameters):
        self.name = name
        self.parameters = parameters

    def insert_into(self, section):
        section.insert(self.name)
        for name, value in list(self.parameters.items()):
            for segment in section:
                mech = getattr(segment, self.name)
                setattr(mech, name, value)


class Section(nrn.Section):
    """
    Examples:
    >>> soma = Section(L=30, diam=30, mechanisms=[hh, leak])
    >>> apical = Section(L=600, diam=2, nseg=5, mechanisms=[leak],
    ...                  parent=soma, connection_point=DISTAL)
    """
    
    def __init__(self, name, L, diam, nseg=1, Ra=100, cm=1,
                 mechanisms=[], parent=None,
                 connection_point=DISTAL,
                 point_processes = [],
                 records=[]):
        nrn.Section.__init__(self)
        # Set human readable name
        self.Name = name
        # set geometry
        self.L = L
        self.diam = diam
        self.nseg = nseg
        # set cable properties
        self.Ra = Ra
        self.cm = cm
        # connect to parent section
        if parent:
            self.connect(parent, connection_point, PROXIMAL)
        # add ion channels
        for mechanism in mechanisms:
            mechanism.insert_into(self)
        # add point processes
        for pp in point_processes:
            self.add_pointprocesses(pp['label'], pp['type'], locations=pp['locations'], parameters=pp['parameters'])
        # record variables
        self.records = {}
        self.records['time'] = {'val':h.Vector(),'unit':'ms'}
        self.records['time']['val'].record(h._ref_t, sec = self)

        for r in records:
            self.records['%s_%g'%(r['variable'],r['location'])] = {
                'unit':r['unit']}
            local_rec = self.records['%s_%g'%(r['variable'],r['location'])]
            if 'point_process' in list(r.keys()):
                local_rec['val'] = self.record_variable(r['variable'],
                                                           location=r['location'],
                                                           point_process = r['point_process'])
            else:
                local_rec['val'] = self.record_variable(r['variable'],
                                                           location=r['location'])

                
    def add_pointprocesses(self, label, type, locations=[0.5], parameters={}):
        if hasattr(self, label):
            raise Exception("Can't overwrite synapse labels (to keep things simple)")
        synapse_group = []
        for location in locations:
            synapse = getattr(h, type)(location, sec=self)
            for name, value in list(parameters.items()):
                setattr(synapse, name, value)
            synapse_group.append(synapse)
        if len(synapse_group) == 1:
            synapse_group = synapse_group[0]
        setattr(self, label, synapse_group)

    def add_synapses(self, label, type, locations=[0.5], **parameters):
        if hasattr(self, label):
            raise Exception("Can't overwrite synapse labels (to keep things simple)")
        synapse_group = []
        for location in locations:
            synapse = getattr(h, type)(location, sec=self)
            for name, value in list(parameters.items()):
                setattr(synapse, name, value)
            synapse_group.append(synapse)
        if len(synapse_group) == 1:
            synapse_group = synapse_group[0]
        setattr(self, label, synapse_group)
    add_synapse = add_synapses  # for backwards compatibility

    def plot(self,
             variable,
             type_mec='mech',
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
        colors = {'r':2,'k':1,'g':4,'b':3,'o':5,'mr':7,'m':9,'y':8,
                  '1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}
        color = colors[str(color)]
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
        if 'mech' in type_mec:
            if type(variable) == type([]):
                for var in variable:
                    print((self.name(), '%s(%g)' % (var, location)))
                    self.push()
                    if h.ismembrane(var):
                        spine_area = h.area(0.5)
                        graph.addvar(var,
                                      'ica_%s(%g)' % (var,
                                                      location),
                                      color, line, sec=self)
                        color += 1
                    h.pop_section()
            else:
                graph.addvar(variable, '%s(%g)' % (variable, location),
                            color, line, sec=self)
        if 'pp' in type_mec:
            graph.addvar(label,
                         getattr(getattr(self,variable[0]),
                                 '_ref_'+variable[1]),
                         color, line, sec=self)
        graph.flush()            
        return graph

    def record_spikes(self, threshold=-30):
        self.spiketimes = h.Vector()
        self.spikecount = h.APCount(0.5, sec=self)
        self.spikecount.thresh = threshold
        self.spikecount.record(self.spiketimes)

    def record_variable(self, variable, location=0.5, point_process=None):
        v = h.Vector()
        if point_process is not None:
            eval('v.record(getattr(self,"%s")._ref_%s, sec = self)'%(point_process,variable))
        else:
            eval('v.record(self(%g)._ref_%s, sec = self)'%(location,variable))
        return v

    def save_records(self, store, index = None, write_datasets = True):
        if index is not None:
            g = store.create_group('%s_%g'%(self.Name, index))
        else:
            g = store.create_group(self.Name)

        for r_n,r in list(self.records.items()):
            r_g = g.create_group(r_n)
            r_u = r_g.create_dataset('Unit', data = np.string_(r['unit']))
            if write_datasets:
                data = np.array(r['val'])
                data_length = data.shape[0]
                r_v = r_g.create_dataset('Data',
                                         data = data,
                                         compression="gzip",
                                         compression_opts=9,
                                         chunks=(min(100,data_length),)
                                         )
            else:
                r_v = r_g.create_dataset('Data',
                                         (1e5,),
                                         dtype = 'float',
                                         compression="gzip")#,
                                         #compression_opts=9)
                                         #chunks=(100,))

    def store_records(self, section_group, index = None):
        # dset = section_group['%s_%g'%(self.Name, index)]['Data']
        if index is not None:
            dgroup = section_group['%s_%g'%(self.Name, index)]
        else:
            dgroup = section_group[self.Name]

        print((list(dgroup.keys())))
        for r_n,r in list(self.records.items()):
            print((dgroup[r_n]['Data']))
            data = np.array(r['val'])
            print((data.shape))
            # dgroup[r_n]['Data'][:] = 
            # dgroup[r_n]['Data'].resize((500,))
            # print dgroup[r_n]['Data']

    def balance_currents(self,Vrest):
        h.v_init = Vrest
        h.init()

        # Balance ion currents with leak at Vrest by changing leak Erev
        for seg in self:
            current = 0
            if hasattr(seg,'ica'):
                current += seg.ica
            if hasattr(seg,'ina'):
                current += seg.ina
            if hasattr(seg,'ik'):
                current += seg.ik
            seg.e_pas = seg.v + current / seg.g_pas

def alias(attribute_path):
    """
    Returns a new property, mapping an attribute nested in an object hierarchy
    to a simpler name

    For example, suppose that an object of class A has an attribute b which
    itself has an attribute c which itself has an attribute d. Then placing
      e = alias('b.c.d')
    in the class definition of A makes A.e an alias for A.b.c.d
    """
    parts = attribute_path.split('.')
    attr_name = parts[-1]
    attr_path = parts[:-1]
    def set(self, value):
        obj = reduce(getattr, [self] + attr_path)
        setattr(obj, attr_name, value)
    def get(self):
        obj = reduce(getattr, [self] + attr_path)
        return getattr(obj, attr_name)
    return property(fset=set, fget=get)


def uniform_property(section_list, attribute_path):
    """
    Define a property that will have a uniform value across a list of sections.
    
    For example, suppose we define a neuron model as a class A, which contains
    three compartments: soma, dendrite and axon. Then placing
    
        gnabar = uniform_property(["soma", "axon"], "hh.gnabar")
    
    in the class definition of A means that setting a.gnabar (where a is an
    instance of A) will set the value of hh.gnabar in both the soma and axon, i.e.

        a.gnabar = 0.01
        
    is equivalent to:
    
        for sec in [a.soma, a.axon]:
            for seg in sec:
                seg.hh.gnabar = 0.01

    """
    parts = attribute_path.split('.')
    attr_name = parts[-1]
    attr_path = parts[:-1]
    def set(self, value):
        for sec_name in section_list:
            sec = getattr(self, sec_name)
            for seg in sec:
                obj = reduce(getattr, [seg] + attr_path)
                setattr(obj, attr_name, value)
    def get(self):
        sec = getattr(self, section_list[0])
        obj = reduce(getattr, [sec(0.5)] + attr_path)
        return getattr(obj, attr_name)
    return property(fset=set, fget=get)



if __name__ == "__main__":
    
    class SimpleNeuron(object):
    
        def __init__(self):
            # define ion channel parameters
            leak = Mechanism('pas', e=-65, g=0.0002)
            hh = Mechanism('hh')
            # create cable sections
            self.soma = Section(L=30, diam=30, mechanisms=[hh])
            self.apical = Section(L=600, diam=2, nseg=5, mechanisms=[leak], parent=self.soma,
                                  connection_point=DISTAL)
            self.basilar = Section(L=600, diam=2, nseg=5, mechanisms=[leak], parent=self.soma,
                                   connection_point=0.5)
            self.axon = Section(L=1000, diam=1, nseg=37, mechanisms=[hh],
                                connection_point=0)
            # synaptic input
            self.soma.add_synapses('syn', 'AlphaSynapse', onset=0.5, gmax=0.05, e=0)
    
        gnabar = uniform_property(["soma", "axon"], "hh.gnabar")
        gkbar = uniform_property(["soma", "axon"], "hh.gkbar")
    
    neuron = SimpleNeuron()
    neuron.soma.plot('v')
    neuron.apical.plot('v')
    
    neuron.gnabar = 0.15
    assert neuron.soma(0.5).hh.gnabar == 0.15
    
    h.dt = 0.025
    v_init = -65
    tstop = 5
    h.finitialize(v_init)
    h.run()
