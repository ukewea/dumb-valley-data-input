import urllib.request
import sys
import getopt
import datetime
import os
import time

def get_daily_data(root_dir, begin_date):
    begin_date_obj = datetime.datetime.strptime(begin_date, '%Y-%m-%d').date()
    print(begin_date_obj)

    d1 = datetime.date.today()
    day_delta = (d1 - begin_date_obj).days
    print(f"Get {day_delta} days of data")

    for i in range(0, day_delta + 1):
        date = begin_date_obj + datetime.timedelta(days=i)
        year = date.strftime("%Y")
        year_republic = int(year) - 1911
        month = date.strftime("%m")
        day = date.strftime("%d")

        date_str=f"{year}-{month}-{day}"
        date_str_without_separator=f"{year}{month}{day}"
        date_republic=f"{year_republic}/{month}/{day}"

        job1 = (
            "上櫃股票個股本益比、殖利率、股價淨值比(依日期查詢)",
            f'https://www.tpex.org.tw/web/stock/aftertrading/peratio_analysis/pera_result.php?l=zh-tw&o=csv&charset=UTF-8&d={date_republic}&c=&s=5,desc',
            os.path.join(root_dir, "TPEX-PeRatio_Pbr", f"pera_{date_str}.csv"),
        )

        job2 = (
            "上櫃股票行情",
            f'https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&o=csv&d={date_republic}&s=0,asc,0',
            os.path.join(root_dir, "TPEX-DailyQuotes", f"DailyQuotes_{date_str}.csv"),
        )

        job3 = (
            "上櫃處置有價證券資訊",
            f'https://www.tpex.org.tw/web/bulletin/disposal_information/disposal_information_download.php?l=zh-tw&sd={date_republic}&ed={date_republic}&code=&choice_type=all_category&stk_cotegory=-1&disposal_measure=-1&group_type=group_stk',
            os.path.join(root_dir, "TPEX-TradingAttentionInformation", f"trading_attention_information_{date_str}.csv"),
        )

        job4 = (
            "上櫃股票個股週轉率排行",
            f'https://www.tpex.org.tw/web/stock/aftertrading/daily_turnover/trn_result.php?l=zh-tw&t=D&d={date_republic}&s=0,asc,1&o=csv',
            os.path.join(root_dir, "TPEX-DailyTurnOver", f"STK_TURN_{date_str}.csv"),
        )

        job5 = (
            "臺灣證券交易所 - 每日收盤行情",
            f"https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date={date_str_without_separator}&type=ALLBUT0999",
            os.path.join(root_dir, "TWSE-DailyQuotes", f"MI_INDEX_ALLBUT0999_{date_str}.csv"),
        )

        job6 = (
            "臺灣證券交易所 - 個股日本益比、殖利率及股價淨值比",
            f"https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date={date_str_without_separator}&selectType=ALL",
            os.path.join(root_dir, "TWSE-PeRatio_Pbr", f"BWIBBU_d_ALL_{date_str}.csv"),
        )

        job7 = (
            "臺灣證券交易所 - 公告注意股票股票資訊",
            f"https://www.twse.com.tw/announcement/notice?response=csv&startDate={date_str_without_separator}&endDate={date_str_without_separator}&stockNo=&sortKind=STKNO&querytype=1&selectType=",
            os.path.join(root_dir, "TWSE-TradingAttentionInformation", f"notice_{date_str}.csv"),
        )

        job8 = (
            "櫃買指數暨產業分類指數(日查詢)",
            f"https://www.tpex.org.tw/web/stock/aftertrading/all_daily_index/sectinx_download.php?l=zh-tw&d={date_republic}&s=undefined",
            os.path.join(root_dir, "TPEX-DailyIndex", f"OSECTINX_{date_str}.csv"),
        )

        job9 = (
            "櫃買指數成分股",
            f"https://www.tpex.org.tw/web/stock/iNdex_info/index/consti_result.php?l=zh-tw&d={date_republic}&s=0,asc,0&o=csv",
            os.path.join(root_dir, "TPEX_Consti", f"CONSTI_{date_str}.csv"),
        )

        print(f"Downloading data on {date_str}")

        jobs = [job1, job2, job3, job4, job5, job6, job7, job8, job9]
        #jobs = [job8, job9]

        for j in jobs:
            title = j[0]
            url = j[1]
            dest = j[2]
            print(f"Download {title} on {date_str}")
            filedata = urllib.request.urlopen(url)
            datatowrite = filedata.read()

            with open(dest, 'wb') as f:
                f.write(datatowrite)
            print(f"Saved to {dest}")
            time.sleep(5)

        print("\n")

def main():
    print(sys.argv)
    print(sys.argv[1:])
    try:
        opts, args = getopt.getopt(sys.argv[1:], "r:d:", ["root=", "date-begin="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)

    for name, value in opts:
        if name in ('-r', '--root'):
            root = value
        elif name in ('-d', '--date-begin'):
            date = value

    get_daily_data(root.strip(), date.strip())

if __name__ == '__main__':
    main()