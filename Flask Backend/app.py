from flask import Flask
from flask_restful import Resource, Api, reqparse
from espn_parser import get_sports_data

app = Flask(__name__)
api = Api(app)


class TeamData(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('league', type=str)
        parser.add_argument('team', type=str)
        args = parser.parse_args()

        try:
            league = args.get('league')
            team = args.get('team').replace('+', ' ')
        except:
            pass


        try: 
            sports_data = get_sports_data(league, team)
            return sports_data
        except:
            return {'error': 'please provide a league and team'}

api.add_resource(TeamData, '/')

if __name__ == '__main__':
    app.run(debug=False)
# Make it publicly available (not just this computer) by running 'flask run --host=0.0.0.0' MAKE SURE debug=False BEFORE THIS