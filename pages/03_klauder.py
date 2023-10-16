import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert
import math
import cmath
pi = math.pi

def ORMSBY(f1=5., f2=10., f3=40., f4=45., length=0.512, dt=0.001):
    p = np.pi
    t = np.linspace(-length/2, (length-dt)/2, int(length/dt))

    y = p*f4**2 * (np.sinc(f4*t))**2/(f4-f3) - p*f3**2 * (np.sinc(f3*t))**2/(f4-f3) - \
        p*f2**2 * (np.sinc(f2*t))**2/(f2-f1) - p*f1**2 * (np.sinc(f1*t))**2/(f2-f1)

    y = y / np.amax(abs(y))

    return t, y

def Klauder(T=6., f1=10., f2=40., length=0.512, dt=0.001):
    k = (f2 - f1)/T
    f0 = (f2 + f1)/2
    i = complex(0, 1)
    p = np.pi
    t = np.linspace(-length/2, (length-dt)/2, int(length/dt))
    #y = t**2

    a = np.exp(2*pi*i*f0*t)
    y = (a * np.sin(pi*k*t*(T - t)) / (pi*k*t)).real

    return t, y

st.title('Klauder wavelet')
#st.text('Change wavlet parameters and rotate phase with sliders.')

#st.subheader("f(t) = ...")
st.latex(r'''
    Klauder(t) = Re (\frac{sin(\pi kt(T-t))}{\pi kt} e^ {2 \pi if_0 t}),
    where \; k = \frac{f_2 - f_l}{T}, fo = \frac{f_2 + f_l}{2}, i = \sqrt{-1}
    ''')
col1, col2 = st.beta_columns((1,1))
with col1:
    f1 = st.slider('Select terminal low frequency (Hz)', value=10., min_value=1., max_value=240.)

with col2:
    f2 = st.slider('Select terminal high frequency (Hz)', value=40., min_value=1., max_value=240.)
    
T = st.slider('Duration of input signal (s)', value=7., min_value=5., max_value=10.)

st.write(f1, " - ", f2, "Hz, T =", T, " s")

#f1 = 5
#f2 = 10

t, y = Klauder(T, f1, f2, 0.512, 0.001)

phi = st.slider('Phase rotation angle (deg)', value=0.0, min_value=0., max_value=360.)
#st.write("Phi = ", phi)

#str1 = str(int(f)) + "Hz, Phase: " + str(int(phi))
str1 = "Klauder " + str(int(f1 + 0.5)) + " - " + str(int(f2 + 0.5))  + " Hz, Phase rotation " + str(int(phi+0.5)) + "°"
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
