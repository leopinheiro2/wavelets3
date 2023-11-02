import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert
import math

st.set_page_config(layout="wide")

pi = math.pi

st.title('Ricker wavelet with synthetuic trace')
st.text('This is a web app to display wavelets - select parameters.')
#url = "https://rmseismic.com"
#st.write("RM Seismic Software [rmseismic.com](%s)" % url)

def ricker(f, length=0.512, dt=0.001):
    t = np.linspace(-length/2, (length-dt)/2, int(length/dt))
    y = (1.-2.*(np.pi**2)*(f**2)*(t**2))*np.exp(-(np.pi**2)*(f**2)*(t**2))
    return t, y

col1, col2, col3 = st.columns(3)
with col1:
    
    st.latex(r'''
    Ricker(t) = (1-2\pi^2 f^2 t^2)e^{-\pi^2 f^2 t^2}
    ''') 
    f = st.slider('Select frequency from [1, 240] Hz', value=30., min_value=1., max_value=240., step=1., format="%.1f")

t, y = ricker (f)

with col1:
    phi = st.slider('Phase rotation angle (deg)', value=0.0, min_value=0., max_value=360., step=45., format="%.1f")
    envelope = st.checkbox('Envelope')

    str1 = "Peak frequency = " + str(int(f + 0.5)) + " Hz, Phase rotation = " + str(int(phi+0.5)) + "°"
    st.subheader(str1)
    
    z= hilbert(y) #form the analytical signal
    inst_amplitude = np.abs(z) #envelope extraction
    inst_phase = np.unwrap(np.angle(z))#inst phase
    
    phase = phi * pi/180
    x_rotate = math.cos(phase)*z.real - math.sin(phase)*z.imag

with col1:
    if envelope:
        chart_data = pd.DataFrame(
           {
               "t": t,
               #"y": y
               "y": x_rotate,
               "y_env2": inst_amplitude,
               "y_env3": -1*inst_amplitude
           }
        )
        st.line_chart(chart_data, x="t", y=["y", "y_env2", "y_env3"], color=["#d62728", "#D3D3D3", "#D3D3D3"], width=450, height=450)
    
    else:
        chart_data = pd.DataFrame(
           {
               "t": t,
               "y": x_rotate
           }
        )

    st.line_chart(chart_data, x="t", y=["y"], color=["#d62728"])

x1 = np.arange(0, 2000., 0.5)
y1 = np.square(x1) -10 * x1
y2 = np.cos(0.02*x1)

fig1, ax1 = plt.figure(1)
fig1.title('Reflectivity')

plt.subplot(111)
plt.plot(y1, x1)

fig2, ax2 = plt.figure(2)
fig1.title('Convolved')

plt.subplot(111)
plt.plot(y2, x1)

with col2:
    st.pyplot(fig1) 

with col3:
    st.pyplot(fig2)



url1 = "https://www.rmseismic.com/lasviewer.html"
st.write("More geophysical web apps: [link](%s)" % url1)
