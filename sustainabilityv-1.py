import streamlit as st

# Title of the app
st.title('Sustainability Considerations: Ensuring Environmentally Friendly Practices')

# Introduction text
st.markdown("""
    Welcome to the **Sustainability Considerations** app! This application is designed to help you understand 
    and implement environmentally friendly practices in your daily life, business, or community. You will find 
    practical suggestions and resources to reduce your environmental impact and make more sustainable choices.
    
    Sustainability involves minimizing harm to the environment, conserving resources, and reducing waste. Let’s 
    explore how we can all make a difference!
""")

# Sidebar with navigation options
st.sidebar.header('Navigation')
option = st.sidebar.selectbox('Choose an area to explore:', 
                             ['Overview of Sustainability Practices', 
                              'Energy Efficiency', 
                              'Waste Reduction', 
                              'Sustainable Transportation', 
                              'Eco-friendly Products', 
                              'Track Your Sustainability Goals'])

# Overview of Sustainability Practices
if option == 'Overview of Sustainability Practices':
    st.header('What is Sustainability?')
    st.write("""
        Sustainability refers to practices and actions that help conserve natural resources, reduce waste, 
        and limit pollution, aiming to preserve the planet for future generations. By focusing on energy efficiency, 
        waste management, eco-friendly transportation, and the use of sustainable products, individuals and businesses 
        can contribute to a healthier planet.
    """)
    st.markdown("""
        ### Key Areas of Sustainability:
        - **Energy Efficiency**: Reducing energy consumption through efficient appliances, renewable energy, etc.
        - **Waste Reduction**: Minimizing waste by reusing, recycling, and composting.
        - **Sustainable Transportation**: Choosing low-carbon transport options like biking, public transport, and electric vehicles.
        - **Eco-friendly Products**: Purchasing products with minimal environmental impact, such as those made from recycled materials.
    """)

# Energy Efficiency
elif option == 'Energy Efficiency':
    st.header('Energy Efficiency Practices')
    st.write("""
        Energy efficiency refers to using less energy to perform the same tasks. By adopting energy-efficient 
        technologies, individuals and businesses can reduce energy consumption, lower costs, and reduce their carbon footprint.
    """)
    st.markdown("""
        ### Tips for Energy Efficiency:
        - Use LED bulbs instead of incandescent lights.
        - Unplug electronics when not in use.
        - Insulate your home or workplace to reduce heating/cooling needs.
        - Switch to energy-efficient appliances (e.g., Energy Star rated).
        - Consider renewable energy sources like solar panels or wind turbines.
    """)
    st.image('https://www.example.com/energy_efficiency_image.jpg', caption='Energy-efficient appliances')

# Waste Reduction
elif option == 'Waste Reduction':
    st.header('Waste Reduction Practices')
    st.write("""
        Waste reduction involves minimizing the amount of waste produced and promoting the reuse and recycling of materials. 
        This is essential for reducing landfill waste and conserving resources.
    """)
    st.markdown("""
        ### Tips for Waste Reduction:
        - Reduce single-use plastic by opting for reusable containers and bags.
        - Start composting organic waste.
        - Recycle paper, plastic, and glass properly.
        - Buy products with minimal packaging.
        - Donate or repurpose old items rather than throwing them away.
    """)
    st.image('https://www.example.com/waste_reduction_image.jpg', caption='Composting and recycling')

# Sustainable Transportation
elif option == 'Sustainable Transportation':
    st.header('Sustainable Transportation Options')
    st.write("""
        Sustainable transportation includes using low-carbon transport modes to reduce greenhouse gas emissions and pollution.
    """)
    st.markdown("""
        ### Sustainable Transportation Options:
        - **Walking or Biking**: The most eco-friendly and healthy mode of transport.
        - **Public Transit**: Reduce the number of vehicles on the road by using buses, trains, or trams.
        - **Electric Vehicles (EVs)**: Consider electric cars or e-scooters to reduce fossil fuel use.
        - **Carpooling**: Share rides with others to reduce the number of vehicles on the road.
    """)
    st.image('https://www.example.com/sustainable_transport_image.jpg', caption='Electric car')

# Eco-friendly Products
elif option == 'Eco-friendly Products':
    st.header('Eco-friendly Products')
    st.write("""
        Eco-friendly products are made using sustainable materials, and their production processes aim to minimize 
        negative environmental impacts.
    """)
    st.markdown("""
        ### Types of Eco-friendly Products:
        - **Organic Food**: Grown without synthetic pesticides or fertilizers.
        - **Reusable Items**: Items like reusable water bottles, shopping bags, and containers.
        - **Biodegradable Products**: Items that break down naturally, reducing waste.
        - **Sustainable Clothing**: Clothing made from recycled or organic materials.
    """)
    st.image('https://www.example.com/eco_products_image.jpg', caption='Eco-friendly products')

# Track Your Sustainability Goals
elif option == 'Track Your Sustainability Goals':
    st.header('Track Your Sustainability Goals')
    st.write("""
        Setting sustainability goals is a great way to stay motivated and measure progress. You can track energy usage, waste reduction, 
        transportation choices, and more. Below is a simple form to help you keep track of your sustainability efforts.
    """)

    # Input form for sustainability goals
    with st.form(key='goal_form'):
        st.text_input('Enter your goal (e.g., reduce energy consumption by 20%)')
        st.slider('Select your target date (in months)', 1, 12, 6)
        submit_button = st.form_submit_button('Track Goal')

    if submit_button:
        st.success("Your sustainability goal has been recorded!")

# Footer
st.markdown("""
    **Thank you for visiting!**  
    Remember, every small step towards sustainability can make a big impact. Start making greener choices today for a better tomorrow.
""")
