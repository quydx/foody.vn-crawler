from app import fapp
from flask import render_template
from app import form
from app.form import EventSearch
from app.ticket_scaper import get_info
import re
#@@@@@
@fapp.route('/')
@fapp.route('/index')
def index():
	return render_template('index.html')
#@
@fapp.route('/search', methods=['GET', 'POST'])
def search():
	posts = []
	form = EventSearch()
	
	detail_link = "//div[@class='resname']/h2/a//@href"
	info = {}
	info['name'] = "//h1[@itemprop='name']//text()"
	info['street'] = "//span[@itemprop='streetAddress']//text()"
	info['district'] = "//span[@itemprop='addressLocality']//text()"
	if form.validate_on_submit():
		event = convert(form.event_name.data)
		location = convert(form.curr_location.data)
		city =	form.city.data
		url = 'https://www.foody.vn/'+ city +'/dia-diem?q=' + event +  '&ss=header_search_form'
		posts = list(get_info(location, url , detail_link, info))[0]
		posts = [ post for post in posts if post['distance'] is not None]
		posts = sorted(posts, key=lambda post: int(post['distance']))
	return render_template('search.html', title='Search for an Event', form=form, posts = posts)


patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}

def convert(text):
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        output = re.sub(regex.upper(), replace.upper(), output)
    return output
