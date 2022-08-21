from pandas import read_csv


def upload_csv_file(title, container, df=None):
    uploaded = container.file_uploader(title, type="csv")

    if uploaded is not None:
        df = read_csv(uploaded, encoding="latin-1", na_values=["NaVal"])

    return uploaded, df


def get_statistics_as_markdown(file, df):
    text = "- Filename: **{}** ({:1} KB)\n".format(file.name, file.size / 1000)
    text += "- DataFrame shape: {}".format(df.shape)

    return text
