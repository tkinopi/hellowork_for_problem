from scr import*

def main():
    urls = ['https://www.hellowork.mhlw.go.jp/kensaku/GECA110010.do?screenId=GECA110010&action=dispDetailBtn&kJNo=2707007864841&kJKbn=1&jGSHNo=V4MTZKzXtQ%2F3PbI5Eoas8Q%3D%3D&fullPart=1&iNFTeikyoRiyoDtiID=&kSNo=&newArrived=&tatZngy=1&shogaiKbn=0', 'https://www.hellowork.mhlw.go.jp/kensaku/GECA110010.do?screenId=GECA110010&action=dispDetailBtn&kJNo=2711002773441&kJKbn=1&jGSHNo=%2B8aVNBsR6Vljzq1mGukWvw%3D%3D&fullPart=1&iNFTeikyoRiyoDtiID=&kSNo=&newArrived=&tatZngy=1&shogaiKbn=0']
    nested_urls = get_urls()
    # Flatten the list using a list comprehension
    flat_urls = [url for sublist in nested_urls for url in sublist]
    print(flat_urls)
    # flat_urls = get_sheet_a_data()
    jobs = []
    for url in flat_urls:
        result_dict = get_job_info(url)
        jobs.append(result_dict)
    print(jobs)
    write_to_spreadsheet(jobs)


if __name__ == "__main__":
    main()