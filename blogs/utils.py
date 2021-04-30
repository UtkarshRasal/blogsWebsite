import pandas as pd
import os
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from datetime import datetime

def file_path(request):
    if not request.FILES.get('file'):
        return ''
    media_file = request.FILES['file']
    path = os.path.join("uploads", media_file.name)
 
    return path

def generate_report(data, data_cols) -> pd.DataFrame:
    '''
    generate dataframe for the given data and data_cols

    data - blogs, comments, likes serialized data
    data_cols - columns used in the dataframe

    '''   
    df = pd.DataFrame.from_dict(data).reindex(columns=data_cols)
    return df

def return_csv_response(df: pd.DataFrame, namescope:str) -> HttpResponse:
    '''
    Function for returning csv as a response for the reports
    '''

    file_name = datetime.now().strftime('%y-%m-%d %H-%M-%S')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{namescope}-{file_name}.csv"'
    df.to_csv(path_or_buf=response, index=False)
    
    return response
