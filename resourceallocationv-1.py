import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define a function to allocate resources
def allocate_resources(demand, available_resources):
    allocation = {}
    remaining_demand = demand.copy()
    
    for resource, available in available_resources.items():
        if resource in remaining_demand:
            # Allocate as much as possible based on available resources
            allocation[resource] = min(remaining_demand[resource], available)
            remaining_demand[resource] -= allocation[resource]
        
        # If there's remaining demand, we can't fulfill it
        if remaining_demand.get(resource, 0) > 0:
            allocation[resource] = allocation.get(resource, 0) + remaining_demand[resource]
            remaining_demand[resource] = 0
    
    return allocation, remaining_demand

# Title of the app
st.title("Resource Allocation Tool")

# Input: Define resource demand
st.subheader("Enter the demand for each resource")
resources = ['Resource A', 'Resource B', 'Resource C']
demand = {}
for resource in resources:
    demand[resource] = st.number_input(f"Demand for {resource}", min_value=0, value=0)

# Input: Define available resources
st.subheader("Enter the available resources")
available_resources = {}
for resource in resources:
    available_resources[resource] = st.number_input(f"Available {resource}", min_value=0, value=0)

# Initialize allocation and remaining demand to empty dicts
allocation = {}
remaining_demand = {}

# Button to perform resource allocation
if st.button("Allocate Resources"):
    allocation, remaining_demand = allocate_resources(demand, available_resources)
    
    # Display allocation results
    st.subheader("Resource Allocation Results")
    allocation_df = pd.DataFrame(list(allocation.items()), columns=["Resource", "Allocated"])
    st.write(allocation_df)
    
    # Display remaining demand
    st.subheader("Remaining Demand")
    remaining_demand_df = pd.DataFrame(list(remaining_demand.items()), columns=["Resource", "Remaining Demand"])
    st.write(remaining_demand_df)

# Optionally, add some visualizations
def plot_allocation(allocation, remaining_demand):
    if not allocation:  # Check if allocation is empty (i.e., no resources allocated yet)
        st.warning("Please click 'Allocate Resources' first.")
        return
    
    labels = list(allocation.keys())
    allocated_values = list(allocation.values())
    remaining_values = list(remaining_demand.values())

    fig, ax = plt.subplots(figsize=(8, 6))
    bar_width = 0.35
    index = range(len(labels))

    ax.bar(index, allocated_values, bar_width, label='Allocated')
    ax.bar([i + bar_width for i in index], remaining_values, bar_width, label='Remaining Demand')

    ax.set_xlabel('Resources')
    ax.set_ylabel('Units')
    ax.set_title('Resource Allocation vs Remaining Demand')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(labels)
    ax.legend()

    st.pyplot(fig)

# Show the plot
plot_allocation(allocation, remaining_demand)
