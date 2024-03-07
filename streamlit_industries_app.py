import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data

df = pd.read_excel('Aggregate industries.xlsx')

df_long = df

# Streamlit app
st.title('European Scaleup Monitor: Bechmarking of industries in Europe')

# add subheader

st.subheader('This benchmarking tool allows you to compare different industries on different growth metrics. For more information on the European Scaleup Institute, visit https://scaleupinstitute.eu/. For more information on this benchmark tool, please reach out to info@scaleupinstitute.eu')



# Country selection
countries = df_long['NACE Rev. 2 main section'].unique()
selected_countries = st.multiselect('Select industries', countries, default=countries[0])

metrics = ['Scaler (companies with average annual growth rate of 10% in past three years)', 'HighGrowthFirm (companies with average annual growth rate of 20% in past three years)', 'Consistent HighGrowthFirm (high growth companies that grew 20% in at least 2 of the past three years)', 'Consistent Hypergrower (high growth companies that grew 40% in at least 2 of the past three years)', 'Gazelle (consistent high growth firm that is younger than 10 years)', 'Mature HighGrowthFirm (consistent high growth firm that is older than 10 years)', 'Scaleup (consistent hypergrower that is younger than 10 years)', 'Superstar (consistent hypergrower that is older than 10 years)' ]
selected = st.selectbox('Select metrics', metrics)
if selected == 'Scaler (companies with average annual growth rate of 10% in past three years)':
    selected_metrics = 'Scaler'
if selected == 'HighGrowthFirm (companies with average annual growth rate of 20% in past three years)':
    selected_metrics = 'HighGrowthFirm'
if selected == 'Consistent HighGrowthFirm (high growth companies that grew 20% in at least 2 of the past three years)':
    selected_metrics = 'ConsistentHighGrowthFirm'
if selected == 'Consistent Hypergrower (high growth companies that grew 40% in at least 2 of the past three years)':
    selected_metrics = 'VeryHighGrowthFirm'
if selected == 'Gazelle (consistent high growth firm that is younger than 10 years)':
    selected_metrics = 'Gazelle'
if selected == 'Mature HighGrowthFirm (consistent high growth firm that is older than 10 years)':
    selected_metrics = 'Mature'
if selected == 'Scaleup (consistent hypergrower that is younger than 10 years)':
    selected_metrics = 'Scaleup'
if selected == 'Superstar (consistent hypergrower that is older than 10 years)':
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

    listrelevantcolumns = ['NACE Rev. 2 main section']
    for i in range(len(filtered_data.columns)):
        if selected_metrics in filtered_data.columns[i]:
            listrelevantcolumns.append(filtered_data.columns[i])
    newtable = filtered_data[listrelevantcolumns]

    # change column names

    newtable.columns = newtable.columns.to_series().replace(selected_metrics + ' 2022 Obs', 'Total number of observed companies in 2022') \
    .replace(selected_metrics + ' 2022 Num', 'Number of ' + selected_metrics + 's in 2022') \
    .replace(selected_metrics + ' 2022 %', 'Percentage of ' + selected_metrics + 's in 2022') \
    .replace(selected_metrics + ' 2021 Obs', 'Total number of observed companies in 2021') \
    .replace(selected_metrics + ' 2021 Num', 'Number of ' + selected_metrics + 's in 2021') \
    .replace(selected_metrics + ' 2021 %', 'Percentage of ' + selected_metrics + 's in 2021') \
    .replace(selected_metrics + ' 2020 Obs', 'Total number of observed companies in 2020') \
    .replace(selected_metrics + ' 2020 Num', 'Number of ' + selected_metrics + 's in 2020') \
    .replace(selected_metrics + ' 2020 %', 'Percentage of ' + selected_metrics + 's in 2020') \
    .replace(selected_metrics + ' 2019 Obs', 'Total number of observed companies in 2019') \
    .replace(selected_metrics + ' 2019 Num', 'Number of ' + selected_metrics + 's in 2019') \
    .replace(selected_metrics + ' 2019 %', 'Percentage of ' + selected_metrics + 's in 2019') \
    .replace(selected_metrics + ' 2018 Obs', 'Total number of observed companies in 2018') \
    .replace(selected_metrics + ' 2018 Num', 'Number of ' + selected_metrics + 's in 2018') \
    .replace(selected_metrics + ' 2018 %', 'Percentage of ' + selected_metrics + 's in 2018')

    # set index to country

    newtable = newtable.set_index('NACE Rev. 2 main section')

    #print newtable as table in streamlit

    st.write(newtable)

else:
    st.write('Click to show data')
