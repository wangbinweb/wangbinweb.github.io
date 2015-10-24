package main
import (
    "os"
    "fmt"
    "strings"
    "regexp"
    "strconv"
)

var filename string=""
var title string=""
var time string=""
var zw string=""
var head string=""
var foot string=""

func main() {
    readtext()
    mdtohtml()
    headandfooter()
}

func readtext() {
    textFile := "post.md"
    fin,err := os.Open(textFile)
    defer fin.Close()
    if err != nil {
        fmt.Println(textFile,err)
        return
    }
    buf := make([]byte,1024)
    alltext := ""
    for {
        n, _ := fin.Read(buf)
        if 0 == n { break }
        alltext = alltext + string(buf[:n])
    }
    sp := strings.Split(alltext,"\n==========\n")
    filename = sp[0]
    zw = sp[1]
    sp2 := strings.Split(zw,"\n")
    time = strings.Replace(sp2[0],"#### ","",1)
    sp3 := strings.Split(zw,"\n")
    title = strings.Replace(sp3[1],"## ","",1)
    fmt.Printf("文件名是： %s\n",filename)
    fmt.Printf("时间是： %s\n",time)
    fmt.Printf("标题是： %s\n",title)
}

func headandfooter() {
    head = "<!DOCTYPE html>\n"
    head = head + "<html>\n"
    head = head + "<head>\n"
    head = head + "<meta charset='utf-8'>\n"
    head = head + "<meta http-equiv=\"X-UA-Compatible\" content=\"chrome=1\">\n"
    head = head + "<meta name=\"description\" content=\"Wangbinweb.GitHub.io : 王斌的博客网站\">\n"
    head = head + "<link rel=\"stylesheet\" type=\"text/css\" media=\"screen\" href=\"../stylesheets/css.css\">\n"
    head = head + "<title>" + title + "</title>\n" + "</head>\n" + "<body>\n" + "<div id=\"container\">\n"
    foot = "</div>\n" + "<nav>\n" + "<div id=\"archive\"><a href=\"../index.html\">文章索引</a></div>\n" + "</nav>\n" + "</body>\n" + "</html>"
}

func mdtohtml() {
    /*段落格式化*/
    reg1 := regexp.MustCompile(`(\r?\n){2,}`)
    rep1 := "</p><p>"
    zw = reg1.ReplaceAllString(zw,rep1)
    zw = strings.Replace(zw,"</p>","",1) + "</p>"
    /* 标题格式化 title */
    first, _ := regexp.MatchString(`^[\s]*#+[ ]+[^\r\n]+`,zw)
    if first {
        reg2 := regexp.MustCompile(`^[\s]*#+[ ]+`)
        s1 := reg2.FindString(zw)
        s2 := strings.Replace(s1," ","",-1)
        n1 := len(s2)
        reg3 := regexp.MustCompile(`^[\s]*#+[ ]+([^\r\n]+?)([\r]?\n|</p>|<p>)`)
        rep3 := "<h" + strconv.Itoa(n1) + ">" + "$1" + "</h" + strconv.Itoa(n1) + ">" + "$2"
        zw = reg3.ReplaceAllString(zw,rep3)
    }
    reg4 := regexp.MustCompile(`([\r]?\n|<p>)[ ]*#[ ]+([^\r\n]+?)([\r]?\n|</p>|<p>)`)
    rep4 := "$1<h1>$2</h1>$3"
    zw = reg4.ReplaceAllString(zw,rep4)
    reg5 := regexp.MustCompile(`([\r]?\n|<p>)[ ]*##[ ]+([^\r\n]+?)([\r]?\n|</p>|<p>)`)
    rep5 := "$1<h2>$2</h2>$3"
    zw = reg5.ReplaceAllString(zw,rep5)
    reg6 := regexp.MustCompile(`([\r]?\n|<p>)[ ]*###[ ]+([^\r\n]+?)([\r]?\n|</p>|<p>)`)
    rep6 := "$1<h3>$2</h3>$3"
    zw = reg6.ReplaceAllString(zw,rep6)
    reg7 := regexp.MustCompile(`([\r]?\n|<p>)[ ]*####[ ]+([^\r\n]+?)([\r]?\n|</p>|<p>)`)
    rep7 := "$1<h4>$2</h4>$3"
    zw = reg7.ReplaceAllString(zw,rep7)
    reg8 := regexp.MustCompile(`([\r]?\n|<p>)[ ]*#####[ ]+([^\r\n]+?)([\r]?\n|</p>|<p>)`)
    rep8 := "$1<h5>$2</h5>$3"
    zw = reg8.ReplaceAllString(zw,rep8)
    reg9 := regexp.MustCompile(`([\r]?\n|<p>)[ ]*######[ ]+([^\r\n]+?)([\r]?\n|</p>|<p>)`)
    rep9 := "$1<h6>$2</h6>$3"
    zw = reg9.ReplaceAllString(zw,rep9)
    /* 项目符号格式化 */
    reg10 := regexp.MustCompile(`(<p>|\r?\n)[-+*][ ]+`)
    rep10 := "</li><li>$1"
    zw = reg10.ReplaceAllString(zw,rep10)
    reg11 := regexp.MustCompile(`(<li>[\s\S]+?</p>)(<p>[ ]{0,3}[^\s]+[\s\S])`)
    rep11 := "$1</li></ul>$2"
    zw = reg11.ReplaceAllString(zw,rep11)
    reg12 := regexp.MustCompile(`</li>([\s\S]+?</ul>)`)
    rep12 := "<ul>$1"
    zw = reg12.ReplaceAllString(zw,rep12)
    reg13 := regexp.MustCompile(`(<li>[\s]*[^<]+[\s\S]+?)(</p>)?</li>`)
    rep13 := "$1</li>"
    zw = reg13.ReplaceAllString(zw,rep13)
    reg14 := regexp.MustCompile(`<li>(<p>)?([\s\S]+?[^</>]</li>)`)
    rep14 := "<li>$2"
    zw = reg14.ReplaceAllString(zw,rep14)
    /* 编号格式化 */
    fmt.Printf("正文内容是：%s\n",zw)
}
