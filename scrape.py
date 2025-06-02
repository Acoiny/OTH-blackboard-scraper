from blackboard import Blackboard

if __name__ == "__main__":
    url = 'https://informatik-mathematik.oth-regensburg.de/schwarzes-brett'
    blackboard = Blackboard(url)
    blackboard.scrape()
    print(blackboard)
