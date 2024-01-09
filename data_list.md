# Data list

## Japan

<ul>
    <li>
        <a href=https://www.e-gov.go.jp>e-GOV</a>
        <div>
            <input type="checkbox" checked />
            <label>Law</label>
        </div>
        <details>
            <summary>check</summary>
            <h3>About e-GOV</h3>
            <blockquote>
            This is the official web portal of Government of Japan, e-Gov is managed by the Digital Agency. In Japan, the Government is working on promotion of initiatives such as online use of administrative procedures, electronic provision of government information, optimization of work and systems, improvement of government procurement related to information systems, and information security measures. This website provides a collection of links according to the purpose of the visitor, and also provides useful information provided in Japan.
            </blockquote>
            <h3>How to obtain data</h3>
            e-GOV data can be obtained via API, and this library also uses the API.
        </details>
    </li>
    <li>
        <a href=https://www.jpx.co.jp>JPX</a>
        <div>
            <input type="checkbox" checked />
            <label>Association rules</label>
        </div>
        <div>
            <input type="checkbox" checked />
            <label for="scales">Public comments</label>
        </div>
        <details>
            <summary>check</summary>
            <h3>About JPX</h3>
            <blockquote>
            Japan Exchange Group, Inc. (JPX) was established via the business combination between Tokyo Stock Exchange Group and Osaka Securities Exchange on January 1, 2013.
            On October 1, 2019, JPX expanded its business into commodity derivatives trading by acquiring Tokyo Commodity Exchange, Inc.
            JPX operates financial instruments exchange markets to provide market users with reliable venues for trading listed securities and derivatives instruments. In addition to providing market infrastructure and market data, JPX also provides clearing and settlement services through a central counterparty and conducts trading oversight to maintain the integrity of the markets. In the course of working together as an exchange group to offer a comprehensive range of services, we continue to make every effort to ensure reliable markets and create greater convenience for all market users.
            </blockquote>
            <h3>How to obtain data</h3>
            JPX data was obtained in two parts: association rules and public comments.
            <h4><a href="https://jpx-gr.info">Association rules</a></h4>
            You can get all the URLs for each link from the <a href="https://jpx-gr.info">JPX's Association Rules website</a>.
            <h4><a href=https://www.jpx.co.jp/rules-participants/public-comment/index.html>Public comments</a></h4>
            First, by specifying the fiscal year, a list of links to public comments received by the JPX can be retrieved (<a href=https://www.jpx.co.jp/rules-participants/public-comment/detail/d1/20231218-01.html>example page</a>). After that, a link to a pdf (attached) summarizing the responses to each public comment can be obtained.
        </details>
    </li>
    <li>
        <a href=https://www.fsa.go.jp/en>FSA</a>
        <div>
            <input type="checkbox" checked />
            <label for="scales">Public comments</label>
        </div>
        <div>
            <input type="checkbox" checked />
            <label>News</label>
        </div>
        <details>
            <summary>check</summary>
            <h3>About FSA</h3>
            The Financial Services Agency is a Japanese government agency and an integrated financial regulator responsible for overseeing banking, securities and exchange, and insurance sectors in order to ensure the stability of the financial system of Japan.
            <h3>How to obtain data</h3>
            Public comments received by the FSA were obtained.
            <h4><a href=https://www.fsa.go.jp/public>Public comments</a></h4>
            First, the list of public comments was retrieved by specifying the year, and the responses (pdf) linked to each public comment were made available for download.
            <h4><a href=https://www.fsa.go.jp/news/index.html>News</a></h4>
            Specify a fiscal year and retrieve links to all news stories within that year.
        </details>
    </li>
    <li>
        <a href=https://www.jsda.or.jp/en>JSDA</a>
        <div>
            <input type="checkbox" checked />
            <label for="scales">Association rules</label>
        </div>
        <details>
            <summary>check</summary>
            <h3>About JSDA</h3>
            The Japan Securities Dealers Association (JSDA) is an association functioning as a self-regulatory organization (SRO) and as an interlocutor for the securities industry.
            <h3>How to obtain data</h3>
            JSDA association rules can be obtained.
            <h4><a href=https://www.jsda.or.jp/about/kisoku">Association rules</a></h4>
            Get all the pdf links in <a href=https://www.jsda.or.jp/about/kisoku>the association rules link</a>.
        </details>
    </li>
    <li>
        <a href=https://www.fsa.go.jp/sesc>SESC</a>
        <div>
            <input type="checkbox" checked />
            <label for="scales">News（報道資料）</label>
        </div>
        <div>
            <input type="checkbox" />
            <label>処分事例</label>
        </div>
        <details>
            <summary>check</summary>
            <h3>About SESC</h3>
            From <a href=https://en.wikipedia.org/wiki/Securities_and_Exchange_Surveillance_Commission>Wikipedia</a>
            <blockquote>
            The Securities and Exchange Surveillance Commission (証券取引等監視委員会, shouken torihikitou kanshi iinkai, SESC) is a Japanese commission which comes under the authority of the Financial Services Agency. It is responsible for “ensuring fair transactions in both securities and financial futures markets.”
            </blockquote>
            <h3>How to obtain data</h3>
            TBE.
            <h4><a href=https://www.fsa.go.jp/sesc/houdou/index.html>報道資料</a></h4>
            TBE.
            <h4><a href=https://www.fsa.go.jp/sesc/jirei/index.html>処分事例</a></h4>
            <code>- 種類は4つ
- 課徴金事例集
    https://www.fsa.go.jp/sesc/jirei/index.html
- 課徴金事例集 (不公正取引編)
    https://www.fsa.go.jp/sesc/jirei/torichou/20170829.html
- 課徴金事例集 (開示規制違反編)
    https://www.fsa.go.jp/sesc/jirei/kaiji/20160826.html
- 開示検査事例集
    https://www.fsa.go.jp/sesc/jirei/kaiji/20210730-1.html
なので、無印、kaji, torichouの3つでフィルターかけて、pdfで絞れば全部とれる</code>
        </details>
    </li>
    <li>
    other
    <code>### 大和総研 (レポート)
https://www.dir.co.jp/report/research/law-research/index.html
### 長嶋大野
https://www.noandt.com/newsletters/
### NRI
https://www.nri.com/jp/knowledge/publication
    </code>
    </li>
</ul>
