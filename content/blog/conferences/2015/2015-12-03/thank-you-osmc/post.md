Title: Thank you OSMC
Author: mickem
Tags: conference,osmc,nsclient

![OSMC]({static|osmc_logo.png} "OSMC")

About a week ago now I got home from the massive 10 year old [https://www.netways.de/en/events_trainings/osmc/](OSMC) which was an excellent conference as always.
And as I always say I learn new things ever year so if your based in Europe be sure to sign up for next year.

This year was rather special not only did I do the NSClient++ workshop for the second year I also had a really terrible presentation :)
But on the up side it is the first year where we had a hackathon and also the first year where we had feature fixed in real time.
During the conference a lot of people always comes up to me with problems, ideas and new features and usually I store it off away somewhere in a dark corner and bring it up when I have time. But this year, mainly due to the hackathon, three of them were implemented in almost real time which was pretty cool. So hopefully for next years hackathon we can implement even more features!

![hackathon]({static|hackathon.png} "The hackathon logo")

The three features were:
* Executing script into a user session
* Eventlog checking tags and tasks.
* Service classifications

# The workshop

The workshop was a great success or at least I thought so. As last year it was difficult to fit all the material in the allotted timeslot. But I think I managed it a bit better then last year.
As before a lot of minor issues and annoyances was found (all have since been fixed) so this is a great forum for me to find the minor things and oddities which people struggle with as I get to observe other people using NSClient++.
![workshop]({static|workshop.png} "The workshop logo")


## Executing scripts in a user session.

This is actually a long time requested feature and I have always said it is too difficult, but during the hackathon I did some google and found some code which was quite easy to add to NSClient++ so this feature was added live during the hackathon. The way this work is that you specify which session you want to execute the script in and it will be run there.

This is very useful if you want to start a program running visually on the desktop or a program which want to monitor the desktop.

    [/settings/external scripts/scripts/annoying_people_with_notepad]
    display=true
    session=1
    command=notepad.exe

Now if you schedule this to run every 5 minutes people will get an annoying notepad windows popping up: sweet huh?

## Service classification

My good friend [https://twitter.com/theflyingcorpse](Rune) came up to me with some custom scripts he had written and I asked why as they seemed to overlap built-in features. And when he explained the purpose of them I thought: Hey that sounds like a sweet idea. And during the hackathon I implemented it in real-time.

The way this feature works is that all standard windows services are classified as:

* essential
* role
* support
* ignored

And all other services are classified as;

* custom

So if you want to check only custom services (i.e. services which does not come with windows) you can use the following check:

    check_service classification=custom

## Eventlog task and keywords

This is another one of those things which has been on the TODO list for some time but after some people asking me about it during the flight home from Nuremberg I looked at it and implemented support for the the next few days.
So now you can do thinks like this:

    # Filter bsased on access privelages
    check_eventlog log=security "filter=task = 'SE_ADT_OBJECTACCESS_FILESYSTEM'"
    # Filter based on keyword
    check_eventlog unique "filter=keyword like 'install'" show-all "detail-syntax=%(message)"

# Thank you, see you all next year!

So next year: please hit me with your favorite monitoring need and we shall see if we can implement even more features!

// Michael Medin
