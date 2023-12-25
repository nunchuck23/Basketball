import math
import streamviz
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# CONSTANTS
g = 32.174;  # gravity acceleration (ft/s^2)
H = 10.0;      # basket height (ft)
X = 15.0;      # free throw line to basket distance (ft)
#-------------------------------------------------------------------

st.title('The Perfect Basketball Free Throw')

st.write('Want to perfect your free throw? Use this simple app to calculate the best release angle and velocity that will result in a successful free throw. All you need to do is enter your height in feet and inches and the app will do the rest. **Good luck!**')

st.subheader('Overview')
st.write('The free throw line from which the player takes the shot is 15 feet from the backboard. Once the player takes the shot, the basketball follows a curved path towards the basket. This is referred to as projectile motion in physics. ')

st.write('The two important factors the player controls are the angle at which the ball is '
         'released (**release angle**) and the speed with which the ball is released (**release '
         'velocity**). The right release angle and release velocity are essential for a successful '
         'free throw.')

# INPUTS
with st.sidebar:
    st.header("Enter your Height Information")
    st.write('Use the sliders below to enter your height in feet and inches. You will see calcuations for the release angle and release velocity necessary for a successful free throw.')
    height_ft = st.slider("Your height in feet", 4,7,5,1)
    height_in = st.slider("Your height in inches", 0,12,6,1)

    st.subheader('created by Neev Goudar')

#-------------------------------------------------------------------

# CALCULATIONS
h1 = height_ft + height_in/12
h2 = H - h1

# Release Angle
num_angle = h2 + math.sqrt(h2**2 + X**2)
release_angle_rad = np.arctan(num_angle/X)
release_angle_deg  = math.degrees(release_angle_rad)

# Initial Velocity
release_velocity = math.sqrt(g*num_angle)

# Time to Basket
time_basket = X/(release_velocity*np.cos(release_angle_rad))

# Max Height Post Release
max_height = (release_velocity**2*np.sin(release_angle_rad)**2)/(2*g)

# Trajectory of the Basketball
xdistance = np.linspace(0, 15, 25)
comp1 = g*(xdistance**2)
comp2 = 2*(release_velocity*np.cos(release_angle_rad))**2
ydistance = h1 + xdistance*np.tan(release_angle_rad) - comp1/comp2
motion_data = pd.DataFrame(ydistance, xdistance)
#-------------------------------------------------------------------------

#Output Visualization (Guages)
st.subheader('Release Angle')
st.write('Once the ball is released, gravity acts downward and influences the path of the ball as it approaches the basket. Shooting the ball at the correct angle is important because that will enable the ball to travel the 15 feet distance and land in the basket. The release angle depends on the height of the player and taller players need a smaller release angle for a successful free throw.')
#st.latex(r'''\theta=\tan^{-1}\left\{\frac{h+\sqrt{h^2+x^2}}{x}\right\}''')
streamviz.gauge(release_angle_deg, gSize="LRG", gTitle="Release Angle (degrees)", arTop=90)

st.subheader('Release Velocity')
st.write('Having the correct release velocity (combined with the correct Release Angle) is essential for a successful free throw. Taller players need lower release velocities for successful free throws.')
streamviz.gauge(release_velocity, gSize="LRG", gTitle="Release Velocity (feet/second)", arTop=90)

st.subheader('Time to Basket')
st.write('Using the equations of projectile motion, we can calculate the time it takes the ball to reach the basket from the free throw line. When a player 5 feet tall shoots a free throw, it takes 0.991 seconds for the ball to reach the basket compared to 0.975 seconds for a 7 feet player. For most players it takes less than 1 second for the ball to make it to the basket from the free throw line.')
streamviz.gauge(time_basket, gSize="LRG", gTitle="Time to basket (seconds)",arTop=3)

st.subheader('Maximum Height after Release')
st.write('The maximum height a ball reaches while traveling from the free throw line to the basket depends on the release velocity and the release angle. For a 5-feet tall player, the maximum height is 6.85 feet while that for a taller 7-feet player is 5.47 feet.')
streamviz.gauge(max_height, gSize="LRG", gTitle="Max Height after Release (feet)",arTop=10)

st.subheader('Journey of the Basketball')
st.write('We can predict the path the ball will take after being released from the free throw line. The graph below shows the path of a basketball when shot at the right release angle and release velocity by a player taking the free throw.')

fig = px.scatter(motion_data)
fig.update_layout(xaxis_title="Horizontal Distance (feet)",
                  yaxis_title="Height of Basketball (feet)",
                  showlegend=False,
                  font_family="corbel",
                  )
fig.update_traces(marker=dict(size=10, symbol="circle"))

st.plotly_chart(fig, theme="streamlit", use_container_width=True)