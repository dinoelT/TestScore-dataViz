import streamlit as st
import pandas as pd
import altair as alt



#Displays the title
st.title("Визуализация баллов ЕГЭ")

df = pd.read_csv("ege_scores.csv")

en_rus_columns = {
    "program": "Кафедра",
    "is_budget": "Бюджет",
    "ege_math": "ЕГЭ по математике",
    "ege_russian": "ЕГЭ по русскому языку", 
    "ege_it":"ЕГЭ по информатике", 
    "ege_foreign": "ЕГЭ  по иностранному языку"
}

en_rus_program = {
    "ITMB": "ИТМБ",
    "FET": "ФЭТ",
    "FM":"ФМ"
}


#Streamlit columns for alignment, ratio (1,1,1,5)
#The first 3 columns will contain the checkboxes, the column with width 5 will be empty
c1,c2,c3, _ = st.beta_columns((1,1,1,5))
#Save the column objects into a list for iteration
cols = [c1,c2,c3]

#Replace the values in the Program column with russian values
df.program.replace(to_replace = en_rus_program, inplace = True)

#The state dictionary in the format <program>:<is_checked>
state_dict = {prog : cols[i].checkbox(label=prog, value=True) for i, prog in enumerate(df.program.unique())}

#Save the programs for which the checkbox is checked in a list
columns_to_plot = [program for program, is_checked in state_dict.items() if is_checked==True]

#Select the datapoints for the programs selected using the checkboxes
df = df[df.program.isin(columns_to_plot)] # select programs

#Rename the dataframe columns
df.rename(columns=en_rus_columns, inplace=True)


#Plot the data
x_col_name = "ЕГЭ по математике"
y_col_name = "ЕГЭ по русскому языку"
color_column = "Кафедра"
tooltip_values = [x_col_name, y_col_name]


chart = alt.Chart(df).mark_circle(size=100).encode(
    alt.X(x_col_name, scale=alt.Scale(domain = (35,105))),
    alt.Y(y_col_name,scale=alt.Scale(domain = (40,105))),
    color = color_column,
    tooltip=tooltip_values
).interactive()

st.altair_chart(chart, use_container_width=True)

#This is just a message displayed under the plot
#The correct way is to use st.text(), but it doesn't look good on page, because it adds a scroller
"Баллы ЕГЭ также показаны по студентам, которые перевелись на факультет в течение первого года обучения."