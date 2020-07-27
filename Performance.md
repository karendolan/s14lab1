# Performance of Community Posts Project

##The Project
**HW4-lab5 s14a-2020 Karen Dolan**

The comment posting project displays community comments and the option for new users to register to post. 
Keywords: post, comment, community


##Testing sites
* [PageSpeed Insights](https://developers.google.com/speed/pagespeed/insights/)  Initial score: 94/100. After improvements: 95/100.
* [Seobility](https://www.seobility.net/en/) Initial score: 48%. After improvements: 57%.
* [Seo-analyzer](https://neilpatel.com/seo-analyzer/) Initial score 81 "Great".
* [Seo test online](https://www.seotesteronline.com/) Initial score: 39.2/100. After improvements: 66.5/100.
* [Site checker](https://sitechecker.pro/) Score: 60/100
* [Site checkup](https://seositecheckup.com/) Score: 65/100
* [Woo rank](https://www.woorank.com/) Inital score: 34/100. After improvements: 42/100

##Analysis and Recommendations

* Performace was good.
* Opportunities/Criticism
	*	Eliminate render-blocking resources (add "asynch" to non-essential imports)
	* Remove unused CSS
	* Missing meta data description
	* No internal links, index page is a dead end
	* Use GZip
	* Need redirects of URLs (http to https, www to non-wwww, etc)
	* Missing robots.txt
	* Should have a different title on each page
	* The title is too short, should be 40-70 char
	* Missing meta keywords
	* H1 text should be more descriptive
	
	
## Improvments made to Project
* Added meta keyworks, description
* Added a longer and different meta title for each page in the project
* Added more descriptive H1 text on each page
* Changed some form-button links to anchor links on index page
* Added robots.txt (to static dir and locatable on root)
* Removed the word "Welcome" from all title and h1 text
* Added "asynch" to all javascript and CSS imports
* Removed redundant CSS lines
	
	  