from email.policy import default
from multiprocessing.sharedctypes import Value
from optparse import Values
import pandas as pd
import numpy as np
import pickle
import sklearn
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from plotly.offline import init_notebook_mode
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime as dt
import plotly.graph_objects as go
from PIL import Image
import altair as alt
import math
import plotly.figure_factory as ff

balls=pd.read_csv("ipldata.csv")
matches= pd.read_csv("yearwise.csv")

st.set_page_config(
    page_title='Akku-Dashboard',
    layout='wide'
)
# st.title("IPL Analysis")
col1,col2,col3=st.columns([3,1,3])
with col2:
    image=Image.open('IPLLogo.png')
    edited=image.resize((2600,1950))
    st.image(edited,use_column_width=True)
    # st.header('Dashboard')

image=Image.open('iplimage.jpg')
edited=image.resize((3060,300))
st.image(edited,use_column_width=True)



# menu =['Home','Search','About']
# choice = st.sidebar.selectbox("Menu",menu)


tab1,tab2,tab3=st.tabs(['OVERVIEW','SCORECARD','PREDICTION'])
with tab1:
    team_option=matches['team1'].unique().tolist()
    year_option=matches['year'].unique().tolist()
    year_option1=matches['year'].unique().tolist()
    year_option1.reverse()
    year_option1.insert(0,"All")
    co1,co2=st.columns(2)
    with co1:
        year_year=st.selectbox("Year",year_option1)
    

    if year_year=="All":
        with co2:
            team_t= st.selectbox("Teams",team_option)
    
    # for i in team_option:
    #     # for j in year_year:
    #         if team_t==i and year_year=="All":
        def year(name):
            c1,c2,c3,c4,c5=st.columns(5)
            play11=matches[matches['team1']==name]
            play12=matches[matches['team2']==name]
            noteam12=play12['team2'].count()
            noteam11=play11['team1'].count()
            t_m_played=noteam11+noteam12

            win=matches[matches['winner']==name]
            winall=win['winner'].count()
                
            t_loss=(t_m_played-winall)  
                
            win_per_total=((winall/t_m_played)*100)
                
            loss_per_total=((t_m_played-winall)/t_m_played)*100
            with c1:
                st.subheader("Matches Played")
                st.subheader(t_m_played)
            with c2:
                st.subheader("Matches Won")
                st.subheader(winall)
            with c3:
                st.subheader("Matches Loss")
                st.subheader(t_loss)
            with c4:
                st.subheader("Win Percentage")
                st.subheader(f'{math.ceil(win_per_total)}%')
            with c5:
                st.subheader("Loss Percentage")
                st.subheader(f'{math.floor(loss_per_total)}%')

        year(team_t)

        pie=matches[matches['winner']==team_t]
        gb=pie.groupby(['team1'],as_index=False)['id'].count().sort_values(by='team1',ascending=False).reset_index(drop=True)
        gbg=pie.groupby(['team2'],as_index=False)['id'].count().sort_values(by='team2',ascending=False).reset_index(drop=True)
        gbg1=pd.DataFrame(gbg)
        hy=gbg1.rename(columns={'team2':'team1'})
        con=pd.concat([gb,hy],ignore_index=True)
        fi_gb=con.groupby(['team1'],as_index=False)['id'].sum().sort_values(by='id',ascending=False).reset_index(drop=True)
        new_gb=fi_gb.drop(0)
        new_new_gb=new_gb.rename(columns={'id':'win'})

        coll1,coll2,coll3=st.columns(3)
       

        with coll2: 

            to=matches[matches['toss_decision']=='bat']
            too=to[to['winner']==team_t]  
            tof=matches[matches['toss_decision']=='field']
            toof=tof[tof['winner']==team_t]
            toss=pd.DataFrame({'A':[too.shape[0],toof.shape[0]],
                        'B':["Bat","Field"]})  
        # st.write(datafroom)

            pie_cart1=px.pie(toss,
                            title=f"            Matches Won By \n Toss Decision",
                            values="A",
                            names="B",
                            width=370,
                            height=370)
            st.plotly_chart(pie_cart1)
        with coll1:
            tor=matches[matches['result']=='runs']
            toor=tor[tor['winner']==team_t]
            tofr=matches[matches['result']=='wickets']
            toofr=tofr[tofr['winner']==team_t]
            tossr=pd.DataFrame({'A':[toor.shape[0],toofr.shape[0]],
                        'B':["Win By Runs","Win By Wickets"]})  
            pie_cart2=px.pie(tossr,
                            title=f"Matches Won By \n Runs/Wickets",
                            values="A",
                            names="B",
                            width=400,
                            height=400)
            st.plotly_chart(pie_cart2)

        per_s=matches[matches['winner']==team_t]
        gb_s=per_s.groupby(['year'],as_index=False)['id'].count().sort_values(by='year',ascending=True).reset_index(drop=True)
        gb_s['Year']=gb_s['year'].astype(str)
        gb_s=gb_s.rename(columns={'id':'Matches'})

        barcart=px.bar(gb_s,
                x='Year',
                y='Matches',
                text='Matches',
                title='<b>Matches Won Per Season</b>',
                template="plotly_white",

                )
        barcart.update_layout(
                xaxis=dict(tickmode='linear'),
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=(dict(showgrid=False)),
                )
        coll3.plotly_chart(barcart,use_container_width=True)
            


        play11=matches[matches['team1']==team_t]
        play12=matches[matches['team2']==team_t]
        pla=pd.concat([play11,play12])
        # pla
        gbs=pla.groupby(['year'],as_index=False)['id'].count().sort_values(by='year',ascending=True).reset_index(drop=True)
        gbs['Win']=gb_s['Matches']
        gbs['M_played']=gbs['id']
        gbb=gbs.drop(['id'],axis=1)
        # gbb

        barcart2=px.bar(gbb,
                x='year',
                y='M_played',
                text='M_played',
                title='<b>Matches Played Per Season</b>',
                template="plotly_white")

        barcart2.update_layout(
                xaxis=dict(tickmode='linear'),
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=(dict(showgrid=False)),
                )

        coo1,coo2=st.columns(2)
        coo2.plotly_chart(barcart2,use_container_width=True)
        with coo1:  
            piey_t2=matches[matches['team2']==team_t]
            piey_t1=matches[matches['team1']==team_t]
            gby_t1=piey_t1.groupby(['team2'],as_index=False)['id'].count().sort_values(by='team2',ascending=False).reset_index(drop=True)

            gby_t2=piey_t2.groupby(['team1'],as_index=False)['id'].count().sort_values(by='team1',ascending=False).reset_index(drop=True)
            hyyy=gby_t1.rename(columns={'team2':'team1'})

            concaaa=pd.concat([hyyy,gby_t2],ignore_index=True)
            conca=pd.concat([piey_t1,piey_t2],ignore_index=True)
            fi_gby_t=concaaa.groupby(['team1'],as_index=False)['id'].sum().sort_values(by='id',ascending=False).reset_index(drop=True)
            per_win_t=fi_gby_t.merge(new_new_gb[['team1','win']], on='team1',how='left')
            final_gby_t=per_win_t.fillna(0)
            per_cent_t=(final_gby_t['win']/final_gby_t['id'])*100
            final_gby_t['per_cent']=per_cent_t
            final_gby_t['per_cent']=final_gby_t['per_cent'].astype(int)
            final_gby_t['per_cent']=final_gby_t['per_cent'].astype(str)
            final_gby_t['win']=final_gby_t['win'].astype(int)
            final_gby_t['label']=(final_gby_t['team1'])+' '+(final_gby_t['per_cent'])+'%'

            datafroom=pd.DataFrame(final_gby_t[['label','win']])  
        # st.write(datafroom)

            pie_cart=px.pie(datafroom,
                            title="Win% Against opposition",
                            values="win",
                            names="label",
                            width=450,
                            height=450)  
            st.plotly_chart(pie_cart)

    myearr=matches[matches['year']==year_year]
    team_option1=myearr['team1'].unique().tolist()
    
    if year_year!="All":

        with co2:
            team_tt= st.selectbox("Teams",team_option1)

        def win(team):
            rcbmyearwon=myearr[myearr['winner']==team]
            play1=myearr[myearr['team1']==team]
            play2=myearr[myearr['team2']==team]
            noteam2=play2['team2'].count()
            noteam1=play1['team1'].count()
            t_m_played=noteam1+noteam2
            loss_team=t_m_played-(rcbmyearwon.shape[0])
            winningpercent=((rcbmyearwon.shape[0])/(t_m_played))*100
            losspercent=(((t_m_played)-(rcbmyearwon.shape[0]))/(t_m_played))*100
            c1,c2,c3,c4,c5=st.columns(5)
            with c1:
                st.subheader("Matches Played")
                st.subheader(t_m_played)

            with c2:
                st.subheader("Matches won")
                st.subheader(rcbmyearwon.shape[0])
            with c3:
                st.subheader("Matches Loss")
                st.subheader(loss_team)
            with c4:
                st.subheader("Win Percentage")
                st.subheader(f'{math.ceil(winningpercent)}%')
            with c5:
                st.subheader("Loss Percentage")
                st.subheader(f'{math.floor(losspercent)}%')
        
        funcall=win(team_tt)

        pie=myearr[myearr['winner']==team_tt]
        gb=pie.groupby(['team1'],as_index=False)['id'].count().sort_values(by='team1',ascending=False).reset_index(drop=True)
        gbg=pie.groupby(['team2'],as_index=False)['id'].count().sort_values(by='team2',ascending=False).reset_index(drop=True)
        gbg1=pd.DataFrame(gbg)
        hy=gbg1.rename(columns={'team2':'team1'})
        con=pd.concat([gb,hy],ignore_index=True)
        fi_gb=con.groupby(['team1'],as_index=False)['id'].sum().sort_values(by='id',ascending=False).reset_index(drop=True)
        new_gb=fi_gb.drop(0)
        new_new_gb=new_gb.rename(columns={'id':'win'}) 
        # st.write(new_new_gb)
        coll1,coll2,coll3=st.columns(3)
        with coll3:  
            piey_t2=myearr[myearr['team2']==team_tt]
            piey_t1=myearr[myearr['team1']==team_tt]
            gby_t1=piey_t1.groupby(['team2'],as_index=False)['id'].count().sort_values(by='team2',ascending=False).reset_index(drop=True)

            gby_t2=piey_t2.groupby(['team1'],as_index=False)['id'].count().sort_values(by='team1',ascending=False).reset_index(drop=True)
            hyyy=gby_t1.rename(columns={'team2':'team1'})

            concaaa=pd.concat([hyyy,gby_t2],ignore_index=True)
            conca=pd.concat([piey_t1,piey_t2],ignore_index=True)
            fi_gby_t=concaaa.groupby(['team1'],as_index=False)['id'].sum().sort_values(by='id',ascending=False).reset_index(drop=True)
            per_win_t=fi_gby_t.merge(new_new_gb[['team1','win']], on='team1',how='left')
            final_gby_t=per_win_t.fillna(0)
            per_cent_t=(final_gby_t['win']/final_gby_t['id'])*100
            final_gby_t['per_cent']=per_cent_t
            final_gby_t['per_cent']=final_gby_t['per_cent'].astype(int)
            final_gby_t['per_cent']=final_gby_t['per_cent'].astype(str)
            final_gby_t['win']=final_gby_t['win'].astype(int)
            final_gby_t['label']=(final_gby_t['team1'])+' '+(final_gby_t['per_cent'])+'%'

            datafroom=pd.DataFrame(final_gby_t[['label','win']])  
            # st.write(datafroom)

            pie_cart=px.pie(datafroom,
                            title="Win% Against opposition",
                            values="win",
                            names="label",
                            width=450,
                            height=450)  
            st.plotly_chart(pie_cart)

        with coll2: 

            to=myearr[myearr['toss_decision']=='bat']
            too=to[to['winner']==team_tt]  
            tof=myearr[myearr['toss_decision']=='field']
            toof=tof[tof['winner']==team_tt]
            toss=pd.DataFrame({'A':[too.shape[0],toof.shape[0]],
                        'B':["Bat","Field"]})  
        # st.write(datafroom)

            pie_cart1=px.pie(toss,
                            title=f"            Matches Won By \n Toss Decision",
                            values="A",
                            names="B",
                            width=370,
                            height=370)
            st.plotly_chart(pie_cart1)

        with coll1:
            tor=myearr[myearr['result']=='runs']
            toor=tor[tor['winner']==team_tt]
            tofr=myearr[myearr['result']=='wickets']
            toofr=tofr[tofr['winner']==team_tt]
            tossr=pd.DataFrame({'A':[toor.shape[0],toofr.shape[0]],
                        'B':["Win By Runs","Win By Wickets"]})  
            pie_cart2=px.pie(tossr,
                            title=f"Matches Won By \n Runs/Wickets",
                            values="A",
                            names="B",
                            width=400,
                            height=400)
            st.plotly_chart(pie_cart2)

with tab2:
    team_optionn=matches['team1'].unique().tolist()
    # year_optionn=matches['year'].unique().tolist()
    year_optionn1=matches['year'].unique().tolist()
    year_optionn1.reverse()
    cc1,cc2,cc3=st.columns([1,3,3])
    with cc1:
          year_year1=st.selectbox("Year1",year_optionn1) 
    
    filter_year=balls[balls["year"]==year_year1]
    # st.write(filter_year)
    battingt=filter_year['batting_team'].unique()
    bowlingt=filter_year['bowling_team'].unique()
    ccc1,ccc2,ccc3,ccc4=st.columns([1.8,0.5,1.8,4])
    with ccc1:
        inn_1=st.selectbox("1st Inning",battingt)
        # st.write("Mumbai Indians")
    with ccc2:
        st.header(f"( Vs )")          
    with ccc3:
        inn_2=st.selectbox("2nd Inning",bowlingt)
        # st.write("Mumbai Indians")
   # if inn_1==inn_2:
    #    st.subheader("You have selected both the team same")
     #   st.caption("There is need to change your one of the inning_team to get the team scorecard ")
    
    try:
        if inn_1==inn_2:
            st.subheader("You have selected both the team same🤨")
            st.info("There is need to change your one of the inning_team to get the team scorecard ")       
    except:
        st.write("Done")

        
    
    
    def filter1(bt,bl):
        tud=filter_year["batting_team"]==bt
        tug=filter_year["bowling_team"]==bl
        tuu=filter_year["batting_team"]==bl
        tuv=filter_year["bowling_team"]==bt
        tuf=filter_year[tud & tug]
        tuw=filter_year[tuu & tuv]
        tuz=tuf.append(tuw)
        return(tuz)

    sor=filter1(inn_1,inn_2)
    no_m=sor['id'].unique().tolist()
    with ccc4:
        num_m=st.selectbox("select match",no_m)
    def Individual_match1(id):
             qe=sor[sor["id"]==id]
             return(qe)
    verses=Individual_match1(num_m)
    # st.write(verses.shape)
    ccl1,ccl2,ccl3,ccl4=st.columns([1.8,0.5,1.8,4])


    with ccl1:
        if (verses['toss_winner'].iat[0]==inn_1) & (verses['toss_decision'].iat[0]=="bat"):
            first_inn=1
        elif (verses['toss_winner'].iat[0]==inn_2) & (verses['toss_decision'].iat[0]=="field"):
            first_inn=1
        else:
            first_inn=2
        if first_inn==1:
            inn111=verses[verses['inning']==1]
            inni1=inn111[inn111['extras_type']!='wides']
            tq11=inni1.groupby(['batsman'],as_index=False)['inning'].count()
            tq1=inn111.groupby(['batsman',],as_index=False)['batsman_runs'].sum().sort_values(by='batsman_runs',ascending=True).reset_index(drop=True)
            runball1=pd.merge(tq1,tq11)
            runball1=runball1.rename(columns={'batsman':'Batsman','batsman_runs':'Run','inning':'Ball'},inplace=False)
            st.write(runball1)
            
    
        else:
            inn222=verses[verses['inning']==2]
            inni2=inn222[inn222['extras_type']!='wides']
            tq12=inni2.groupby(['batsman'],as_index=False)['inning'].count()
            tq2=inn222.groupby(['batsman'],as_index=False)['batsman_runs'].sum().sort_values(by='batsman_runs',ascending=True).reset_index(drop=True)
            runball2=pd.merge(tq2,tq12)
            runball2=runball2.rename(columns={'batsman':'Batsman','batsman_runs':'Run','inning':'Ball'},inplace=False)
            st.write(runball2)
        


    with ccl3:
        if (verses['toss_winner'].iat[0]==inn_2) & (verses['toss_decision'].iat[0]=="bat"):
            first_inn=1
        elif (verses['toss_winner'].iat[0]==inn_1) & (verses['toss_decision'].iat[0]=="field"):
            first_inn=1
        else:
            first_inn=2
        if first_inn==1:
            inn111=verses[verses['inning']==1]
            inni1=inn111[inn111['extras_type']!='wides']
            tq11=inni1.groupby(['batsman'],as_index=False)['inning'].count()
            tq1=inn111.groupby(['batsman',],as_index=False)['batsman_runs'].sum().sort_values(by='batsman_runs',ascending=True).reset_index(drop=True)
            runball1=pd.merge(tq1,tq11)
            runball1=runball1.rename(columns={'batsman':'Batsman','batsman_runs':'Run','inning':'Ball'},inplace=False)
            st.write(runball1)
            
    
        else:
            inn222=verses[verses['inning']==2]
            inni2=inn222[inn222['extras_type']!='wides']
            tq12=inni2.groupby(['batsman'],as_index=False)['inning'].count()
            tq2=inn222.groupby(['batsman'],as_index=False)['batsman_runs'].sum().sort_values(by='batsman_runs',ascending=True).reset_index(drop=True)
            runball2=pd.merge(tq2,tq12)
            runball2=runball2.rename(columns={'batsman':'Batsman','batsman_runs':'Run','inning':'Ball'},inplace=False)
            st.write(runball2)
    with ccl4:

        
        if (verses['toss_winner'].iat[0]==inn_1) & (verses['toss_decision'].iat[0]=="bat"):
            first_inn=1
        elif (verses['toss_winner'].iat[0]==inn_2) & (verses['toss_decision'].iat[0]=="field"):
            first_inn=1
        else:
            first_inn=2
        if first_inn==1:
            inn111=verses[verses['inning']==1] 
            st.subheader(f"{inn_1} Total Score => {inn111['total_runs'].sum()}")
        else:
            inn222=verses[verses['inning']==2]
            st.subheader(f"{inn_1} Total Score => {inn222['total_runs'].sum()}")

        if (verses['toss_winner'].iat[0]==inn_2) & (verses['toss_decision'].iat[0]=="bat"):
            first_inn=1
        elif (verses['toss_winner'].iat[0]==inn_1) & (verses['toss_decision'].iat[0]=="field"):
            first_inn=1
        else:
            first_inn=2
        if first_inn==1:
            inn111=verses[verses['inning']==1] 
            st.subheader(f"{inn_2} Total Score => {inn111['total_runs'].sum()}")
        else:
            inn222=verses[verses['inning']==2]
            st.subheader(f"{inn_2} Total Score => {inn222['total_runs'].sum()}")

        pl_of_mat=verses['player_of_match'].iat[0]
        st.subheader(f"Player Of The Match => {pl_of_mat}")
        
        a=verses['toss_decision'].iat[0]
        if (verses['toss_winner'].iat[0]==inn_1):
            st.subheader(f"{inn_1} Won toss, elected to {a} first ")
        else:
            st.subheader(f"{inn_2} Won toss, elected to {a} first ")

        st.subheader(f"Venue of the Match => {verses['venue'].iat[0]}")
with tab3:
    teams = ['Sunrisers Hyderabad',
    'Mumbai Indians',
    'Royal Challengers Bangalore',
    'Kolkata Knight Riders',
    'Kings XI Punjab',
    'Chennai Super Kings',
    'Rajasthan Royals',
    'Delhi Capitals']

    cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
        'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
        'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
        'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
        'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
        'Sharjah', 'Mohali', 'Bengaluru']

    pipe = pickle.load(open('pipe.pkl','rb'))
    st.title('IPL Win Predictor')

    col1, col2 = st.columns(2)

    with col1:
        batting_team = st.selectbox('Select the batting team',sorted(teams))
    with col2:
        bowling_team = st.selectbox('Select the bowling team',sorted(teams))

    selected_city = st.selectbox('Select host city',sorted(cities))

    target = st.number_input('Target')

    col3,col4,col5 = st.columns(3)

    with col3:
        score = st.number_input('Score')
    with col4:
        overs = st.number_input('Overs completed')
    with col5:
        wickets = st.number_input('Wickets out')

    if st.button('Predict Probability'):
        runs_left = target - score
        balls_left = 120 - (overs*6)
        wickets = 10 - wickets
        crr = score/overs
        rrr = (runs_left*6)/balls_left

        input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wickets':[wickets],'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})

        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]
        st.header(batting_team + "- " + str(round(win*100)) + "%")
        st.header(bowling_team + "- " + str(round(loss*100)) + "%")
    
