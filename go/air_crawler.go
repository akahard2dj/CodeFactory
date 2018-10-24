package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"regexp"
	"strconv"
	"strings"

	"github.com/labstack/echo"

	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/mysql"
	"golang.org/x/text/encoding/korean"

	//go get -u golang.org/x/text/...
	//http://blog.suapapa.net/post/handling_cp949_in_go/

	"github.com/PuerkitoBio/goquery"
)

type Observatory struct {
	AWSCode      int32
	AWSType      string
	AWSName      string
	AWSLongitude float64
	AWSLatitude  float64
}

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

type WeatherData struct {
	ID                  uint    `json:"id"`
	TagDate             string  `json:"tag_date"`
	ObsName             string  `json:"obs_name"`
	WindDirection       float64 `json:"wind_dir"`
	WindDirectionString string  `json:"wind_dir_str"`
	WindSpeed           float64 `json:"wind_speed"`
	Temperature         float64 `json:"temp"`
	Precipitation       float64 `json:"preci"`
	Humidity            float64 `json:"hum"`
}

func StringToFloat(strValue string) float64 {
	val, err := strconv.ParseFloat(strValue, 64)
	if err == nil {
		return val
	} else {
		return -999
	}
}

func WeatherDataScrape(db *gorm.DB) {
	resp, err := http.Get("http://aws.seoul.go.kr/RealTime/RealTimeWeatherUser.asp?TITLE=%C0%FC%20%C1%F6%C1%A1%20%C7%F6%C8%B2")
	if err != nil {
		log.Fatal(err)
	}

	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		log.Fatalf("status code error: %d %s", resp.StatusCode, resp.Status)
	}

	bytes, err := ioutil.ReadAll(resp.Body)
	euckrDecoder := korean.EUCKR.NewDecoder()
	decodedContents, err := euckrDecoder.String(string(bytes))

	doc, err := goquery.NewDocumentFromReader(strings.NewReader(decodedContents))
	if err != nil {
		log.Fatal(err)
	}

	timeItems := strings.Fields(doc.Find(".top tbody tr tbody tr td").Eq(1).Text())
	re := regexp.MustCompile("[0-9]+")

	year := re.FindAllString(timeItems[0], -1)
	month := re.FindAllString(timeItems[1], -1)
	day := re.FindAllString(timeItems[2], -1)
	hour := re.FindAllString(timeItems[3], -1)

	tagDate := fmt.Sprintf("%s-%s-%s %s:00", year[0], month[0], day[0], hour[0])

	queryResult := WeatherData{}
	db.Where("tag_date = ?", tagDate).First(&queryResult)
	var doScrape bool
	if queryResult.ID == 0 {
		doScrape = true
	} else {
		doScrape = false
	}

	if doScrape {
		items := doc.Find(".top .main tr td table tbody tr")
		for i := 1; i < 27; i++ {
			replacedItem := strings.Replace(items.Eq(i).Text(), "\n", "", -1)
			listSubItem := strings.Fields(replacedItem)

			obsName := listSubItem[1] + "구"
			windDirection := StringToFloat(listSubItem[2])
			windDirectionString := listSubItem[3]
			windSpeed := StringToFloat(listSubItem[4])
			temperature := StringToFloat(listSubItem[5])
			precipitation := StringToFloat(listSubItem[6])
			humidity := StringToFloat(listSubItem[8])

			obs := WeatherData{}
			obs.TagDate = tagDate
			obs.ObsName = obsName
			obs.WindDirection = windDirection
			obs.WindDirectionString = windDirectionString
			obs.WindSpeed = windSpeed
			obs.Temperature = temperature
			obs.Precipitation = precipitation
			obs.Humidity = humidity

			db.NewRecord(obs)
			db.Create(&obs)
			fmt.Println(obsName, windDirection, windDirectionString, windSpeed, temperature, precipitation, humidity)
		}
	}
}

func AirPollutionScrape(db *gorm.DB) {
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
		for i := 1; i < len(items.Nodes); i++ {
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
			db.NewRecord(obs)
			db.Create(&obs)

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

	/*
		if !db.HasTable(&AirPollution{}) {
			db.CreateTable(&AirPollution{})
		}

		if !db.HasTable(&WeatherData{}) {
			db.CreateTable(&WeatherData{})
		}

		//if !db.HasTable(&Observatory{}) {
		//	db.CreateTable(&Observatory{})
		//}

		AirPollutionScrape(db)
		WeatherDataScrape(db)
	*/
	e := echo.New()
	e.GET("/", func(c echo.Context) error {
		log.Println("OK")
		return c.String(http.StatusOK, "Hello, World!")
	})
	e.Logger.Fatal(e.Start(":1323"))
}
