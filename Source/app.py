import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Skyline Airways Analytics",
    page_icon="✈️",
    layout="wide"
)



# ---------------- LOAD DATA ----------------


airline = pd.read_excel(
r"C:\Users\AGALYAMAHESWARAN\Desktop\Documents\Airline_Passenger_Satisfaction_Analysis\Datasets\train.xlsx"
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



# ---------------- FILTER ----------------


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



df = airline[

(airline["Class"].isin(classes))

&

(airline["Customer Type"].isin(customers))

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



satisfied=(

df["satisfaction"]

.value_counts(normalize=True)

.get("satisfied",0)

*100

)



dissatisfied=(

df["satisfaction"]

.value_counts(normalize=True)

.get("neutral or dissatisfied",0)

*100

)



avg_delay=(

df["Departure Delay in Minutes"].mean()

+

df["Arrival Delay in Minutes"].mean()

)/2



service_score=df[service_columns].mean().mean()




st.subheader("📌 Business KPI")



a,b,c,d,e=st.columns(5)



a.metric(
"Total Passengers",
f"{total:,}"
)


b.metric(
"Satisfaction %",
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

    fig,ax=plt.subplots()

    return fig,ax





# ---------------- ROW 1 ----------------



c1,c2=st.columns(2)



with c1:


    st.subheader("Customer Satisfaction")


    fig,ax=chart()


    df["satisfaction"].value_counts().plot(

    kind="pie",

    autopct="%1.1f%%",

    ax=ax

    )


    ax.set_ylabel("")

    st.pyplot(fig)




with c2:


    st.subheader("Travel Class Performance")


    fig,ax=chart()


    df.groupby(

    "Class"

    )["satisfaction"].value_counts().unstack().plot(

    kind="bar",

    ax=ax

    )


    st.pyplot(fig)




# ---------------- ROW 2 ----------------



c3,c4=st.columns(2)



with c3:


    st.subheader("Service Quality Rating")


    fig,ax=chart()


    df[service_columns].mean().plot(

    kind="barh",

    ax=ax

    )


    ax.set_xlabel("Rating")


    st.pyplot(fig)





with c4:


    st.subheader("Customer Type Analysis")


    fig,ax=chart()


    df.groupby(

    "Customer Type"

    )["satisfaction"].value_counts().unstack().plot(

    kind="bar",

    stacked=True,

    ax=ax

    )


    st.pyplot(fig)





# ---------------- ROW 3 ----------------



c5,c6=st.columns(2)



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

    ax=ax

    )


    st.pyplot(fig)





with c6:


    st.subheader("Departure vs Arrival Delay")


    fig,ax=chart()


    ax.scatter(

    df["Departure Delay in Minutes"],

    df["Arrival Delay in Minutes"]

    )


    ax.set_xlabel("Departure Delay")

    ax.set_ylabel("Arrival Delay")


    st.pyplot(fig)




# ---------------- RAW DATA ----------------



st.divider()


st.subheader("📄 Passenger Raw Data")


st.dataframe(

df.head(20),

use_container_width=True

)