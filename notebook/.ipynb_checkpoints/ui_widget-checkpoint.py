import ipywidgets

header_capacitance = ipywidgets.HTML(value=f"<b><font color='blue'>Membrane Capacitance, uF/cm^2</b>")
header_conductance = ipywidgets.HTML(value=f"<b><font color='blue'>Maximum Conductances, mS/cm^2</b>")
header_potential   = ipywidgets.HTML(value=f"<b><font color='blue'>Nernst Reverasal Potentials, mV</b>")
slider_capacitance = ipywidgets.FloatSlider(value=1,min=0,max=3,step=0.1,description='Capacitance',readout_format='.1f')
slider_cond_Na     = ipywidgets.FloatSlider(value=120,min=80,max=160,step=0.1,description='Sodium',readout_format='.1f')
slider_cond_K      = ipywidgets.FloatSlider(value=36,min=0,max=80,step=0.1,description='Potassium',readout_format='.1f')
slider_cond_L      = ipywidgets.FloatSlider(value=0.3,min=0,max=1,step=0.1,description='Leak',readout_format='.1f')
slider_pot_Na      = ipywidgets.FloatSlider(value=50,min=-100,max=100,step=0.1,description='Sodium',readout_format='.1f')
slider_pot_K       = ipywidgets.FloatSlider(value=-77,min=-100,max=100,step=0.1,description='Potassium',readout_format='.1f')
slider_pot_L       = ipywidgets.FloatSlider(value=-54.387,min=-100,max=100,step=0.1,description='Leak',readout_format='.1f')

h1=ipywidgets.HBox([header_capacitance])
h2=ipywidgets.HBox([slider_capacitance])
h3=ipywidgets.HBox([header_conductance])
h4=ipywidgets.HBox([slider_cond_Na,slider_cond_K,slider_cond_L])
h5=ipywidgets.HBox([header_potential])
h6=ipywidgets.HBox([slider_pot_Na,slider_pot_K,slider_pot_L])
v1=ipywidgets.VBox([h1,h2,h3,h4,h5,h6])