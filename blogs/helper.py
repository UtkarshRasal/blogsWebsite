import pandas as pd
import os
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from datetime import datetime

def file_path(request):
    file = request.FILES['file']
    path = os.path.join("uploads", file.name)
 
    return path

def generate_blogs_report(data) -> pd.DataFrame:
        
    data_cols = ['id', 'user', 'title', 'content', 'tags', 'media_file', 'created_at']
    df = pd.DataFrame.from_dict(data).reindex(columns=data_cols)

    return df

def generate_comments_report(data) -> pd.DataFrame:
        
    data_cols = ['id', 'title', 'comments_count', 'comment']
    df = pd.DataFrame.from_dict(data).reindex(columns=data_cols)
    
    return df

def generate_likes_report(data) -> pd.DataFrame:
        
    data_cols = ['id', 'title', 'likes_count', 'likes']
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
