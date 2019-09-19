nordea_url = "https://www.nordea.dk/erhverv/valutamarginaler.html"
nordea_xpaths = [" ",
                 "/html/body/main/section[1]/div/article/table/tbody/tr/td[1]/text()",
                 "/html/body/main/section[1]/div/article/table/tbody/tr/td[4]/text()",
                 "/html/body/main/section[1]/div/article/table/tbody/tr/td[5]/text()"
                 ]

fynske_url = "https://www.fynskebank.dk/om-os/priser-og-vilkar/valutamarginaler/"
fynske_xpaths = [" ",
                 "/html/body/div[1]/div[1]/div/div/div/section/div/div[1]/table[1]/tbody/tr/td[1]/text()",
                 "/html/body/div[1]/div[1]/div/div/div/section/div/div[1]/table[1]/tbody/tr/td[3]/text()",
                 "/html/body/div[1]/div[1]/div/div/div/section/div/div[1]/table[1]/tbody/tr/td[4]/text()"
                 ]

jyske_url = "https://www.jyskebank.dk/produkter/priser/valutamarginaler"
jyske_xpaths = [" ",
                "/html/body/div[1]/div[4]/div/div[2]/div[1]/div[2]/table/tbody/tr/td[1]/text()",
                "/html/body/div[1]/div[4]/div/div[2]/div[1]/div[2]/table/tbody/tr/td[2]/div/div/text()",
                "/html/body/div[1]/div[4]/div/div[2]/div[1]/div[2]/table/tbody/tr/td[2]/div/div/text()"
                ]

nykredit_url = "https://www.nykredit.dk/dit-liv/priser-og-vilkar/valutakurser/valutakurser---noteringskurser/"
nykredit_xpaths = [" ",
                   '//*[@id="main-container"]/article/div[3]/div[2]/div/div/div[2]/div/table/tbody/tr/td[3]/text()',
                   '//*[@id="main-container"]/article/div[3]/div[2]/div/div/div[2]/div/table/tbody/tr/td[8]/text()',
                   '//*[@id="main-container"]/article/div[3]/div[2]/div/div/div[2]/div/table/tbody/tr/td[8]/text()'
                   ]
