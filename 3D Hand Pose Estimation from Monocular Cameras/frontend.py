# frontend.py
import requests
import streamlit as st
import plotly.graph_objs as go

st.title("3D Hand Pose Estimation")

if st.button('Capture Hand Pose'):
    try:
        response = requests.get('http://127.0.0.1:5000/hand_landmarks')
        hands = response.json().get('hands', [])
        if hands:
            hand = hands[0]
            x = [point['x'] for point in hand]
            y = [-point['y'] for point in hand]  # invert y for better visualization
            z = [-point['z'] for point in hand]  # invert z to represent depth properly

            fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='markers+lines')])
            fig.update_layout(scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z',
                yaxis=dict(autorange='reversed')
            ))
            st.plotly_chart(fig)
        else:
            st.write("No hand detected. Please try again.")
    except Exception as e:
        st.error(f"Error fetching hand data: {e}")
