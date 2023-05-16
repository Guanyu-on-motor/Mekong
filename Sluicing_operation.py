#import necessary modules
import pandas as pd

#input csv_file with data on simulated sediment and discharge

df=pd.read_csv(csv_file,sep=',',parse_dates=['Date'],dayfirst=True,index_col=['Date'])
wet_season=df.loc['2021-06-01':'2021-10-01'] #only consider wet-season


def q_released(wet_season_df,Ndays,start_date):
    '''
    function calculates how much water(km3) will be released
    input:
        wet_seson_df: wet season dataframe{pandas dataframe}
        Ndays: number of days in sluicing operation (integer)
        start_date: start date of sluicing operation (string in 'yyyy-mm-dd' format)
    '''
    end_date = pd.to_datetime(start_date) + pd.DateOffset(days=Ndays)
    sluicing_df = wet_season_df.loc[start_date:end_date] #create df with only dates that sluicing takes place
    
    #calculate discharge released in km3
    q_released=abs(sluicing_df['Water released (Mm3/d)'].sum()/1000)
    return q_released

def storage (wet_season_df,Ndays,start_date,active_storage):
    '''
    function determines percentage of active storage will be filled at the end of wet-season (after sluicing has taken place)
    input:
        wet_seson_df: wet season dataframe{pandas dataframe}
        Ndays: number of days in sluicing operation (integer)
        start_date: start date of sluicing operation (string in 'yyyy-mm-dd' format)
        active_storage: amount of active storage in the reservoirs (float)
    '''
    end_date = pd.to_datetime(start_date) + pd.DateOffset(days=Ndays)
    sluicing_df = wet_season_df.loc[start_date:end_date]
    
    non_sluicing = wet_season.loc[~wet_season.index.isin(sluicing_df.index)]
    #calculate water in storage after end of wet season in km3
    filled_storage=abs(non_sluicing['Water released (Mm3/d)'].sum()/1000)
    #get percentage of active storage
    active_storage_percent=filled_storage/active_storage*100
    return active_storage_percent
    
def sed_released(wet_season_df,Ndays,start_date,dead_storage,TE_alpha):
    '''
    function calculates how much sediment (Mt) will be released
    input:
        wet_seson_df: wet season dataframe{pandas dataframe}
        Ndays: number of days in sluicing operation (integer)
        start_date: start date of sluicing operation (string in 'yyyy-mm-dd' format)
        dead_storage: amount of dead storage in the reservoirs (float)
        TE_alpha: pre-determined constant to determine trapping efficiency of reservoirs (float)
    '''
    end_date = pd.to_datetime(start_date) + pd.DateOffset(days=Ndays)
    sluicing_df = wet_season_df.loc[start_date:end_date]
    
    #calculate storage at start of sluicing in km3
    pre_sluicing=wet_season.loc[:start_date]
    pre_storage=abs(pre_sluicing['Water released (Mm3/d)'].sum()/1000)+dead_storage
    def trap_eff(a_value,storage,Q_cms):
        #note that Q in cms, storage is pre_sluice storage in km3
        RS=(storage*1000)/Q_cms
        try:
            return 1-(a_value/RS** 0.5)
        except:
            return 0.999

    def sed_released(SSC,Q,TE):
        #note that Q in cms, SSC in kt/Mm3
        #return in kt/day
        return SSC*(Q*3600*24/1e6)*(1-TE)
    
    #calculate sediment released in Mt
    sluicing_df['TE']=sluicing_df.apply(lambda y:trap_eff(TE_alpha,pre_storage,y['Qsim (cms)']),axis=1)
    sluicing_df['SL_released (kt)'] = sluicing_df.apply(lambda x: sed_released(x['SSCsim (kt/Mm3)'],x['Qsim (cms)'],x['TE']), axis=1)
    tot_SL_released=abs(sluicing_df['SL_released (kt)'].sum()/1000)
    
    return tot_SL_released



print(f"discharge released is{q_released(wet_season,Ndays=120,start_date='2021-06-01')} km3")
print(f"storage filled is{storage(wet_season,Ndays=120,start_date='2021-06-01',active_storage=25.24)}%")
print(f"sediment released is{sed_released(wet_season,Ndays=78,start_date='2021-07-15',dead_storage=19.2,TE_alpha=0.48)} Mt")

