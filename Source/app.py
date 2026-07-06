import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Skyline Airways Analytics",
    layout="wide"
)


# ---------------- LOAD DATA ----------------

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
airline = pd.read_excel(BASE_DIR / "Datasets" / "train.xlsx")


# ---------------- DATA CLEANING ----------------


# Customer Type rename

airline['Customer Type'] = airline['Customer Type'].replace(
    {
        'Loyal Customer':'Frequent Traveler',
        'disloyal Customer':'Occasional Traveler'
    }
)


# Satisfaction convert into 2 categories

airline['satisfaction'] = airline['satisfaction'].replace(
    {
        'neutral or dissatisfied':'dissatisfied'
    }
)



# ---------------- STYLE ----------------


st.markdown("""
<style>

.main-title{
font-size:45px;
font-weight:800;
color:#B22222;
}

.sub-title{
font-size:22px;
color:#555;
}

</style>

""",unsafe_allow_html=True)



# ---------------- HEADER ----------------


col1,col2 = st.columns([1,5])


with col1:

    logo="Assets/logo.png"

    if os.path.exists(logo):

        st.image(
            logo,
            width=120
        )

    else:
        st.write("✈️")



with col2:

    st.markdown(

    """
    <div class="main-title">
    SKYLINE AIRWAYS
    </div>

    <div class="sub-title">
    Customer Satisfaction & Service Quality Analytics Dashboard
    </div>

    """,

    unsafe_allow_html=True
    )



st.divider()



# ---------------- FILTERS ----------------


st.sidebar.header("Dashboard Filters")



classes = st.sidebar.multiselect(

    "Travel Class",

    airline["Class"].unique(),

    default=airline["Class"].unique()

)



customers = st.sidebar.multiselect(

    "Customer Type",

    airline["Customer Type"].unique(),

    default=airline["Customer Type"].unique()

)



satisfaction_filter = st.sidebar.multiselect(

    "Satisfaction",

    airline["satisfaction"].unique(),

    default=airline["satisfaction"].unique()


)

# ---------------- BUSINESS INSIGHT FILTER ----------------

st.sidebar.markdown("---")

st.sidebar.subheader("🔍 Analyze Satisfaction By")

analysis = st.sidebar.selectbox(
    "Select a Factor",
    [
        "Travel Class",
        "Customer Type",
        "Departure Delay",
        "Arrival Delay",
        "Seat Comfort",
        "Food and Drink",
        "Inflight Service",
        "Online Boarding",
        "Cleanliness",
        "Baggage Handling"
    ]
)



# Filter data


df = airline[

    (airline["Class"].isin(classes))

    &

    (airline["Customer Type"].isin(customers))

    &

    (airline["satisfaction"].isin(satisfaction_filter))

]




# ---------------- KPI ----------------



service_columns=[

'Seat comfort',

'Inflight service',

'Food and drink',

'Cleanliness',

'Online boarding',

'Baggage handling'

]



total=len(df)



satisfied = (

df["satisfaction"]

.value_counts(normalize=True)

.get("satisfied",0)

*100

)



dissatisfied = (

df["satisfaction"]

.value_counts(normalize=True)

.get("dissatisfied",0)

*100

)



avg_delay=(

df["Departure Delay in Minutes"].mean()

+

df["Arrival Delay in Minutes"].mean()

)/2



service_score = df[service_columns].mean().mean()




st.subheader("📌 Business KPI")



a,b,c,d,e = st.columns(5)



a.metric(
"Total Passengers",
f"{total:,}"
)



b.metric(
"Satisfied %",
f"{satisfied:.1f}%"
)



c.metric(
"Dissatisfied %",
f"{dissatisfied:.1f}%"
)



d.metric(
"Average Delay",
f"{avg_delay:.1f} min"
)



e.metric(
"Service Rating",
f"{service_score:.2f}/5"
)




st.divider()



# ---------------- CHART FUNCTION ----------------


def chart():

    fig, ax = plt.subplots(figsize=(7,5))
    fig.tight_layout()

    return fig, ax




# ---------------- ROW 1 ----------------



c1,c2 = st.columns(2)



# Satisfaction chart


with c1:


    st.subheader("Customer Satisfaction")


    fig,ax=chart()


    df["satisfaction"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    colors=["#C0392B", "#2E8B57"],
    startangle=90,
    wedgeprops={"edgecolor":"white","linewidth":1},
    ax=ax
)


    ax.set_ylabel("")


    st.pyplot(fig)





# Travel Class chart


with c2:


    st.subheader("Travel Class Performance")


    fig,ax=chart()


    df.groupby("Class")["satisfaction"].value_counts().unstack().plot(
    kind="bar",
    ax=ax,
    color=["#C0392B", "#2E8B57"]
)


    ax.tick_params(

        axis='x',

        rotation=0

    )


    ax.set_ylabel("Passengers")


    st.pyplot(fig)






# ---------------- ROW 2 ----------------



c3,c4 = st.columns(2)



# Service rating


with c3:

    st.subheader("Service Quality Rating")

    fig, ax = chart()

    # Average rating in descending order
    service_avg = df[service_columns].mean().sort_values(ascending=False)

    service_avg.plot(
        kind="barh",
        color="#2E8B57",      # Same green as 'Satisfied'
        edgecolor="black",
        ax=ax
    )

    # Highest rating at the top
    ax.invert_yaxis()

    ax.set_xlabel("Average Rating", fontsize=11)
    ax.set_ylabel("")

    ax.set_xlim(0, 5)

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)





# Customer type


with c4:

    st.subheader("Customer Type Analysis")

    fig, ax = chart()

    customer = (
        df.groupby("Customer Type")["satisfaction"]
          .value_counts()
          .unstack()
    )

    customer.plot(
    kind="bar",
    stacked=False,
    ax=ax,
    width=0.65,
    color=["#C0392B", "#2E8B57"]
)

    ax.set_xticklabels(
        ["Frequent\nTraveler", "Occasional\nTraveler"],
        rotation=0,
        fontsize=9
    )

    ax.set_xlabel("Customer Type", fontsize=10)
    ax.set_ylabel("Passengers", fontsize=10)

    ax.legend(
        title="Satisfaction",
        fontsize=8,
        title_fontsize=9,
        loc="upper right"
    )

    fig.tight_layout()

    st.pyplot(fig, use_container_width=True)




# ---------------- ROW 3 ----------------



c5,c6 = st.columns(2)



# Delay impact


with c5:


    st.subheader("Delay Impact")


    fig,ax=chart()


    df.groupby(

        "satisfaction"

    )[

    [

    "Departure Delay in Minutes",

    "Arrival Delay in Minutes"

    ]

    ].mean().plot(
    kind="bar",
    ax=ax,
    color=["#C0392B", "#2E8B57"]
)


    ax.tick_params(

        axis='x',

        rotation=0

    )


    st.pyplot(fig)







# Scatter plot


with c6:

    st.subheader("Departure vs Arrival Delay")

    fig, ax = chart()

    ax.scatter(
        df["Departure Delay in Minutes"],
        df["Arrival Delay in Minutes"],
        color="#2E8B57",     # Dashboard green
        alpha=0.6,           # Slight transparency
        s=18,                # Point size
        edgecolors="white",
        linewidth=0.3
    )

    ax.set_xlabel("Departure Delay (Minutes)", fontsize=11)
    ax.set_ylabel("Arrival Delay (Minutes)", fontsize=11)

    ax.grid(alpha=0.3, linestyle="--")

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)

    # ---------------- BUSINESS INSIGHTS ----------------

st.divider()

st.subheader("📊 Business Insight")

if analysis == "Travel Class":
    st.info("""
Business class passengers generally report higher satisfaction.

Economy passengers show comparatively lower satisfaction due to seat comfort,
food quality, and service experience.
""")

elif analysis == "Customer Type":
    st.info("""
Frequent travelers are more likely to be satisfied.

Retaining loyal customers through rewards and personalized services can improve customer retention.
""")

elif analysis == "Departure Delay":
    st.warning("""
Higher departure delays reduce customer satisfaction.

Reducing departure delays can significantly improve the passenger experience.
""")

elif analysis == "Arrival Delay":
    st.warning("""
Arrival delays strongly affect customer satisfaction.

Improving on-time arrivals increases customer trust and loyalty.
""")

elif analysis == "Seat Comfort":
    st.success("""
Seat comfort is one of the strongest drivers of customer satisfaction.

Investing in better seating can improve customer experience.
""")

elif analysis == "Food and Drink":
    st.success("""
Improving food quality and beverage options can increase overall passenger satisfaction.
""")

elif analysis == "Inflight Service":
    st.success("""
Friendly and efficient inflight service has a positive impact on customer satisfaction.
""")

elif analysis == "Online Boarding":
    st.success("""
A smooth online boarding process reduces waiting time and improves the travel experience.
""")

elif analysis == "Cleanliness":
    st.success("""
Passengers highly value aircraft cleanliness.

Maintaining hygiene standards improves customer confidence.
""")

elif analysis == "Baggage Handling":
    st.success("""
Reliable baggage handling improves passenger trust and reduces travel complaints.
""")






# ---------------- RAW DATA ----------------



st.divider()



st.subheader("📄 Passenger Raw Data")



st.dataframe(

df.head(20),

use_container_width=True

)



# ---------------- RECOMMENDATIONS ----------------


st.divider()


st.subheader("💡 Business Recommendations for Skyline Airways")


st.markdown(
"""
### 1. Improve Flight Delay Management
- Analyze the major causes of departure and arrival delays.
- Improve scheduling and operational planning.
- Provide real-time updates to passengers during delays.


### 2. Improve Low Rated Services
- Focus on services with lower passenger ratings.
- Improve areas like food quality, cleanliness, baggage handling, and online boarding experience.


### 3. Enhance Economy Class Experience
- If Economy passengers show lower satisfaction, improve:
    - Seat comfort
    - Food quality
    - Customer support
    - Overall travel experience


### 4. Retain Frequent Travelers
- Frequent travelers are valuable customers.
- Provide better loyalty benefits and personalized services to increase retention.


### 5. Improve Digital Experience
- Simplify online booking and boarding process.
- Provide a smoother mobile and web experience for passengers.

"""
)



# ---------------- PROJECT AUTHOR ----------------


st.divider()



st.markdown(
"""

**Author:**  
Agalya M


**Role:**  
Data Analyst Project


"""
)