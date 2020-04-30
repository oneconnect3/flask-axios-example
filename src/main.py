import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
import traceback

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

CORS(app, resources={r'/*': {'origins': '*'}})

base_url = '/Users/Tianyu/Documents/OneConnect/Hackathon/flask-axios-example/data/'


# 数据处理
def get_data_by_keyword(keyword):
  df = pd.read_csv(base_url + 'animal-crossing-fish-info.csv')
  df['price'] = df['price'].astype(str)
  price = df[df['name'] == keyword]['price'].iloc[0]
  image = df[df['name'] == keyword]['image'].iloc[0].split('\t')[0] + '>'
  fish_info = {'price': str(price), 'image': image}
  
  return {'fish_info': fish_info}


@app.route('/data_generate', methods=['POST'])
def data_generate():
  global data
  
  if request.method == 'POST':
    
    try:
      post_data = request.get_json()
      keyword = post_data.get('search')
      data = get_data_by_keyword(keyword)
      message = {'status': 'success'}
    
    except Exception as e:
      traceback.print_exc()
      return jsonify({'status': 'fail'})
    
    else:
      return jsonify(message)


@app.route('/get_data', methods=['GET'])
def get_data():
  global data
  if request.method == 'GET':
    try:
      arg = request.args.get('name')
      response_data = data.get(arg)
      
      return jsonify(response_data)
    
    except Exception as e:
      traceback.print_exc()
      
      return None


if __name__ == '__main__':
  app.run(port=8000)
