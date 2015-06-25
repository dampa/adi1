#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-


from flask import Flask, jsonify, abort, make_response, request
from datetime import datetime

app = Flask (__name__)

news = [
	{
        'ID_New' : 1,
        'ID_Publisher' : '1',
        'Title' : '1',
        'Text' : '1',
        'Date' : '1',
        'Last_Update' : '1',
        'Like' : [],
        'Dislike' : [],
        'Photo' : '1'
	},
	{
        'ID_New' : 2,
        'ID_Publisher' : '2',
        'Title' : '2',
        'Text' : '2',
        'Date' : '2',
        'Last_Update' : '2',
        'Like' : [],
        'Dislike' : [],
        'Photo' : '2'
	}
]


id_publisher = 1

# OPERACIONES SOBRE EL CONJUNTO DE RECURSOS

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify ({'error' : 'Not found'}), 404)


def post_news(request):
    if not request.json or not 'Title' in request.json:
        abort(400)
    if len(news) == 0:    
		id_new = 1
	else:
		id_new = news[-1]['ID_New']+1
    new = {
        'ID_New' : id_new,
        'ID_Publisher' : id_publisher,
        'Title' : request.json.get('Title', ""),
        'Text' : request.json.get('Text', ""),
        'Date' : datetime.now(),
        'Last_Update' : datetime.now(),
        'Like' : [],
        'Dislike' : [],
        'Photo' : request.json.get('Photo', "")}
    news.append(new)
    return jsonify({'new':new}), 201
    

def get_news():
    return jsonify({'news': news}), 200


def del_news():
	for i in news[:]:
		news.remove(i)
	return jsonify({'news deleted': True}), 200
	

@app.route('/news', methods = ['GET', 'POST', 'DELETE'])
def news_management():
    if request.method == 'GET':
        return get_news()
    elif request.method == 'DELETE':
      return del_news()
    elif request.method == 'POST':
      return post_news(request)
    else:
      abort(404)



# OPERACIONES SOBRE EL RECURSO

def getNew(new_id):
    new = filter(lambda t:t['ID_New'] == new_id, news)
    if len(new) == 0:
        abort(404)
    return jsonify({'new': new}), 200


def updateNew(new_id):
    new = filter(lambda t:t['ID_New'] == new_id, news)
    if len(new) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'Title' in request.json and type(request.json['Title']) != unicode:
        abort(400)
    if 'Text' in request.json and type(request.json['Text']) != unicode:
        abort(400)
    if 'Like' in request.json and type(request.json['Like']) != list:
        abort(400)
    if 'Dislike' in request.json and type(request.json['Dislike']) != list:
        abort(400)
    if 'Photo' in request.json and type(request.json['Photo']) != unicode:
        abort(400)
    news[new_id-1]['Title'] = request.json.get('Title', news[new_id-1]['Title'])
    news[new_id-1]['Text'] = request.json.get('Text', news[new_id-1]['Text'])
    news[new_id-1]['Last_Update'] = datetime.now()
    news[new_id-1]['Like'] = request.json.get('Like', news[new_id-1]['Like'])
    news[new_id-1]['Dislike'] = request.json.get('Dislike', news[new_id-1]['Dislike'])
    news[new_id-1]['Photo'] = request.json.get('Photo', news[new_id-1]['Photo'])
    return jsonify({'update new': news[new_id-1]}), 200


def delNew(new_id):    
    new = filter(lambda t:t['ID_New'] == new_id, news)
    if len(new) == 0:
        abort(404)
    news.remove(new[0])
    return jsonify({'deleted': new[0]}), 200



@app.route('/news/<int:new_id>', methods=['GET', 'PUT', 'DELETE'])
def manager_post(new_id):
    if request.method == 'GET':
        return getNew(new_id)
    elif request.method == 'PUT':
        return updateNew(new_id)
    elif request.method == 'DELETE':
        return delNew(new_id)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug = True )



