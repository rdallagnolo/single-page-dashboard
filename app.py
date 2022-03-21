import streamlit as st
import streamlit_authenticator as stauth
from multiapp import MultiApp
from apps import home, Ops001, Ops0011, Ops0012, Ops004, Fin008
from PIL import Image

image = Image.open('images/grameen-logo.jpg')
app = MultiApp()

st.image(image)

# authenticator
names = ['Grameen America','Nina Simone','Bessie Smith']
usernames = ['gamerica','nsimone','bsmith']
passwords = ['123','456','789']

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
    'stauth','1234567890',cookie_expiry_days=0)

name, authentication_status, username = authenticator.login('Login','main')


if authentication_status:
    st.write('Welcome *%s*' % (name))
    st.markdown("<h2 style='text-align: center; color: #55D0CE '>Please select the dashboard</h2>", unsafe_allow_html=True)
    # Add dashboard apps here
    app.add_app("Home", home.app)
    app.add_app("Ops.001 Branch Daily Update", Ops001.app)
    app.add_app("Ops.001-1 Area and Branch Wise Daily Updates", Ops0011.app)
    app.add_app("Ops.001-2 Daily Email Report to CEO", Ops0012.app)
    app.add_app("Ops.004 Center Discipline Report", Ops004.app)
    app.add_app("Fin.008 Repay and Present by Center", Fin008.app)
# The main app
    app.run()
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
