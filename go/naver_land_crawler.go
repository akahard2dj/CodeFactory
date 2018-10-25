//https://land.naver.com/article/cityInfo.nhn

package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/PuerkitoBio/goquery"
)

type NaverC1Item struct {
	Name string
	Code string
}

type NaverC2Item struct {
	ParentCode string
	Name       string
	Code       string
}

type NaverC3Item struct {
	ParentCode string
	Name       string
	Code       string
}

type NaverC1 struct {
	Items []NaverC1Item
}

type NaverC2 struct {
	Items []NaverC2Item
}

type NaverC3 struct {
	Items []NaverC3Item
}

func (naverC1 *NaverC1) AddItem(item NaverC1Item) []NaverC1Item {
	naverC1.Items = append(naverC1.Items, item)
	return naverC1.Items
}

func (naverC2 *NaverC2) AddItem(item NaverC2Item) []NaverC2Item {
	naverC2.Items = append(naverC2.Items, item)
	return naverC2.Items
}

func (naverC3 *NaverC3) AddItem(item NaverC3Item) []NaverC3Item {
	naverC3.Items = append(naverC3.Items, item)
	return naverC3.Items
}

func savePage(url string) {
	resp, err := http.Get(url)
	if err != nil {
		log.Panic(err)
	}

	f, err := os.Create("naver.html")
	defer f.Close()
	resp.Write(f)
}

func loadPage(filename string) *goquery.Document {
	f, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	doc, err := goquery.NewDocumentFromReader(f)
	if err != nil {
		log.Fatal(err)
	}

	return doc
}

func loadPageByURL(url string) *goquery.Document {
	resp, err := http.Get(url)
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
	return doc
}

func main() {
	url := "https://land.naver.com/article/cityInfo.nhn"
	//savePage(url)

	doc := loadPage("naver.html")
	items := doc.Find(".selectbox-source.forload").Find("option")

	c1Items := NaverC1{}
	for i := 0; i < len(items.Nodes); i++ {
		if items.Eq(i).Text() == "시⁄군⁄구" {
			break
		}
		item := NaverC1Item{}
		codeValue, _ := items.Eq(i).Attr("value")
		nameValue := items.Eq(i).Text()
		item.Code = codeValue
		item.Name = nameValue
		c1Items.AddItem(item)
	}

	c2Items := NaverC2{}
	for i := 0; i < len(c1Items.Items); i++ {
		c2URL := fmt.Sprintf("%s?cortarNo=%s", url, c1Items.Items[i].Code)
		fmt.Println(c2URL)
		subDoc := loadPageByURL(c2URL)
		queryItems := subDoc.Find(".area.scroll ul li")
		for j := 0; j < len(items.Nodes); j++ {
			//<a href="#" onclick="nhn.article.sector.goToDivision(&#39;1168000000&#39;);" class="NPI=a:area,r:1,i:1168000000">강남구</a> <nil>
			item := NaverC2Item{}
			nameValue := queryItems.Eq(j).Text()
			classValue, check := queryItems.Eq(j).Find("a").Attr("class")
			if check {
				//NPI=a:area,r:1,i:1168000000 true
				classValueSplit := strings.Split(classValue, ",")
				codeValue := strings.Split(classValueSplit[2], ":")[1]
				item.ParentCode = c1Items.Items[i].Code
				item.Code = codeValue
				item.Name = nameValue
				c2Items.AddItem(item)
			}
		}
	}

	//c3Items := NaverC3{}
	for i := 0; i < 1; i++ {
		c3URL := fmt.Sprintf("%s?cortarNo=%s", url, c2Items.Items[i].Code)
		fmt.Println(c3URL)
	}
}
