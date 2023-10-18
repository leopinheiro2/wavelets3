import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert
import math
pi = math.pi

st.title('Ricker wavelet')
st.text('This is a web app to display wavelets - select parameters.')
#url = "https://rmseismic.com"
#st.write("RM Seismic Software [rmseismic.com](%s)" % url)

st.latex(r'''
    Ricker(t) = (1-2\pi^2 f^2 t^2)e^{-\pi^2 f^2 t^2}
    ''') 

def ricker(f, length=0.512, dt=0.001):
    t = np.linspace(-length/2, (length-dt)/2, int(length/dt))
    y = (1.-2.*(np.pi**2)*(f**2)*(t**2))*np.exp(-(np.pi**2)*(f**2)*(t**2))
    return t, y

col1, col2 = st.columns(2)
with col1:
    f = st.slider('Select frequency from [1, 240] Hz', value=30., min_value=1., max_value=240.)

t, y = ricker (f)

with col2:
    phi = st.slider('Phase rotation angle (deg)', value=0.0, min_value=0., max_value=360., step=45., format="%.1f")
#st.write("Phi = ", phi)
    envelope = st.checkbox('Envelope')

#str1 = str(int(f)) + "Hz, Phase: " + str(int(phi))
str1 = "Peak frequency = " + str(int(f + 0.5)) + " Hz, Phase rotation = " + str(int(phi+0.5)) + "°"
st.subheader(str1)

z= hilbert(y) #form the analytical signal
inst_amplitude = np.abs(z) #envelope extraction
inst_phase = np.unwrap(np.angle(z))#inst phase

phase = phi * pi/180
x_rotate = math.cos(phase)*z.real - math.sin(phase)*z.imag

chart_data = pd.DataFrame(
   {
       "t": t,
       #"y": y
       "y": x_rotate
   }
)

st.line_chart(chart_data, x="t", y="y")

url1 = "https://www.rmseismic.com/lasviewer.html"
st.write("More geophysical web apps: [link](%s)" % url1)
