import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data

df = pd.read_excel('Aggregate industries.xlsx')

df_long = df

# Streamlit app
st.title('European Scaleup Monitor: Bechmarking of industries in Europe')

# add subheader

st.subheader('This benchmarking tool allows you to compare different industries on different growth metrics. For more information on the European Scaleup Institute, visit https://scaleupinstitute.eu/. For more information on this benchmark tool, please reach out to Dries Faems (https://www.linkedin.com/in/dries-faems-0371569/)')



# Country selection
countries = df_long['NACE Rev. 2 main section'].unique()
selected_countries = st.multiselect('Select industries', countries, default=countries[0])

metrics = ['Scaler', 'HighGrowthFirm', 'Consistent HighGrowthFirm', 'Consistent Hypergrower', 'Gazelle', 'Mature HighGrowthFirm', 'Scaleup', 'Superstar']
selected = st.selectbox('Select metrics', metrics)
if selected == 'Scaler':
    selected_metrics = 'Scaler'
if selected == 'HighGrowthFirm':
    selected_metrics = 'HighGrowthFirm'
if selected == 'Consistent HighGrowthFirm':
    selected_metrics = 'ConsistentHighGrowthFirm'
if selected == 'Consistent Hypergrower':
    selected_metrics = 'VeryHighGrowthFirm'
if selected == 'Gazelle':
    selected_metrics = 'Gazelle'
if selected == 'Mature HighGrowthFirm':
    selected_metrics = 'Mature'
if selected == 'Scaleup':
    selected_metrics = 'Scaleup'
if selected == 'Superstar':
    selected_metrics = 'Superstar'


# Filtering data
filtered_data = df_long[df_long['NACE Rev. 2 main section'].isin(selected_countries)]
number_of_countries = len(selected_countries)

clicked = st.button('Show data')
if clicked:
    
    # Plotting
    fig, ax = plt.subplots()
    x = [2018, 2019, 2020, 2021, 2022]
    ylistmeta = []
    for country in selected_countries:
        country_data = filtered_data[filtered_data['NACE Rev. 2 main section'] == country]
        ylist = list()
        ylist.append(country_data[selected_metrics + ' ' + str(2018) + ' %'].iloc[0]*100)
        ylist.append(country_data[selected_metrics + ' ' + str(2019) + ' %'].iloc[0]*100)
        ylist.append(country_data[selected_metrics + ' ' + str(2020) + ' %'].iloc[0]*100)
        ylist.append(country_data[selected_metrics + ' ' + str(2021) + ' %'].iloc[0]*100)
        ylist.append(country_data[selected_metrics + ' ' + str(2022) + ' %'].iloc[0]*100)
        ylistmeta.append(ylist)
        ax.plot(x, ylist, label=country)
        for i, txt in enumerate(ylist):
        # Format the number to two decimal places
            formatted_txt = "{:.2f}".format(txt)
            ax.annotate(formatted_txt, (x[i], ylist[i]), textcoords="offset points", xytext=(0,4), ha='center')

    # Set x-axis to display only integers
    ax.set_xticks(x)
    ax.set_xticklabels(x)

    # Add grid to the plot
    ax.grid(True)

    ax.set_title('Benchmarking of industries in Europe based on the metric: ' + selected_metrics)


    ax.set_xlabel('Year')
    ax.set_ylabel(selected_metrics+ ' %')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15))
    st.pyplot(fig)

else:
    st.write('Click to show data')
