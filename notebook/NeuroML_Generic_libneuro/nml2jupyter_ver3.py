import pylab as plt
import numpy as np
import os
import re
import ipywidgets
import xml.etree.ElementTree as ET

#python helper class for updating NeuroML files and running it from Jupyter Notebook
class nml2jupyter():
    
    def __init__(self, path2source, fname_LEMS):
        
        self.path2source      = path2source
        self.fname_LEMS       = fname_LEMS
        self.filelist         = []
        #self.fname_cellNML    = fname_cellNML
        #self.fname_netNML     = fname_netNML
        #self.fname_NML_output = fname_NML_output
        
    #function to parse NeuroML files
    def parseNML(self):
        
        tree=[]          #for all element trees (including LEMS**.xml)
        #filelist=[]      #for all the filenames included in LEMS simulation file
        
        filename=os.path.join(self.path2source, self.fname_LEMS)
        #tree.append(ET.parse(filename))
        root = ET.parse(filename).getroot()
        
        self.filelist.append(self.fname_LEMS)
        #find all nml files included in the simulation
        for f in root.findall('./{*}*/[@file]'):
            if f.attrib['file'].endswith('.nml'):
                self.filelist.append(f.attrib['file'])
 
        for file in self.filelist:
            filename=os.path.join(self.path2source, file)
            tree.append(ET.parse(filename))
            
        #registering namespace as blank space (some user tag can also be used)
        ET.register_namespace("","http://www.neuroml.org/schema/neuroml2")
        #ns = {"xmlns":"http://www.neuroml.org/schema/neuroml2"}
        
        return tree
    
    def findLevel(self,elem,level):
        if (len(elem.findall('./{*}*'))):
            level+=1
            for subelem in elem.findall('./{*}*'):
                print('\033[0;{}m'.format(30+level) + ' |---'*level + str(subelem.tag.split("}")[-1]) + str(subelem.attrib))
                self.findLevel(subelem,level)
        
    def generateDashboard(self,trees):
       
        out=[]
        for tree in trees:
            out.append(ipywidgets.Output())
            with out[-1]:          #last element of out
                root = tree.getroot()
                self.findLevel(root, -1)                  
        
        tab_nest = ipywidgets.Tab()
        #create tab headers
        idx=0
        for x in out:
            tab_nest.set_title (idx, self.filelist[idx])
            idx+=1    
        
        #add aditional tab for results
        #tab_nest.set_title (idx, 'Result')
        #file = open("nml_result.PNG", "rb")
        #image = file.read()
        #out.append(ipywidgets.Output(layout=ipywidgets.Layout(width='100%',
        #                                   height='auto',
        #                                   max_height='1000px',
        #                                   overflow='hidden scroll',)))
        
        #set content to tabs
        tab_nest.children = out
        ######################################
        
        ######################################
        #display the tab
        display(tab_nest)
        
    #function to update existing NeuroML file based on widget inputs
    def writeNMLinputFile(self,C_m, g_Na, g_K, g_L, E_Na, E_K, E_L, t_0, t_n, delta_t, I_inj_max, I_inj_width, I_inj_trans):
        print('will do later')
        
    #function to plot data generated by NeuroML
    def plotData(self,fname_NML_output):

        #read data file and import columns as array using numpy
        data = np.loadtxt(fname_NML_output)
        t=data[:,0]*1000    #convert to ms
        V=data[:,1]*1000    #convert to mV
        m=data[:,2]
        h=data[:,3]
        n=data[:,4]
        ina=data[:,5]
        ik=data[:,6]
        il=data[:,7]
        i_inj1=data[:,8]*10**9 #convert to nA
        i_inj2=data[:,9]*10**9 #convert to nA

        plt.rcParams['figure.figsize'] = [12, 8]
        plt.rcParams['font.size'] = 15
        plt.rcParams['legend.fontsize'] = 12
        plt.rcParams['legend.loc'] = "upper right"

        fig=plt.figure()

        ax1 = plt.subplot(4,1,1)
        plt.xlim([np.min(t),np.max(t)])  #for all subplots
        plt.title('Hodgkin-Huxley Neuron')
        #i_inj_values = [self.I_inj(t) for t in t]
        plt.plot(t, i_inj1, 'k')
        plt.plot(t, i_inj2, 'b')
        plt.ylabel('$I_{inj}$ (nA)')      

        plt.subplot(4,1,2, sharex = ax1)
        plt.plot(t, ina, 'c', label='$I_{Na}$')
        plt.plot(t, ik, 'y', label='$I_{K}$')
        plt.plot(t, il, 'm', label='$I_{L}$')
        plt.ylabel('Current')
        plt.legend()

        plt.subplot(4,1,3, sharex = ax1)
        plt.plot(t, m, 'r', label='m')
        plt.plot(t, h, 'g', label='h')
        plt.plot(t, n, 'b', label='n')
        plt.ylabel('Gating Value')
        plt.legend()

        plt.subplot(4,1,4, sharex = ax1)
        plt.plot(t, V, 'k')
        plt.ylabel('V (mV)')
        plt.xlabel('t (ms)')
        #plt.ylim(-1, 40)

        plt.tight_layout()
        plt.show()
#end of class