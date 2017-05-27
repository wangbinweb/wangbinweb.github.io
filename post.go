package main
import (
    "os"
    "fmt"
    "strings"
    "regexp"
    "io/ioutil"
)

var FileName string=""
var Title string=""
var Time string=""
var Content string=""
var head string=""
var foot string=""
var wri string=""
var indexfile string=""
var mdfilename string=""

func main() {
    readtext()
    headandfooter()
    writefile()
    writeindex()
    writeindexfile()
    cpmd()
}

func cpmd() {
    alltext := ""
    buf, err := ioutil.ReadFile("post.md")
    if err != nil {
        fmt.Fprintf(os.Stderr, "File Error: %s\n", err)
        // panic(err.Error())
        }
    alltext = string(buf)
    wFile := "./md/" + mdfilename
    fout,err := os.Create(wFile)
    defer fout.Close()
    if err != nil {
        fmt.Println(wFile,err)
        return
    }
    fout.WriteString(alltext)
}

func writeindex() {
    alltext := ""
    buf, err := ioutil.ReadFile("index.html")
    if err != nil {
        fmt.Fprintf(os.Stderr, "File Error: %s\n", err)
        // panic(err.Error())
        }
    alltext = string(buf)

    indexln := ""
    indexln = "<p>最近文章：</p>\n"
    indexln = indexln + "<p><a href=\"/htm/" + FileName + ".htm" + "\">" + Time + "-" + Title + "</a></p>"
    alltext = strings.Replace(alltext,"<p>最近文章：</p>",indexln,1)
    fin2, err := os.OpenFile("index.html",os.O_RDWR | os.O_TRUNC,0644)
    defer fin2.Close()
    fin2.WriteString(alltext)
    fin2.Close()
}

func writeindexfile() {
    alltext := ""
    buf, err := ioutil.ReadFile(indexfile)
    if err != nil {
        fmt.Fprintf(os.Stderr, "File Error: %s\n", err)
        // panic(err.Error())
        }
    alltext = string(buf)

    indexln := ""
    indexln = "归档文章：</p>\n"
    indexln = indexln + "<p><a href=\"/htm/" + FileName + ".htm"+ "\">" + Time + "-" + Title + "</a></p>"
    alltext = strings.Replace(alltext,"归档文章：</p>",indexln,1)
    fin2, err := os.OpenFile(indexfile,os.O_RDWR | os.O_TRUNC,0644)
    defer fin2.Close()
    fin2.WriteString(alltext)
    fin2.Close()
}


func readtext() {
    buf, err := ioutil.ReadFile("post.md")
    if err != nil {
        fmt.Fprintf(os.Stderr, "File Error: %s\n", err)
        // panic(err.Error())
    }
    alltext := ""
    alltext = string(buf)
    reg1 := regexp.MustCompile(`\[Title\]\n(.+)\n\[/Title\]`)
    s1 := reg1.FindString(alltext)
    s2 := "$1"
    Title = reg1.ReplaceAllString(s1,s2)
    fmt.Printf("标题是： %s\n",Title)
    reg2 := regexp.MustCompile(`\[FileName\]\n(.+)\n\[/FileName\]`)
    s3 := reg2.FindString(alltext)
    s4 := "$1"
    FileName = reg2.ReplaceAllString(s3,s4)
    fmt.Printf("文件名是： %s\n",FileName)
    mdfilename = FileName + ".md"
    reg3 := regexp.MustCompile(`\[Time\]\n(.+)\n\[/Time\]`)
    s5 := reg3.FindString(alltext)
    s6 := "$1"
    Time = reg3.ReplaceAllString(s5,s6)
    fmt.Printf("文章发表时间是： %s\n",Time)
    indexfile = Time[0:4] + "index.htm"
    fmt.Printf("indexfile is %s\n",indexfile)
    reg4 := regexp.MustCompile(`\[Content\]\n([\s\S]+)\n\[/Content\]`)
    s7 := reg4.FindString(alltext)
    s8 := "$1"
    Content = reg4.ReplaceAllString(s7,s8)
    fmt.Printf("文章内容是： %s\n",Content)
}

func headandfooter() {
    head = "<!DOCTYPE html>\n"
    head = head + "<html>\n"
    head = head + "<head>\n"
    head = head + "<meta charset='utf-8'>\n"
    head = head + "<meta http-equiv=\"X-UA-Compatible\" content=\"chrome=1\">\n"
    head = head + "<meta name=\"description\" content=\"Wangbinweb.GitHub.io : 王斌的博客网站\">\n"
    head = head + "<link rel=\"stylesheet\" type=\"text/css\" media=\"screen\" href=\"../stylesheets/css.css\">\n"
    head = head + "<title>" + Title + "</title>\n" + "</head>\n" + "<body>\n" + "<div id=\"container\">\n"
    head = head + "<h4>" + Time + "</h4>\n" + "<h2>" + Title + "</h2>\n"
    foot = "</div>\n" + "<nav>\n" + "<div id=\"archive\"><a href=\"../index.html\">文章索引</a></div>\n" + "</nav>\n" + "</body>\n" + "</html>"
}


func writefile() {
    wFile := "./htm/" + FileName + ".htm"
    fout,err := os.Create(wFile)
    defer fout.Close()
    if err != nil {
        fmt.Println(wFile,err)
        return
    }
    wri = head + Content + foot
    fout.WriteString(wri)
}
