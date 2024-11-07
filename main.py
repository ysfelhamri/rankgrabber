import requests
from riotwatcher import RiotWatcher, LolWatcher, ApiError
import tkinter
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
window = customtkinter.CTk()
window.geometry("300x380")
window.resizable(False, False)
window.title("Rank grabber")

account_regions = ["EUROPE","AMERICAS","ASIA"]
regions = ["EUW1","EUN1","NA1","BR1","LA1","LA2","JP1","KR","OC1"]
queuetypes = ["Solo/Duo","Flex"]
errdis = ["Success","api_key.txt doesn't exist \n or can't be opened","Invalid api key","Please fill all fields"
,"Invalid name","output.txt can't be created","A connection error has occurred","An unknown error has occurred"]

def showerr(errindx):
    if errindx == 0:
        dis.configure(text = errdis[errindx],text_color = "Green")
    else :
        dis.configure(text = errdis[errindx],text_color = "Red")
    dis.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

def callapi():
    
    try:
        requests.head("http://google.com",timeout=1)
    except Exception:
        showerr(6)
        return


    if dis.winfo_viewable():
        dis.place_forget()


    name = entry1.get()
    tag = tagtxt.get()
    region = rankmenu.get()
    if (qmenu.get()==queuetypes[0]):
        q="RANKED_SOLO_5x5"
    else:
        q="RANKED_FLEX_SR"


    try:
        open("api_key.txt",'r')
    except IOError:
        showerr(1)
        return

    api_key = open("api_key.txt",'r')
    api_txt = api_key.read().strip()

    
    if(len(name)==0 or len(region)==0 or len(tag)==0):
        showerr(3)
        return

    accregion = ""
    if region == regions[0] or region == regions[1]:
        accregion = account_regions[0]
    elif region == regions[2] or region == regions[3] or region == regions[4] or region == regions[5]:
        accregion = account_regions[1]
    elif region == regions[6] or region == regions[7] or region == regions[8]:
        accregion = account_regions[2]

    riotw=RiotWatcher(api_txt)
    account = ""
    try:
        account = riotw.account.by_riot_id(accregion,name,tag)
    except ApiError as err:
        print(err)
        if err.response.status_code == 404:
            showerr(4)
            return
        elif err.response.status_code == 403:
            showerr(2)
            return
        else:
            showerr(7)
            return



    lolw=LolWatcher(api_txt)
    try:
        lolw.summoner.by_puuid(region, account['puuid'])
    except ApiError as err:
        if err.response.status_code == 404:
            showerr(4)
            return
        elif err.response.status_code == 403:
            showerr(2)
            return
        else:
            showerr(7)
            return
    userinfo = lolw.summoner.by_puuid(region,account['puuid'])
    rank = lolw.league.by_summoner(region,userinfo['id'])

    try:
        open("output.txt","w")
    except IOError:
        showerr(5)
        return

    output = open("output.txt","w", encoding="utf-8")

    if(len(rank)==0):
        txt = [name," is unranked"]
        output.writelines(txt)
    else:
        flag =0
        for rnk in rank:
            if rnk['queueType'] == q:
                disrnk = rnk
                flag =1
        if flag==0:
            txt = [name," is unranked"]
            output.writelines(txt)
        else:
            txt = [name,"\n",disrnk['tier']," ",disrnk['rank']," ",str(disrnk['leaguePoints'])," LP","\n",str(disrnk["wins"]),'W/',str(disrnk["losses"]),'L']
            output.writelines(txt)

    dis.configure(text_color= "Green") 
    showerr(0)



def refresh(event=None):
    callapi()
    window.after(900000,refresh)


window.bind('<Return>', refresh)
frame = customtkinter.CTkFrame(master = window, width=270, height=280,corner_radius=10)
frame.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)
insideframe = customtkinter.CTkFrame(master = frame, width=250, height=180,corner_radius=10)
insideframe.place(relx=0.5, rely=0.35, anchor=tkinter.CENTER)
dis = customtkinter.CTkLabel(master = window,text_color = "Red" ,text_font=('',12))


label1= customtkinter.CTkLabel(master = insideframe  , text = "Name :",text_font=('',12))
label1.place(relx=0.2, rely=0.2, anchor=tkinter.CENTER)


entry1 = customtkinter.CTkEntry(master = insideframe  , width=95, height=40,corner_radius=10,justify='center', text_font=('',12),fg_color='#2B2D2F')
tagtxt = customtkinter.CTkEntry(master = insideframe  , width=50, height=40,corner_radius=10,justify='center', text_font=('',12),fg_color='#2B2D2F', placeholder_text="#")
entry1.place(relx=0.54, rely=0.2, anchor=tkinter.CENTER)
tagtxt.place(relx=0.85, rely=0.2, anchor=tkinter.CENTER)



label2= customtkinter.CTkLabel(master = insideframe  , text = "Region :",text_font=('',12))
label2.place(relx=0.2, rely=0.5, anchor=tkinter.CENTER)


rankmenu = customtkinter.CTkOptionMenu(master = insideframe  , width=150, height=40,values = regions,corner_radius=10, text_font=('',12),fg_color='#2B2D2F',button_color='#212325',button_hover_color='#242628')
rankmenu.place(relx=0.65, rely=0.5, anchor=tkinter.CENTER)

label3= customtkinter.CTkLabel(master = insideframe  , text = "Queue :",text_font=('',12))
label3.place(relx=0.2, rely=0.8, anchor=tkinter.CENTER)


qmenu = customtkinter.CTkOptionMenu(master = insideframe  , width=150, height=40,values = queuetypes,corner_radius=10, text_font=('',12),fg_color='#2B2D2F',button_color='#212325',button_hover_color='#242628')
qmenu.place(relx=0.65, rely=0.8, anchor=tkinter.CENTER)


button = customtkinter.CTkButton(master = frame , command=refresh,text = "Get data",height=40,corner_radius=25, text_font=('',12))
button.place(relx=0.5, rely=0.825, anchor=tkinter.CENTER)


window.mainloop()
