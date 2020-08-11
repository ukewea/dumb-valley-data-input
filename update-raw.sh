#!/bin/bash

DIR=`pwd`

function get_daily_data {
  if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    date_start=$(date --utc --date "$1" +%s)
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    date_start=$(date -u -j -f "%Y-%m-%d %H:%M:%S" "$1 00:00:00" +"%s")
  else
    echo "Unknown OS type"
    exit 123
  fi

  if [[ $? != 0 ]]; then
    echo "Invalid date format"
    exit $?
  fi

  if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    date_end=$(date --utc --date "" +%s)
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    date_end=$(date -j -u -f "%H:%M:%S" "00:00:00" "+%s")
  fi

  diffSec=$((date_end-date_start))
  if ((diffSec < 0)); then abs=-1; else abs=1; fi

  diff_day=$((diffSec/86400*abs))
  i=$diff_day
  echo diff day is $i

  # 從最早的日期開始遞增下載
  for (( ; ; ))
    do
      if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        year=$(date -d "$i days ago" +"%Y")
        year_republic=$(( $year-1911 ))
        month=$(date -d "$i days ago" +"%m")
        day=$(date -d "$i days ago" +"%d")
      elif [[ "$OSTYPE" == "darwin"* ]]; then
        year=$(date -v-"$i"d +"%Y")
        year_republic=$(( $year-1911 ))
        month=$(date -v-"$i"d +"%m")
        day=$(date -v-"$i"d +"%d")
      fi

      date_str="$year-$month-$day"
      date_str_without_separator="$year$month$day"
      date_republic="$year_republic/$month/$day"

      echo "Downloading data on $date_str"

      echo "Download 上櫃股票個股本益比、殖利率、股價淨值比(依日期查詢)"
      url1='https://www.tpex.org.tw/web/stock/aftertrading/peratio_analysis/pera_result.php?l=zh-tw&o=csv&charset=UTF-8&d='"$date_republic"'&c=&s=5,desc'
      echo "URL is $url1"
      curl "$url1" > "TPEX-PeRatio_Pbr/pera_""$date_str"".csv"

      sleep 5

      echo "Download 上櫃股票行情"
      url2='https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&o=csv&d='$date_republic'&s=0,asc,0'
      echo "URL is $url2"
      curl "$url2" > "TPEX-DailyQuotes/DailyQuotes_$date_str.csv"

      sleep 5

      echo "Download 上櫃處置有價證券資訊"
      url3='https://www.tpex.org.tw/web/bulletin/disposal_information/disposal_information_download.php?l=zh-tw&sd='$date_republic'&ed='$date_republic'&code=&choice_type=all_category&stk_cotegory=-1&disposal_measure=-1&group_type=group_stk'
      echo "URL is $url3"
      curl "$url3" > "TPEX-TradingAttentionInformation/trading_attention_information_$date_str.csv"

      sleep 5

      echo "Download 上櫃股票個股週轉率排行"
      url4='https://www.tpex.org.tw/web/stock/aftertrading/daily_turnover/trn_result.php?l=zh-tw&t=D&d='$date_republic'&s=0,asc,1&o=csv'
      echo "URL is $url4"
      curl "$url4" > "TPEX-DailyTurnOver/STK_TURN_$date_str.csv"

      sleep 5

      echo "Download 臺灣證券交易所 - 每日收盤行情"
      url5="https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date="$date_str_without_separator"&type=ALLBUT0999"
      echo "URL is $url5"
      curl "$url5" > "TWSE-DailyQuotes/MI_INDEX_ALLBUT0999_"$date_str".csv"

      sleep 5

      echo "Download 臺灣證券交易所 - 個股日本益比、殖利率及股價淨值比"
      url6="https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date="$date_str_without_separator"&selectType=ALL"
      echo "URL is $url6"
      curl "$url6" > "TWSE-PeRatio_Pbr/BWIBBU_d_ALL_"$date_str".csv"

      sleep 5

      echo "Download 臺灣證券交易所 - 公告注意股票股票資訊"
      url7="https://www.twse.com.tw/announcement/notice?response=csv&startDate="$date_str_without_separator"&endDate="$date_str_without_separator"&stockNo=&sortKind=STKNO&querytype=1&selectType="
      echo "URL is $url7"
      curl "$url7" > "TWSE-TradingAttentionInformation/notice_"$date_str".csv"

      echo ''

      i=$(($i-1))
      if [ "$i" -lt 0 ]; then
        break
      fi

      sleep 5
  done
}

get_daily_data $1

exit 0
