import requests

from bs4 import BeautifulSoup


def get_content(url):
    res = requests.get(url)
    page_content = res.content.decode("utf-8")
    return page_content


def save_download_file(content, file_name):
    with open(file_name, "wb") as f:
        f.write(content)
    print("File saved!")


def get_data_source_from_lws(file_index, save=False, save_file_name="file.csv"):
    """Get file source from learnwithshin."""
    url = "https://learnwithshin.github.io/docs/files/"
    content = get_content(url)
    soup = BeautifulSoup(content, "html.parser")
    article = soup.find("article")
    anchors = article.find_all("a")

    base_url = "https://learnwithshin.github.io/docs/"
    target_anchor = anchors[file_index]
    file_url = target_anchor["href"]
    file_url = file_url.replace("../", base_url)

    res = requests.get(file_url)
    if save:
        save_download_file(res.content, save_file_name)
    return res.content


def content_to_df(bytes_content):
    file_obj = io.BytesIO(bytes_content)
    return pd.read_csv(file_obj)


if __name__ == "__main__":
    get_data_source_from_lws(file_index=0, save=True, save_file_name="countries.csv")
    get_data_source_from_lws(file_index=1, save=True, save_file_name="vacc_data.csv")