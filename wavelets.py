import streamlit as st
from streamlit.components.v1 import html

st.title('Seismic Wavelets')
st.subheader('Alex Falkovskiy')
url = "https://www.rmseismic.com"
st.write("RM Seismic Software [rmseismic.com](%s)" % url)
st.write('The purpose of this web app is to illustrate how basic seismic wavelets change with the change of parameters.')
st.write('It is based on a paper by Harold Ryan: Ricker, Ormsby; Klander, Bntterworth - A Choice of wavelets, publised in CSEG Recorder, September 1994.')
st.write('A list of wavelets you can display and vary parameters:')
st.write('**Ricker, Ormsby, Klauder** - use left side menu to select a wavelet and sliders to change parameters.')

url1 = "https://www.rmseismic.com/lasviewer.html"
st.write("More geophysical web apps: [link](%s)" % url1)
st.write("A.F., Sep 2023")

google_js = """
<!-- Google tag (gtag.js) --><script async src="https://www.googletagmanager.com/gtag/js?id=G-VBX865DFKL"></script><script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-VBX865DFKL');
</script>
"""

#html1 = f"{google_js}"
 
