import streamlit as st
import requests
import pandas as pd
import altair as alt

logo_image = "ecognitive.png"
st.image(logo_image, use_column_width=True)

url = "https://api.thingspeak.com/channels/2121478/fields/1.json"
response = requests.get(url)
data = response.json()

created_at_values = [entry["created_at"] for entry in data["feeds"]]
field1_values = [float(entry["field1"]) for entry in data["feeds"]]

with st.container():
    st.subheader("Elemento obtido pelo thigspeak: Co2")
    st.title('Gráfico de Quantidade de Poluente')

with st.container():
    st.write("---")
    df = pd.DataFrame({"Data": created_at_values, "Quantidade do Poluente": field1_values})

    df = df[df["Quantidade do Poluente"] > 0]

    # calcular a porcentagem de poluente em relação ao total
    total = df["Quantidade do Poluente"].sum()
    df["Porcentagem"] = (df["Quantidade do Poluente"] / total) * 100
    # Adicionar coluna de cor com base na quantidade do poluente
    df["Cor"] = df["Porcentagem"].apply(lambda x: "Grave" if x > 5 else "Alerta" if 3 <= x <= 5 else "Estável")
    #df["Porcentagem"] = df["Porcentagem"].map("{:.2f}%".format)  # formata os valores como porcentagem

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
        filtered_df = df

    if st.button("Exibir Gráfico"):
        chart = alt.Chart(filtered_df).mark_bar().encode(
            x="Data",
            y="Porcentagem",
            color=alt.Color("Cor:N", scale=alt.Scale(domain=["Estável", "Alerta", "Grave"],
                                                     range=["#4ac26b", "#eac54f", "#ec6547"]))
        )

        st.altair_chart(chart, use_container_width=True)
