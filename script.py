import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

highLighted = None

def ViewPrototype(map_img_filename):
    df = pd.read_csv('data/seafloor/EMODNET_MLDB_aggregated_collection_seafloor.csv')
    dateQuantifyer = "Date > '2018-01-01'" + '&' + "Date < '2019-01-01'"

    # DepthQuantifyer = '&' + 'Depth > 50'
    df = df.query(dateQuantifyer) # + DepthQuantifyer)
    print(df.head())

    # Bounding Box

    # from dataset
    # BBox = ((df.HaulLong.min(),   df.HaulLong.max(),      
    #          df.HaulLat.min(), df.HaulLat.max()))

    # map-1. Coords taken from OpenStreetMap map export
    BBox = ((6.723632812500001,17.490234375000004,54.18494116668456,57.856443276115066))

    # map-2
    #BBox = ((9.8, 13.370, 56.172, 57.169))

    print(BBox)
    # Prints the actual bounding box for the data points in dataset


    def update_annot(ind):
        global highLighted 
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        dateQuantifyer = "Date > '2018-01-01'" + '&' + "Date < '2019-01-01'"
        query = dateQuantifyer +'&'+ 'HaulLong=='+str(pos[0])+'&'+'HaulLat=='+str(pos[1])
        
        res = df.query(query)

        if highLighted == None: 
            highLighted = ax.scatter(res.ShootLong, res.ShootLat, zorder=1, alpha= 0.2, c='r', s=10)
            highLighted.set_visible(True)

        date = res[['Date', 'SurveyName', 'Country', 'Ship', 'Depth', 'UnitWgt', 'LT_Weight', 'UnitItem', 'LT_Items', 'ShootLong', 'ShootLat', 'HaulLong', 'HaulLat']]
        print(date)

        text = "Id"
        text = text + date.to_csv().replace(',', ',    ')
        text = text.strip()
        annot.set_text(text)
        # annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
        annot.get_bbox_patch().set_alpha(0.4)

    def hover(event):
        global highLighted 
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                sc2.set_visible(False)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    if highLighted != None: 
                        highLighted.set_visible(False)
                        highLighted = None
                    sc2.set_visible(True)
                    fig.canvas.draw_idle()

    ocean_m = plt.imread(f'map/{map_img_filename}.png')
    fig, ax = plt.subplots(figsize = (20,40))
    sc2 = ax.scatter(df.ShootLong, df.ShootLat, zorder=1, alpha= 0.2, c='r', s=10)
    sc = ax.scatter(df.HaulLong, df.HaulLat, zorder=1, alpha= 0.2, c='b', s=10)
    ax.set_title('Exploring ' + 'EMODNET_MLDB_aggregated_collection_seafloor.csv' + ' Data on Map')


    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    fig.canvas.mpl_connect("motion_notify_event", hover)

    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])

    ax.imshow(ocean_m, extent = BBox, zorder=0) #, aspect= 'equal'

    plt.show()

ViewPrototype("map-simple")
# ViewPrototype("map-advanced")
