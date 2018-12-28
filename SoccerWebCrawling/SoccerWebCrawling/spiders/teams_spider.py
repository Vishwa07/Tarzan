import scrapy


class MatchInfo:
  def __init__(self, league, teamA,teamB,url):
    self.league = league
    self.teama = teamA
    self.teamb = teamB
    self.url = url



class TeamsSpider(scrapy.Spider):
    name = "Socccerteams"
    leagues = ['England - Premier League','World - Friendlies']
    url = 'https://int.soccerway.com'
    def  start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self,response):
        items = response.xpath('//table[@class="matches date_matches grouped "]/tbody/tr')
        index = 0
        infolist = []
        while(index<len(items)):            
            if items[index].xpath('@class').extract()[0] == "group-head expanded loaded  ":
                leaguename = items[index].xpath("./th/h3/span/text()").extract()[0]
                if leaguename in self.leagues:
                    while(1):                                               
                        index = index + 1
                        if(index > len(items)-1):
                            break                        
                        type =  items[index].xpath('@class').extract()[0]
                        if(type == "group-head expanded loaded  " ):
                            index = index -1
                            break                        
                        elif(type == "even  expanded first last  match no-date-repetition"):
                            teama = (items[index].xpath('./td[@class="team team-a "]/a/text()').extract())[0].strip()
                            teamb = (items[index].xpath('./td[@class="team team-b "]/a/text()')).extract()[0].strip()
                            infoURL = items[index].xpath('./td[@class="info-button button"]/a/@href').extract()[0]
                            infoURL = self.url + infoURL
                            matchinfo = MatchInfo(leaguename,teama,teamb,infoURL)
                            infolist.append(matchinfo)

            else:
                index = index + 1
        
        f = open('workfile', 'w')
        f.write(infolist[0].league)
        for item in infolist:
            f.write(item.league)
            f.write('/n')
            f.write(item.teama)
            f.write('/n')
            f.write(item.teamb)
            f.write('/n')
            f.write(item.url)
            f.write('/n------------------------/n')
        f.close()