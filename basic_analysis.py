import plotly.express as px
import pandas as pd
import os
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt


def plot_lat_and_long():
    df = pd.read_csv("/Users/byronkim/Documents/projects/coros-data-analysis/converted_files/458499106195668992.fit_record.csv")

    # df.dropna(
    #     axis=0,
    #     how='any',
    #     thresh=None,
    #     subset=None,
    #     inplace=True
    # )

    df['formatted_lat'] = df['position_lat'] * ( 180 / 2**31 )
    df['formatted_long'] = df['position_long'] * ( 180 / 2**31 )


    color_scale = [(0, 'orange'), (1,'red')]

    print(df[['formatted_lat', 'formatted_long']].head())

    fig = px.scatter_mapbox(df, 
                            lat="formatted_lat", 
                            lon="formatted_long", 
                            #hover_name="Address", 
                            #hover_data=["Address", "Listed"],
                            #color="Listed",
                            color_continuous_scale=color_scale,
                            #size="Listed",
                            zoom=8, 
                            height=800,
                            width=800)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

def lap_analysis():

    new_rows = []

    for file in os.listdir('/Users/byronkim/Documents/projects/coros-data-analysis/converted_files/'):
        if 'lap' in file:
            lap_file = pd.read_csv('/Users/byronkim/Documents/projects/coros-data-analysis/converted_files/' + file)

            for idx, row in lap_file.iterrows():
                new_rows.append(row)

    total_laps_df = pd.DataFrame(new_rows, columns= lap_file.columns)

    print(total_laps_df.shape)

    plt.figure(figsize=(10, 6))
    plt.scatter(total_laps_df['avg_temperature'], total_laps_df['avg_speed'])
    plt.xlabel('Average Temperature')
    plt.ylabel('Average Speed')
    plt.title('Scatter Plot')
    plt.grid(True)
    plt.show()



if __name__ == "__main__":
    
    #plot_lat_and_long()
    lap_analysis()