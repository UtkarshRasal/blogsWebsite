def download_survey_report(self, request, queryset):
        """
        Action function to download survey report in the form of csv
        """
        # call to generate survey report to get data in pandas dataframe
        df = generate_survey_report()
        # return the csv response with file name being namescope-timestamp.csv
        return return_csv_response(df, "survey-tracker")

def return_csv_response(df: pd.DataFrame, namescope: str) -> HttpResponse:
    """
    Function for returning csv as a response for reports
    Args:
        - df: pandas dataframe which needs to be output as csv
        - namescope: namescope for the reports
    return:
        - HTTPResponse in a form of csv file
    """
    filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    response = HttpResponse(content_type='text/csv')
    response[
        'Content-Disposition'] = f'attachment; filename="{namescope}-{filename}.csv"'
    df.to_csv(path_or_buf=response, index=False)
    return response
