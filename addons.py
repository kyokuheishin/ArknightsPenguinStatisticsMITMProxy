#-*- coding: utf-8 -*-
from mitmproxy import ctx
import mitmproxy.http
import json
import urllib
class BattleResult:
    def response(self,flow:mitmproxy.http.HTTPFlow):
        print(flow.request.host)
        if ("ak" in flow.request.host) and ("battleFinish" in flow.request.path):
            result = json.loads(flow.response.get_text())
            print("The stage's ID is %s" % list(result["playerDataDelta"]["modified"]["dungeon"]["stages"].keys())[0])
            print("Drop Items:")
            drops = []
            
            for r in result["rewards"]:
                print("ID: %s" % r["id"])
                print("Type: %s" % r['type'])
                print("Count: %s" % str(r['count']))
                drops.append({"itemId":r["id"],"quantity":r['count']})
            
            data = {"stageId":list(result["playerDataDelta"]["modified"]["dungeon"]["stages"].keys())[0],"drops":drops,"source":"penguin-stats-mitm-py","version":"v0.0.1"}
            if result["furnitureRewards"] != []:
                data["furniturenum"] = 1
            else:
                data["furniturenum"] = 0
            headers = {'Content-Type': 'application/json'}
            data_json = json.dumps(data)
            data_json = data_json.encode()
            request = urllib.request.Request("https://penguin-stats.io/report",headers=headers,data=data_json)
            res = urllib.request.urlopen(request)
            print(res.getcode())
        pass

addons = [
    BattleResult()
]