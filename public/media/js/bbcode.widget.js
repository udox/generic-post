var $ = django.jQuery;
$(document).ready(function() {

});

function insert_youtube(video_id, element) {
    if (!video_id) {
        video_id = prompt('What is the ID of the video (the v= bit of the URL)?\n\n(Fear not, we\'ll clean it for you, you can copy the\nURL bit straight from youtube)');
        var re = new RegExp(/v=([a-zA-Z0-9_-]+)/);
        var m = re.exec(video_id);
        if (m) {
            video_id = m[1];
            return do_insert('[youtube]'+video_id+'[/youtube]', element);
        } else {
            return false;
        }
    } else {
        return false;
    }
    return false;
}

function insert_vimeo(video_id, element) {
    if (!video_id) {
        video_id = prompt('What is the ID of the video (the numbers after the URL)?\n\n(Fear not, we\'ll clean it for you, you can copy the\nURL bit straight from vimeo)');
        var re = new RegExp(/([0-9]+)/);
        var m = re.exec(video_id);
        if(m) {
            video_id = m[1];
            return do_insert('[vimeo]'+video_id+'[/vimeo]', element);
        }
    } else {
        return false;
    }
    return false;
}

function insert_link(url, name, title, element) {
	var ta = $(element).parent().next('textarea').get(0);
	var val = ta.value;
    if (!url) {
		url = prompt(('What is the URL of the link?'), 'http://');
        if (val.substring(ta.selectionStart, ta.selectionEnd)) {
			ta.value = val.substring(0, ta.selectionStart) + '[url=' + url + ']' + val.substring(ta.selectionStart, ta.selectionEnd) + '[/url]' + val.substring(ta.selectionEnd, val.length);
			return false;
		}
		if (!url) {
            return false;
        }
    }
    if (!name) {
        name = prompt(('What is the title of the link?'));
        if (!name) {
            name = url;
        }
    }
    if (!title) {
        title = name;
    }
    return do_insert('[url=' + url + ']' + name + '[/url]', element);
}

function surround(tag, ctag, element) {
	var ta = $(element).parent().next('textarea').get(0);
    if (!ctag) {
        ctag = tag;
    }
    if (document.selection) {
        ta.focus();
        var selection = document.selection.createRange();
        selection.text = tag + selection.text + ctag;
    } else if (ta.selectionStart >= 0) {
        var val = ta.value;
        ta.value = val.substring(0, ta.selectionStart) + tag + val.substring(ta.selectionStart, ta.selectionEnd) + ctag + val.substring(ta.selectionEnd, val.length);
    } else {
        ta.value += tag + ctag
    }
    return false;
}

function do_insert(tag, element) {
    var ta = $(element).parent().next('textarea').get(0);
    if (document.selection) {
        ta.focus();
        var selection = document.selection.createRange();
        text = selection.text;
        selection.text = tag;
    } else if (ta.selectionStart >= 0) {
        var val = ta.value;
        ta.value = val.substring(0, ta.selectionStart) + tag + val.substring(ta.selectionEnd, val.length);
    } else {
        ta.value += '\n' + tag;
    }
    return false;
}

function get_ta() {
	
    return document.getElementById('id_body');
}

function insert_img(number, element) {
    if (!number) {
        number = prompt(('What number image from below?'), '');
        if (!number) {
            return false;
        }
    }
    return do_insert('[[image-' + number + ']]', element);
}

function insert_map(number, element) {
    // These id's come via admin form for Locatable abstract base class
    var ad1 = $('#id_address_1').val();
    var ad2 = $('#id_address_2').val();
    var city = $('#id_city').val();
    var zipcode = $('#id_zipcode').val();

    var address = ad1;
    if (ad2)
        address += ', '+ad2;
    if (city)
        address += ', '+city;
    if (zipcode)
        address += ', '+zipcode;

    return do_insert('[map]'+address+'[/map]', element);
}

function insert_readmore(element) {
    return do_insert('[[readmore]]', element);
}

function insert_urlimg(url, name, title, element) {
    if (!url) {
        url = prompt(('What is the URL of the image?'), 'http://');
        if (!url) {
            return false;
        }
    }
    if (!name) {
        name = prompt(('What is the title of the image?'));
        if (!name) {
            name = '';
        }
    }
    if (!title) {
        title = name;
    }
    return do_insert('[img' + (name ? '=' + name : '') + ']' + url + '[/img]', element);
}
