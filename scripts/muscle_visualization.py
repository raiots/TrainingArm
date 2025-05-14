import streamlit as st
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Set page title
st.set_page_config(page_title="Muscle Activation Visualization", layout="wide")
st.title("Muscle Activation Data Visualization")

# Load data
@st.cache_data
def load_data():
    with open('data/muscle_activation_data.json', 'r') as f:
        return json.load(f)

try:
    data = load_data()
    muscle_names = data['muscle_names']
    trajectories = data['trajectories']
except Exception as e:
    st.error(f"Unable to load data file: {e}")
    st.stop()

# Create sidebar for muscle selection
st.sidebar.header("Select Muscles to Display")
selected_muscles = st.sidebar.multiselect(
    "Choose muscles",
    options=muscle_names,
    default=muscle_names[:5]  # Default to first 5 muscles
)

if not selected_muscles:
    st.warning("Please select at least one muscle to display")
    st.stop()

# Create 3D plot
fig = plt.figure(figsize=(8, 5))  # Further reduced figure size
ax = fig.add_subplot(111, projection='3d')

# Add trajectories for each selected muscle
for i, muscle_name in enumerate(selected_muscles):
    muscle_idx = muscle_names.index(muscle_name)
    # Get activation data for this muscle
    steps = []
    activations = []
    for traj in trajectories:
        steps.append(traj['step'])
        activations.append(traj['muscle_activation'][muscle_idx])
    
    # Create y-axis offset with fixed interval
    y_offset = i * 0.2
    
    # Plot 3D curve
    ax.plot(steps, [y_offset] * len(steps), activations, 
            label=muscle_name, linewidth=2)
    
    # Create fill effect (using polygon)
    verts = [(steps[0], y_offset, 0)]
    verts.extend([(s, y_offset, a) for s, a in zip(steps, activations)])
    verts.append((steps[-1], y_offset, 0))
    verts = [verts]
    
    # Add filled polygon
    ax.add_collection3d(Poly3DCollection(verts, 
                                       alpha=0.3,
                                       facecolor=plt.gca().lines[-1].get_color()))

# Update layout
ax.set_title("Muscle Activation Over Time")
ax.set_xlabel("Steps")
ax.set_ylabel("Muscles")
ax.set_zlabel("Activation")

# Set y-axis ticks
ax.set_yticks([i * 0.2 for i in range(len(selected_muscles))])
ax.set_yticklabels(selected_muscles)

# Adjust view angle
ax.view_init(elev=25, azim=115)

# Add legend
ax.legend(loc='upper right')

# Set axis limits
ax.set_xlim(min(steps), max(steps))
ax.set_ylim(-0.2, (len(selected_muscles) - 1) * 0.2 + 0.2)
ax.set_zlim(0, 1)

# Adjust axis direction
ax.invert_xaxis()  # Invert x-axis to show steps increasing from left to right

# Display plot
st.pyplot(fig, use_container_width=False)  # Added use_container_width=False to prevent automatic scaling

# Add data statistics
st.subheader("Data Statistics")
st.write(f"Total number of muscles: {len(muscle_names)}")
st.write(f"Currently selected muscles: {len(selected_muscles)}")
st.write(f"Total number of steps: {len(trajectories)}")

# Add instructions
st.markdown("""
### Instructions
- Select muscles to display from the sidebar
- Multiple muscles can be displayed simultaneously
- The plot shows muscle activation values over time
- Each muscle's data is shown with a different color and fill effect
""") 