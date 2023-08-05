def main():
    import tkinter
    import pip
    # try:
    #     pip.main(['install', '--upgrade', "autobuff"])
    # except:
    #     print("Couldnt update.")
    import customtkinter
    import threading
    from time import sleep
    import os
    from PIL import Image
    from tkinter import PhotoImage
    from tkinter import Wm
    import sys
    from tkinter import filedialog
    from pathlib import Path

    data_folder = Path("Images/")

    file = data_folder / "bg.jpg"
    
    STEAM = data_folder / "Test.png"
    VALO = data_folder / "VALORANT.PNG"
    ROBLOX = data_folder / "Roblox.png"
    
    exit = False

    def output_sentence(sentence, color):
        global text
        # Insert the sentence at the end of the text widget, using the color provided
        text.configure(state="normal")
        text.insert("end", f"{sentence}\n", color)  # Use the custom tag for the color and the "bold" tag to make the text bold
        # Update the window size to fit the output
        loginwin.update_idletasks()
        # Set the width of the window to the width of the output and the height to 600 pixels
        text.configure(state="disabled")
        text.tag_add("center", "1.0", "end")
        text.tag_config("center", justify='center')
        text.see("end")
    
    
    def MailScraper():
        
        if not exit:
            output_sentence("Sleeping to get new emails...","#000")
            output_sentence("—————","#000")
            for n in range(5):
                output_sentence(n+1, "#000")
                sleep(1)

            output_sentence("—————","#000")
        
        import easyimap as e
        import re
        host = "imap.gmail.com"
        server = e.connect(host, USER, PASS)

        def emails(n):
            global mail
            mail = server.mail(server.listids()[n])

        for n in range(10):
            emails(n)
            if mail.title == "Buff Game":
                output_sentence("Email Found","#000")
                output_sentence("————","#000")
                buffemail = server.mail(server.listids()[n])
                temp = re.findall(r'\d{6}', buffemail.body)
                res = list(map(int, temp))
                # output_sentence("The numbers list is : " + str(res))
            
                finalN = []
                
                for n in res:
                    if n not in finalN and n != 131517 and n != 165884 and n != 32419 and n != 29238:
                        finalN.append(n)
                
                output_sentence("Code is : " + str(finalN[-1]),"#000")
                break
            
        while True:
            try:
                Key = pg.locateCenterOnScreen(str(data_folder / "Key.png"), confidence=0.8)
                if Key != None:
                    break
            except:
                sleep("[ERR]Cant find text box")
                sleep(1)

        pg.click(Key.x, Key.y)
        pg.typewrite(str(finalN[-1]))
        sleep(0.5)
        try:
            confirm = pg.locateCenterOnScreen(str(data_folder / "confirm.png"), confidence=0.8)
            # pg.click(confirm.x, confirm.y)
            spam(msg, webhook)
        except:
            output_sentence("[err]","#000")
            sleep(0.5)
            
        

    def Program():
        global manual, pg, exit
        import pyautogui as pg
        from time import sleep
        import os
        from os import sys
        import pygetwindow as gw
        from time import sleep
        import requests
        
        global msg, webhook, spam
        msg = "@everyone AutoBuff Found the item in stock!!!."
        webhook = str(WebhookVar.get())
        def spam(msg, webhook):
            try:
                data = requests.post(webhook, json={'content': msg})
                if data.status_code == 204:
                    output_sentence("Message sent successfuly", "#fff")
            except:
                output_sentence("—————","#000")
                output_sentence("Bad Webhook :" + webhook, "#ddd")
                


        # def resource_path(relative_path):
        #     """ Get absolute path to resource, works for dev and for PyInstaller """
        #     try:
        #         # PyInstaller creates a temp folder and stores path in _MEIPASS
        #         base_path = sys._MEIPASS
        #     except Exception:
        #         base_path = os.path.realpath(".")

        #     return os.path.join(base_path, relative_path)

        # SHOP = resource_path("Main\SHOP.PNG")
        # BUY = resource_path("Main\BUY.PNG")
        # VALORANT = resource_path("Main\VALORANT.PNG")

        try:
                
            win = gw.getWindowsWithTitle('Buff App')[0] 
            win.activate()
            pg.keyDown("enter")
        except IndexError:
            output_sentence("Buff Games not launched.", "")
            exit = True
            text.configure(state="disabled")


        RefreshEvery = 1
        sleep(2)
        if manual:
           output_sentence("Starting in Manual Mode...", "")
           output_sentence("—————","#000")
        else:
            output_sentence("Starting in Auto Mode.", "")
            output_sentence("—————","#000")
            
        def Relode():
            sleep(RefreshEvery)
            shop = pg.locateCenterOnScreen(str(data_folder / "SHOP.PNG"), confidence=0.8)
            lounge = pg.locateCenterOnScreen(str(data_folder / "Lounge.png"), confidence=0.8)
            if lounge == None:
                lounge = pg.locateCenterOnScreen(str(data_folder / "LoungeG.jpg"), confidence=0.8)
                
            if shop == None:
                shop = pg.locateCenterOnScreen(str(data_folder / "ShopG.jpg"), confidence=0.8)
            if shop != None:
                pg.click(lounge.x, lounge.y)
                sleep(0.5)
                pg.click(shop.x, shop.y)
                pg.move(200, 0)
                sleep(0.5)
                
            Value = SettingsSelectVar.get()
            if Value == 2:
                Filter = pg.locateCenterOnScreen(str(data_folder / "Filter.jpg"), confidence=0.7)
                if Filter != None:
                    pg.click(Filter)
                    sleep(1)
                    Premium = pg.locateCenterOnScreen(str(data_folder / "premium.jpg"), confidence=0.8)
                    if Premium != None:
                        pg.click(Premium)
                        pg.moveTo(shop)
                        pg.move(200, 0)
                        sleep(1)
                    
                else:
                    output_sentence("Error finding Filters", "")
            
                
        Relode()

        n = 0
        while True:
            if exit == True:
                break
            pg.scroll(-n)
            sleep(1)
            product = pg.locateCenterOnScreen(str(image), confidence=0.8)
            

            if product != None:
                pg.click(product.x, product.y)
                sleep(2)
                Buy = pg.locateCenterOnScreen(str(data_folder / "BUY.PNG"), confidence=0.8)
                if Buy != None:
                    output_sentence("In Stock, Item clicked...","#000")
                    output_sentence("—————","#000")
                    pg.click(Buy.x, Buy.y)
                    if manual == False:
                        MailScraper()
                    if manual:
                        output_sentence("Trying the webhook", "")
                        spam(msg, webhook)
                        
                    break
                    
                else:
                    output_sentence("Out of Stock, Reloding Shop...","#000")
                    output_sentence("—————","#000")
                    Relode()

            else:
                output_sentence("Looking For Product...", "")
                n +=  n + 100
                Relode()
                sleep(3)
            
        
    def ConfigBtn():
        global manual
        SettingsWin()
        if os.path.isfile('save.txt'):
            with open('save.txt','r') as f:
                lines = [line.rstrip() for line in f]
                WebhookVar.set(lines[2])
        Manual()
        btn.configure(state=("disabled"), fg_color="#5d5d5d", text_color_disabled="#262626")
        global image, USER, PASS
        USER = str(entry1Var.get())
        PASS = str(entry2Var.get())
        
        value = radiobutton_var.get()
        
        if value == 1:
            image = STEAM
        elif value == 2:
            image = VALO
        elif value == 3:
            image = ROBLOX
        elif value == 4:
            filetypes = (('Image', '*.png'), ('Image', '*.jpg'))
            image = filedialog.askopenfile(filetypes=filetypes).name
        
        

    def Beginbtn():
        Begin.configure(state=("disabled"), fg_color="#5d5d5d", text_color_disabled="#262626")
        outputwindow()
        sleep(1)
        threading.Thread(target=Program).start()
        


            
    def outputwindow():
        global text, window
        window = customtkinter.CTkToplevel()
        window.geometry("200x200")
        window.resizable(width=False, height=False)
        window.title("Console Log")
        
        
        text = customtkinter.CTkTextbox(window, width=200, height=200, fg_color="#242424", text_color="#fff")
        text.place(relx=.5, rely=.5, anchor="center")
        
        def prevent_highlight(event):
            return "break"
        
        text.bind("<1>", prevent_highlight)
        
        window.wm_transient(loginwin)
        


    def exitP():
        global exit
        try:
            window.destroy()
            exit = True
        except:    
            pass
        loginwin.destroy() 
    
    def Manual():
        global manual
        manual = False
        if ManualVar.get() == "True":
            manual = True
        else:
            manual = False
    
    
    
    def SettingsWin():
        global SettingsSelectVar, WebhookVar, Begin
        frame.grid_forget()
        SettingsFrame = customtkinter.CTkFrame(loginwin, fg_color="#303030", border_color="#fff")
        SettingsFrame.grid(row=0)
        
        WebhookVar = tkinter.StringVar(frame)
        WebhookLabel = customtkinter.CTkLabel(SettingsFrame, text="Webhook-URL", font=customtkinter.CTkFont("Montserrat", 17, weight="bold"), text_color="#dadada")
        WebhookLabel.grid(sticky="news", column=0, row=0, pady=(0, 0))
        entry = customtkinter.CTkEntry(SettingsFrame, textvariable=WebhookVar, width=250, font=customtkinter.CTkFont("Montserrat", 14, weight="bold"), text_color="#dadada", border_color="#dadada", corner_radius=8)
        entry.grid(column=0, row=1, pady=(0, 0))
        
        
        SettingsSelectVar = customtkinter.IntVar(value=1)
        
        Regular = customtkinter.CTkRadioButton(SettingsFrame, text="Regular",variable=SettingsSelectVar, value=1, font=customtkinter.CTkFont("Montserrat", 17, weight="bold"), fg_color="#dadada", hover_color="#5d5d5d", corner_radius=0, border_width_checked=3)
        Regular.grid(column=0, row=3, pady=10)
        Premium = customtkinter.CTkRadioButton(SettingsFrame, text="Premium",variable=SettingsSelectVar, value=2, font=customtkinter.CTkFont("Montserrat", 17, weight="bold"), fg_color="#dadada", hover_color="#5d5d5d", corner_radius=0, border_width_checked=3)
        Premium.grid(column=0, row=4, pady=10, padx=50)
        
        Begin = customtkinter.CTkButton(SettingsFrame, text="Begin", font=customtkinter.CTkFont("Montserrat", 15, weight="bold"), command=Beginbtn, text_color="#000", fg_color="#c3c3c3", hover_color="#909090", corner_radius=10)
        Begin.grid(sticky="", pady=(10, 20) , column=0, row=5)
        
    

    loginwin = customtkinter.CTk()
    loginwin.geometry("700x600")
    loginwin.title("Auto Buff")
    backg = customtkinter.CTkImage(Image.open(data_folder / "bg.jpg"), size=(700, 600))


    loginwin.resizable(width=False, height=False)

    loginwin.iconbitmap(data_folder / "logo.ico")

    customtkinter.set_default_color_theme("green")

    backgg = customtkinter.CTkLabel(loginwin, image=backg).grid(row=0, column=0)

    frame = customtkinter.CTkFrame(loginwin, fg_color="#303030")
    frame.grid(row=0)
    btnframe= customtkinter.CTkFrame(frame, fg_color="#303030")
    btnframe.grid(column=0, row=9)

    label = customtkinter.CTkLabel(frame, text="User-Info", font=customtkinter.CTkFont("Montserrat", 30, weight="bold"), text_color="#dadada")
    label.grid(column=0, row=0)
    label2 = customtkinter.CTkLabel(frame, text="—————————————————", font=customtkinter.CTkFont("Montserrat", 17, weight="bold"), text_color="#dadada")
    label2.grid(column=0, row=1, pady=0)

    entry1Var = tkinter.StringVar(frame)
    gmailLabel = customtkinter.CTkLabel(frame, text="Gmail", font=customtkinter.CTkFont("Montserrat", 17, weight="bold"), text_color="#dadada")
    gmailLabel.grid(sticky="news", column=0, row=2, pady=(0, 0))
    entry = customtkinter.CTkEntry(frame, textvariable=entry1Var, width=250, font=customtkinter.CTkFont("Montserrat", 14, weight="bold"), text_color="#dadada", border_color="#dadada", corner_radius=8)
    entry.grid(column=0, row=3, pady=(0, 0))

    entry2Var = tkinter.StringVar(frame)
    passLabel = customtkinter.CTkLabel(frame, text="Password", font=customtkinter.CTkFont("Montserrat", 17, weight="bold"), text_color="#dadada")
    passLabel.grid(sticky="news", column=0, row=4, pady=(0, 0))
    entry2 = customtkinter.CTkEntry(frame, textvariable=entry2Var, width=250, font=customtkinter.CTkFont("Montserrat", 18, weight="bold"), text_color="#dadada", show="*", border_color="#dadada", corner_radius=8)
    entry2.grid(column=0, row=5)
    
    ManualVar = tkinter.StringVar(frame)
    
    ManualBtn = customtkinter.CTkSwitch(frame, text="Manual",width=0, font=customtkinter.CTkFont("Montserrat", 17, weight="bold"), command=Manual, variable=ManualVar, onvalue="True")
    ManualBtn.grid(sticky="", column=0, row=6, pady=(10, 0))
    
    
    btn = customtkinter.CTkButton(frame, text="Start", font=customtkinter.CTkFont("Montserrat", 15, weight="bold"), command=ConfigBtn, text_color="#000", fg_color="#c3c3c3", hover_color="#909090", corner_radius=10)
    btn.grid(sticky="", pady=(10, 20) , column=0, row=7)



    radiobutton_var = customtkinter.IntVar(value=1)
    # frame.grid_columnconfigure(1, weight=1)
    # frame.grid_columnconfigure((2, 3), weight=1)
    btn2 = customtkinter.CTkRadioButton(btnframe, text="Steam", width=10,variable=radiobutton_var, value=1, font=customtkinter.CTkFont("Montserrat", 17, weight="bold"), fg_color="#dadada", hover_color="#5d5d5d", corner_radius=0, border_width_checked=3)
    btn2.grid(sticky="news", column=0, row=0, pady=10, padx=70, columnspan=1)
    btn3 = customtkinter.CTkRadioButton(btnframe, text="Valorant",width=10, variable=radiobutton_var, value=2, font=customtkinter.CTkFont("Montserrat", 17, weight="bold"), fg_color="#dadada", hover_color="#5d5d5d", corner_radius=0, border_width_checked=3)
    btn3.grid(sticky="news", column=0, row=1, pady=10, padx=70, columnspan=1)
    btn4 = customtkinter.CTkRadioButton(btnframe, text="Roblox",width=10, variable=radiobutton_var, value=3, font=customtkinter.CTkFont("Montserrat", 17, weight="bold"), fg_color="#dadada", hover_color="#5d5d5d", corner_radius=0, border_width_checked=3)
    btn4.grid(sticky="news", column=0, row=2, pady=10, padx=70, columnspan=1)
    btn5 = customtkinter.CTkRadioButton(btnframe, text="Custom", width=10,variable=radiobutton_var, value=4, font=customtkinter.CTkFont("Montserrat", 17, weight="bold"), fg_color="#dadada", hover_color="#5d5d5d", corner_radius=0, border_width_checked=3)
    btn5.grid(sticky="news", column=0, row=3, pady=10, padx=70, columnspan=1)


    logoIMG = customtkinter.CTkImage(Image.open(data_folder / "logo.png"), size=(70, 80))
    logo = customtkinter.CTkLabel(btnframe , image=logoIMG, text="").grid(column=0, row=5, sticky="news", pady=(20, 13))

    creds = customtkinter.CTkButton(frame, text="Made By SDK", fg_color="#c3c3c3", hover_color="#909090",text_color="#000", font=customtkinter.CTkFont("Montserrat", 17, weight="bold"))
    creds.grid(column=0, row=10, sticky="we")


    if os.path.isfile('save.txt'):
        with open('save.txt','r') as f:
            lines = [line.rstrip() for line in f]
            entry1Var.set(lines[0])
            entry2Var.set(lines[1])
        
    try:
        loginwin.protocol("WM_DELETE_WINDOW", exitP)
    except:
        pass    

    loginwin.mainloop()

    with open('save.txt','w') as f:
        f.write(entry1Var.get() + "\n")
        f.write(entry2Var.get() + "\n")
        try:
            f.write(WebhookVar.get())
        except NameError:
            f.write("Your Webhook")
main()