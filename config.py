import datetime

# pobranie daty
today = datetime.date.today()
year, week, weekday = today.isocalendar()

# wyliczenie i sformatowanie dni "od" i "do"
date_from = today - datetime.timedelta(days=weekday-1)
date_to = date_from + datetime.timedelta(days=6)
date_from = date_from.strftime("%d.%m.%Y")
date_to = date_to.strftime("%d.%m.%Y")


link = r'https://online.focusmr.com/ActionFocusOnline/app.iface?action=restoreSearch&recentSearchId=29778102&rnd=f2b8b027-97ef-49b5-879b-c5bcd7006b89&country=pl&appMode=standard'
directory = r'P:\Production\Clients\GlobalCosmed\SkanyTyg'
directory_it = r'P:\IT\GlobalCosmed\ActionFOCUS_3409_GC_Skany.zip'
file_name = r'ActionFOCUS_3409_GC_Skany_Week_' + str(week)
