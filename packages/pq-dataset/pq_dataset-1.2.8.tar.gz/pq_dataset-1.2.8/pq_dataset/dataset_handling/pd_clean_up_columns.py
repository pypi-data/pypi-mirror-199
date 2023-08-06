import pandas as pd
import logging
from pq_dataset.logging.DummyLogger import DummyLogger

def pd_clean_up_columns(df) -> pd.DataFrame:
    
    logger = logging.getLogger(__name__) if logging.getLogger().hasHandlers else DummyLogger()        
    logger.debug(f'Started pd_clean_up_columns')
    
    # Drops all columns where all values are null/nan
    df_temp = df.dropna(how='all', axis=1)
    logger.debug(f'Done dropping empty columns')
    # Drops all columns which only contains 0's - multiple choice variables
    df_temp = df_temp.loc[:, (df_temp != 0).any(axis=0)]
    logger.debug(f'Done dropping columns containing only 0 values')
    # Test of unique values in each column
    nb_unique = df_temp.apply(pd.Series.nunique) 
    static_cols = nb_unique[nb_unique==1].index # Cols containing only one value - though NANs as well
    columns_with_nan = df_temp.columns[df_temp.isna().any()].tolist()
    possible_cols = [col for col in static_cols if col not in columns_with_nan]

    # Close your eyes... this is ugly!
    remove_these_cols = []

    for col in possible_cols:
        if col.startswith('background__ptype') and col.endswith('t'):
            if possible_cols.count(col[:-1]) == 1:
                remove_these_cols.append(col[:-1])
                remove_these_cols.append(col)
    
    logger.debug(f'Done removing ptype variables where ptypext is static but ptype is not')

    closed_ptypes = [col for col in df_temp.columns if col.startswith('background__ptype') and col.endswith('c')]
    
    if closed_ptypes:
        remove_these_cols.extend(closed_ptypes)

    df2 = df_temp.drop(columns=remove_these_cols)
    logger.debug(f'pd_clean_up_columns removed {df.shape[1]-df2.shape[1]} columns')
    return df2