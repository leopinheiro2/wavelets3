import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert
import math
pi = math.pi

pi = math.pi

def ORMSBY(f1=5., f2=10., f3=40., f4=45., length=0.512, dt=0.001):
    p = np.pi
    t = np.linspace(-length/2, (length-dt)/2, int(length/dt))

    # y = p*p*f4**2 * (np.sinc(f4*t))**2/(p*f4-p*f3) - p*p*f3**2 * (np.sinc(f3*t))**2/(p*f4-p*f3) - \
    #     p*p*f2**2 * (np.sinc(f2*t))**2/(p*f2-p*f1) - p*p*f1**2 * (np.sinc(f1*t))**2/(p*f2-p*f1)
    y = p*f4**2 * (np.sinc(f4*t))**2/(f4-f3) - p*f3**2 * (np.sinc(f3*t))**2/(f4-f3) - \
        p*f2**2 * (np.sinc(f2*t))**2/(f2-f1) - p*f1**2 * (np.sinc(f1*t))**2/(f2-f1)

    y = y / np.amax(abs(y))

    return t, y

st.title('ORMSBY wavelet')

st.latex(r'''
    Ormsby(t) = \frac{\pi f_4^2 sinc^2 (\pi f_4 t) - \pi f_3^2 sinc^2 (\pi f_3 t)}{f_4 - f_3}  
    - \frac{\pi f_2^2 sinc^2 (\pi f_2 t) - \pi f_1^2 sinc^2 (\pi f_1 t)}{f_2 - f_1}
    ''') 

col1, col2 = st.columns(2)
with col1:
    f1 = st.slider('Select frequency f1 (Hz)', value=5., min_value=1., max_value=240., step=1., format="%.1f")
    f3 = st.slider('Select frequency f3 (Hz)', value=60., min_value=1., max_value=240., step=1., format="%.1f")
    phi = st.slider('Phase rotation angle (deg)', value=0.0, min_value=0., max_value=360., step=45., format="%.1f")

with col2:
    f2 = st.slider('Select frequency f2 (Hz)', value=10., min_value=1., max_value=240., step=1., format="%.1f")
    f4 = st.slider('Select frequency f4 (Hz)', value=70., min_value=1., max_value=240., step=1., format="%.1f")
    envelope = st.checkbox('Display wavelet envelope')
#st.write(f1, " - ", f2, " - ", f3, " - ", f4)

#st.write("Phi = ", phi)
str1 = "ORMSBY " + str(int(f1 + 0.5)) + " - " + str(int(f2 + 0.5))  + " - " + str(int(f3 + 0.5)) + " - " + str(int(f4 + 0.5)) + " Hz, Phase " + str(int(phi+0.5)) + "°"
st.subheader(str1)

t, y = ORMSBY(f1, f2, f3, f4, 0.512, 0.001)

z= hilbert(y) #form the analytical signal
inst_amplitude = np.abs(z) #envelope extraction
#inst_amplitude = np.sqrt(np.square(z.real) + np.square(z.imag)) #envelope extraction


inst_phase = np.unwrap(np.angle(z))#inst phase

phase = phi * pi/180
x_rotate = math.cos(phase)*z.real - math.sin(phase)*z.imag
if envelope:
    chart_data = pd.DataFrame(
       {
           "t": t,
           #"y": y
           "y": x_rotate,
           "y2": inst_amplitude,
           "y3": -1*inst_amplitude
       }
    )

    st.line_chart(chart_data, x="t", y=["y", "y2", "y3"], color=["#d62728", "#1f77b4", "#1f77b4"])

else:
    chart_data = pd.DataFrame(
       {
           "t": t,
           "y": x_rotate
       }
    )

    st.line_chart(chart_data, x="t", y=["y"], color=["#d62728"])

url1 = "https://www.rmseismic.com/lasviewer.html"
st.write("More geophysical web apps: [link](%s)" % url1)
