import streamlit as st
import requests
import pandas as pd

url = "https://api.thingspeak.com/channels/2121478/fields/1.json"
response = requests.get(url)
data = response.json()

created_at_values = [entry["created_at"] for entry in data["feeds"]]
field1_values = [float(entry["field1"]) for entry in data["feeds"]]

with st.container():
    st.subheader("eCOgnitive IoT")
    st.title('Gráfico de Quantidade de Poluente')

with st.container():
    st.write("---")
    df = pd.DataFrame({"Data": created_at_values, "Quantidade do Poluente": field1_values})

    df = df[df["Quantidade do Poluente"] > 0]

    period = st.selectbox("Selecione o período", ["7D", "15D", "30D", "MAX", "MIN"])

    if period == "7D":
        filtered_df = df.tail(7)
    elif period == "15D":
        filtered_df = df.tail(15)
    elif period == "30D":
        filtered_df = df.tail(30)
    elif period == "MAX":
        filtered_df = df.nlargest(1, "Quantidade do Poluente")
    elif period == "MIN":
        filtered_df = df.nsmallest(1, "Quantidade do Poluente")
    else:
        filtered_df = df  # Período completo

    if st.button("Exibir Gráfico"):
        st.bar_chart(filtered_df, x="Data", y="Quantidade do Poluente")
