package main

import (
	"fmt"
	"log"
	"net/http"
	"strconv"
	"strings"

	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/mysql"

	"github.com/PuerkitoBio/goquery"
)

type AirPollution struct {
	ID       uint
	TagDate  string
	ObsName  string
	ItemPM10 float64
	ItemPM25 float64
	ItemO3   float64
	ItemNO2  float64
	ItemCO   float64
	ItemSO2  float64
}

func StringToFloat(strValue string) float64 {
	val, err := strconv.ParseFloat(strValue, 64)
	if err == nil {
		return val
	} else {
		return -999
	}
}

func AirPollutionScarpe(db *gorm.DB) {
	resp, err := http.Get("http://cleanair.seoul.go.kr/air_city.htm?method=measure&grp1=pm10")
	if err != nil {
		log.Fatal(err)
	}

	defer resp.Body.Close()
	if resp.StatusCode != 200 {
		log.Fatalf("status code error: %d %s", resp.StatusCode, resp.Status)
	}

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	items := doc.Find(".tbl2 tbody tr")
	ii := strings.Fields(strings.Replace(items.Eq(0).Text(), "\n", "", -1))

	tagDate := ii[0] + " " + ii[1]
	fmt.Printf(tagDate)

	queryResult := AirPollution{}
	db.Where("tag_date = ?", tagDate).First(&queryResult)
	var doScrape bool
	if queryResult.ID == 0 {
		doScrape = true
	} else {
		doScrape = false
	}

	if doScrape {
		for i := 1; i < len(items.Nodes)-1; i++ {
			time := items.Eq(i).Find("th").Text()
			subItem := items.Eq(i).Find("td")
			replacedSubItem := strings.Replace(subItem.Text(), "\n", "", -1)
			listSubItem := strings.Fields(replacedSubItem)

			obsName := listSubItem[0]
			pm10 := StringToFloat(listSubItem[1])
			pm25 := StringToFloat(listSubItem[2])
			o3 := StringToFloat(listSubItem[3])
			no2 := StringToFloat(listSubItem[4])
			co := StringToFloat(listSubItem[5])
			so2 := StringToFloat(listSubItem[6])
			obs := AirPollution{}
			obs.ObsName = obsName
			obs.TagDate = time
			obs.ItemPM10 = pm10
			obs.ItemPM25 = pm25
			obs.ItemO3 = o3
			obs.ItemNO2 = no2
			obs.ItemCO = co
			obs.ItemSO2 = so2
			//db.NewRecord(obs)
			//db.Create(&obs)

			fmt.Println(time, obsName, pm10, pm25, o3, no2, co, so2)
		}
	}

}

func main() {

	db, err := gorm.Open("mysql", "user:passwd@/database?charset=utf8")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	if !db.HasTable(&AirPollution{}) {
		db.CreateTable(&AirPollution{})
	}

	AirPollutionScarpe(db)
}
