from TimeFollow.models import Post

MONTHS = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December',
}

###### Timeline methods ######
def generateTimeline(posts: Post):
    sortedPosts = {'test': {'test': []}}
    
    for post in posts:
        date = post['timeStamp']
        year = str(date.year)
        month = date.month
        month = MONTHS[month]
        time = date.strftime("%H:%M")
        post = {'day':str(date.day), 'time':time, 'content':post['postContent']}

        if sortedPosts.get(year) is not None:
            if sortedPosts[year].get(month) is not None:
                sortedPosts[year][month].append(post)
            else:
                sortedPosts[year][month] = [post]
        else:
            sortedPosts[year] = {month: []}
            sortedPosts[year][month].append(post)
    sortedPosts.pop('test')
    return sortedPosts