import json
import dicttoxml
from xml.dom.minidom import parseString

file_number = 1
class ReadInput:



    def ConvertInput(self, text):
        #Standardize the data. Remove tags 
        text = text.replace("Collision: ", "")
        _quiz = text.split("[Q]")
        text = text.replace(" ", "")
        text = text.replace("cTS:","")
        text = text.replace("cPOS", "Coll:")
        text = text.replace("aTS:", "")
        text = text.replace("aPOS:", "Atk:")
        text = text.replace("aTar:", "")
        text = text.replace("aHt:", "")
        text = text.replace("dTS:", "")
        text = text.replace("dPOS:", "Dmg:")
        text = text.replace("dATK:", "")
        text = text.replace("dDMG:", "")
        Col_to_Attack = text.split("Attakc:")
        _collisions = Col_to_Attack[0].split("|")

        _combined = []
        if 1<len(Col_to_Attack):
            Attack_to_Damage = Col_to_Attack[1].split("Damage:")
            _attacks = Attack_to_Damage[0].split("|")
            Damage_to_Heal = Attack_to_Damage[1].split("Heal:")
            _damage = Damage_to_Heal[0].split("|")
            Heal_to_Kill = Damage_to_Heal[1].split("Kill:")
            _heal = Heal_to_Kill[0].split("|")
            Kill_to_Quiz = Heal_to_Kill[0].split("1.")
            _kill = Kill_to_Quiz[0].split("|")
            _combined = _kill + _heal + _damage + _attacks + _collisions
            _combined = [i for i in _combined if i]

        #Define a function that returns 
        def myFunc(e):
            return e["time"]

        #MAster dictionary has players,
        #Players have Data and Survey

        action = {}
        for i in range(len(_combined)):
            split = _combined[i].split(":")
            diction= {}
            convertedTime = split[0].replace(",", ".")
            diction["time"] = float(convertedTime.strip("\'"))
            diction["type"] = split[1]
            #Split the Position into x and y
            strippedCoordinates = split[2].strip("()")
            strippedCoordinates = strippedCoordinates.split(",")
            strippedCoordinates[0] = float(strippedCoordinates[0])
            strippedCoordinates[1] = float(strippedCoordinates[1])
            diction["pos"] = strippedCoordinates

            if 3<len(split):
                diction["obj"] = split[3]
                if 4<len(split):
                    diction["state"] = split[4]
            _combined[i] = diction
            
        _combined.sort(key=myFunc)
        
        for i in range(len(_combined)):
            action[f"{i}"] = _combined[i]

        #Create Item for every item in _combined if Item is true
        if len(_quiz)> 1:
            _quiz.pop(0)
            for i in range(len(_quiz)):
                _quiz[i] = _quiz[i][len(_quiz[i])-5:len(_quiz[i])-1:]
                _quiz[i] = _quiz[i].strip("; ")
            print("Quizz: ")
            print(*_quiz, sep="\n")

        print("Chronological ")
        for key, item in action.items():
            print(key, " : ", action[key])

        player_tuple = (action, _quiz)
        return player_tuple


    def ReadJsonData(self):
        readData = {}
        with open("C:/Users/codeg/Documents/data1.json") as r:
            readData = json.load(r)
        print(f"there are {len(readData)} datapoints in this collection")
        return readData

    def AddToDict(self, json_dict, player_tuple):
        index = len(json_dict)
        json_dict[f"{index}"] = {"action" : player_tuple[0], "quiz" : player_tuple[1]}
        return json_dict

    def WriteJsonData(self,filename, write_data):
        with open ("C:/Users/codeg/Documents/" + filename + ".json", "w") as w:
            json.dump(write_data, w)
            print("\n ---Write to JSON Completed---- \n")

    def RemoveNullSurveys(self, jsonData):
        for key, value in jsonData.items():
            data = value["quiz"]
            if len(data) < 2:
                value["quiz"] = "No Survey Data"
                print("Removed Null Survey Data")
        return jsonData
    
    def SummarizeData(self, dictionary):
        #Create a dictionary to hold all data
        all_players = {}
        for item in dictionary.items():
            #Create a player dictionary
            player = {"time": "", "datapoints": "","collisions": "", "attacks": "", "damaged": "","xAxis": "", "yAxis": "",  "survey": ""}
            coll_count = 0
            atk_count = 0
            dmg_count = 0
            player_data = item[1]
            actions = player_data["action"]
            survey = player_data["quiz"]
            if survey == "No Survey Data":
                survey = ["No Data", "No Data", "No Data", "No Data", "No Data", "No Data", "No Data"]
            if len(survey) == 8:
                del survey[7]
            player["survey"] = survey
            numberOfDataPoints = len(actions) #Number of Datapoints
            player["datapoints"] = numberOfDataPoints
            xCoord = -500
            yCoord = -500
            for key, value in actions.items():
                data_type = value["type"]
                if data_type == "Coll":
                    coll_count += 1
                if data_type == "Atk":
                    atk_count += 1
                if data_type == "Dmg":
                    dmg_count += 1
                coordinates = value["pos"]
                if coordinates[0] > xCoord:
                    print("X coordinate " + str(yCoord) + " being replaced by " + str(coordinates[0]))
                    xCoord = coordinates[0]
                if coordinates[1] > yCoord:
                    print("Y coordinate " + str(yCoord) + " being replaced by " + str(coordinates[1]))
                    yCoord = coordinates[1]
                
            player["collisions"] = coll_count
            player["attacks"] = atk_count
            player["damaged"] = dmg_count
            player["yAxis"] = yCoord
            player["xAxis"] = xCoord
            if str(numberOfDataPoints -1) in actions:
                
                lastAction = actions[str(numberOfDataPoints -1)]
                if "time" in lastAction:
                    time = lastAction["time"]
                    timeInMinutes = time/60
                    player["time"] = timeInMinutes
            #print(player)
            all_players[len(all_players)] = player
        #print(all_players)
        return all_players
        
    def SummaryToXML(self, filename, dictionary):
        #for key, value in dictionary.items():
           # joinedString = ", "
            #value["survey"] = joinedString.join(value["survey"])
            #print(value["survey"])
        xml = dicttoxml.dicttoxml(dictionary, attr_type=False)
        #print(parseString(xml).toprettyxml())
        with open ("C:/Users/codeg/Documents/" + filename + ".xml", "wb") as file:
            file.write(xml)

        #json_string = json.dumps(dictionary)
        #json_dict = json.loads(json_string)
        #root = ET.element("Players")
        #for key, value in json_dict.items:
         #   print(item)
        #player_element = ET.SubElement(root, "Player")
        #text = json_dict["time"][]
        
        
            
        
            #print(lastAction["time"])
                
    def CountSurveyAnswers(self, dictionary):
        for key, value in dictionary.items():
            questionsCount = [0,0,0,0,0,0,0]
            data = value["quiz"]
            if len(data) > 1:
                if data[0] == "Yes":
                    questionsCount[0] += 1
                if data[1] == "Yes":
                    questionsCount[1] += 1
                if data[2] == "Yes":
                      questionsCount[2] += 1
                if data[3] == "Yes":
                      questionsCount[3] += 1
                if data[4] == "Yes":
                      questionsCount[4] += 1
                if data[5] == "Yes":
                      questionsCount[5] += 1
                if data[6] == "Yes":
                     questionsCount[6] += 1
            return questionsCount

        """print("Collision:")
        print(*_collisions, sep = "\n")
        print("Attack: ")
        print(*_attacks, sep = "\n")
        print("Damage")
        print(*_damage, sep = "\n")
        print("Heal: ")
        print(*_heal, sep = "\n")
        print("Kill: ")
        print(*_kill, sep = "\n")"""




if __name__ == "__main__":
    instance = ReadInput()
    jsonData = instance.ReadJsonData()
    removedNull = instance.RemoveNullSurveys(jsonData)
    

    #instance.WriteJsonData(removedNull)
    players = instance.SummarizeData(removedNull)
    instance.SummaryToXML("formatted_v4",players)
    #instance.WriteJsonData("sumarized",players)

"""
        print("Q 0 " + str(questionsCount[0]))
        print("Q 1 " + str(questionsCount[1]))
        print("Q 2 " + str(questionsCount[2]))
        print("Q 3 " + str(questionsCount[3]))
        print("Q 4 " + str(questionsCount[4]))
        print("Q 5 " + str(questionsCount[5]))
        print("Q 6 " + str(questionsCount[6]))"""
       
"""    while True:
        input_text = input()
        player = instance.ConvertInput(input_text)
        jsonData = instance.ReadJsonData()
        new_jsonData = instance.AddToDict(jsonData,player)
        instance.WriteJsonData(new_jsonData)
        for key, value in new_jsonData.items():
            print(key, ":", value)"""

            
    
    

# Get
#Time
#Collisions
#attacks
#Survey
#Level?
#Northmost Point?

