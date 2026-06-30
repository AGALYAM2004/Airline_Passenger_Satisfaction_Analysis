import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ---------------- DATA ----------------

airline = pd.read_excel(
    r"C:\Users\AGALYAMAHESWARAN\Desktop\Documents\Airline_Passenger_Satisfaction_Analysis\Datasets\train.xlsx"
)


# ---------------- TITLE ----------------

st.title("✈️ Airline Customer Satisfaction Dashboard")


# ---------------- KPI ----------------

total_passengers = len(airline)

satisfaction = (
    airline['satisfaction']
    .value_counts(normalize=True)
    ['satisfied'] * 100
)

dissatisfaction = (
    airline['satisfaction']
    .value_counts(normalize=True)
    ['neutral or dissatisfied'] * 100
)


avg_delay = (
    airline['Departure Delay in Minutes'].mean()
    +
    airline['Arrival Delay in Minutes'].mean()
)/2

service_columns = [
    'Seat comfort',
    'Inflight service',
    'Food and drink',
    'Cleanliness',
    'Online boarding',
    'Baggage handling'
]


service_rating = airline[service_columns].mean().mean()



k1,k2,k3,k4,k5 = st.columns(5)


k1.metric("Total Passengers", total_passengers)

k2.metric(
    "Satisfaction %",
    f"{satisfaction:.2f}%"
)

k3.metric(
    "Dissatisfaction %",
    f"{dissatisfaction:.2f}%"
)

k4.metric(
    "Average Delay",
    f"{avg_delay:.2f} min"
)

k5.metric(
    "Service Rating",
    f"{service_rating:.2f}/5"
)



# ---------------- CHARTS ----------------


c1,c2 = st.columns(2)


with c1:

    st.subheader("Satisfaction Distribution")

    fig,ax = plt.subplots()

    airline['satisfaction'].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax
    )

    ax.set_ylabel("")

    st.pyplot(fig)



with c2:

    st.subheader("Travel Class Satisfaction")

    fig,ax = plt.subplots()

    airline.groupby(
        'Class'
    )['satisfaction'].value_counts().unstack().plot(
        kind="bar",
        ax=ax
    )

    st.pyplot(fig)




c3,c4 = st.columns(2)


with c3:

    st.subheader("Service Ratings")

    services = [
        'Seat comfort',
        'Inflight service',
        'Food and drink',
        'Cleanliness',
        'Online boarding',
        'Baggage handling'
    ]

    fig,ax = plt.subplots()

    airline[services].mean().plot(
        kind="bar",
        ax=ax
    )

    st.pyplot(fig)



with c4:

    st.subheader("Delay Correlation")

    fig,ax = plt.subplots()

    ax.scatter(
        airline['Departure Delay in Minutes'],
        airline['Arrival Delay in Minutes']
    )

    ax.set_xlabel("Departure Delay")

    ax.set_ylabel("Arrival Delay")

    st.pyplot(fig)




# ---------------- RAW DATA ----------------


st.subheader("📄 Raw Data")

st.dataframe(
    airline.head(20)
)