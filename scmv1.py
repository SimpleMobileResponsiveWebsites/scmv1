import streamlit as st

def main():
    st.title("Supply Chain Management Visualization")
    st.sidebar.title("Navigate SCM Phases")

    menu = [
        "Planning",
        "Sourcing",
        "Manufacturing/Production",
        "Inventory Management",
        "Distribution",
        "Customer Service",
        "Integration",
    ]

    choice = st.sidebar.selectbox("Select a Phase:", menu)

    if choice == "Planning":
        planning()
    elif choice == "Sourcing":
        sourcing()
    elif choice == "Manufacturing/Production":
        manufacturing()
    elif choice == "Inventory Management":
        inventory_management()
    elif choice == "Distribution":
        distribution()
    elif choice == "Customer Service":
        customer_service()
    elif choice == "Integration":
        integration()


def planning():
    st.header("Planning")
    st.write("Planning is a critical step in supply chain management that includes:")
    st.markdown("- **Demand forecasting**: Predicting customer demand for products.")
    st.markdown("- **Resource allocation**: Assigning resources efficiently to meet demand.")
    st.markdown("- **Risk assessment**: Identifying and mitigating risks.")
    st.markdown("- **Sustainability considerations**: Ensuring environmentally friendly practices.")

def sourcing():
    st.header("Sourcing")
    st.write("Sourcing involves securing the materials and services required for production. Key steps include:")
    st.markdown("- **Supplier selection**: Identifying and evaluating potential suppliers.")
    st.markdown("- **Material procurement**: Acquiring the necessary materials.")
    st.markdown("- **Price negotiation**: Ensuring cost-effectiveness.")
    st.markdown("- **Quality control**: Maintaining high-quality standards.")

def manufacturing():
    st.header("Manufacturing/Production")
    st.write("This phase focuses on transforming raw materials into finished products:")
    st.markdown("- **Raw material transformation**: Converting inputs into usable forms.")
    st.markdown("- **Assembly**: Combining components to create the final product.")
    st.markdown("- **Quality control**: Ensuring products meet quality standards.")
    st.markdown("- **Packaging**: Preparing products for distribution.")

def inventory_management():
    st.header("Inventory Management")
    st.write("Effective inventory management is key to avoiding overstocking or stockouts:")
    st.markdown("- **Stock tracking**: Monitoring stock levels in real-time.")
    st.markdown("- **Warehouse management**: Organizing and storing inventory efficiently.")
    st.markdown("- **Real-time inventory updates**: Ensuring accurate and timely updates.")

def distribution():
    st.header("Distribution")
    st.write("Distribution ensures products reach customers efficiently:")
    st.markdown("- **Transportation planning**: Developing strategies for shipping.")
    st.markdown("- **Logistics coordination**: Managing the flow of goods.")
    st.markdown("- **Order fulfillment**: Processing and delivering customer orders.")
    st.markdown("- **Last-mile delivery**: Ensuring timely delivery to end customers.")

def customer_service():
    st.header("Customer Service")
    st.write("Customer service focuses on maintaining satisfaction and managing returns:")
    st.markdown("- **Returns management**: Processing returned products.")
    st.markdown("- **Reverse logistics**: Handling the return flow of goods.")

def integration():
    st.header("Integration")
    st.write("Integration ensures seamless operation across all supply chain phases:")
    st.markdown("- **Cross-functional collaboration**: Promoting teamwork across departments.")
    st.markdown("- **Information sharing**: Ensuring transparency and effective communication.")
    st.markdown("- **Process alignment**: Streamlining processes to work in unison.")

if __name__ == "__main__":
    main()
