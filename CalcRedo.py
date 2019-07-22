import random
import tkinter as tk
from tkinter import *
import tk_tools

def Main():
    root=tk.Tk()
    root.geometry("650x250")
    #root.configure(bg="grey")
    rerolltype=IntVar()
    rerolltype2=IntVar()
    rerolltype3=IntVar()
    var=IntVar()
    invuln=IntVar()
    Phase=""

    def Enter():
        Enterbutton.grid_remove()
        Nextbutton.grid(column=3)
        action_phase()
        Enterbutton.grid()
        Nextbutton.grid_remove()
      
    def Next():
        Messagescreen.insert("end-1c","Press 'Next' To Continue...")
        Nextbutton.wait_variable(var)
        Messagescreen.delete(1.0, "end-1c")

    def get_Wound_need():
        T=int(TargetT.get())
        S=int(WeaponS.get())
        if S>T: 
            if S>=2*T:
                wound_need=2
            else:
                wound_need=3
        elif S==T:
                wound_need=4
        elif S<T:
            if T>=2*S:
                wound_need=6
            else:
                wound_need=5
        return int(wound_need)

    def wound_counter(Wound_list):
        printto(Messagescreen,"Enter Toughness and Strength values:")
        Next()
        wounds_count=0
        T=int(TargetT.get())
        S=int(WeaponS.get())
        for wound in Wound_list:
            if S>T: 
                if S>=2*T:
                    if wound >= 2:
                        wound_need="2+"
                        wounds_count+=1
                else:
                    if wound >=3:
                        wound_need="3+"
                        wounds_count+=1
            if S==T:
                if wound >=4:
                    wound_need="4+"
                    wounds_count+=1
            if S<T:
                if T>=2*S:
                    if wound==6:
                        wound_need="6+"
                        wounds_count+=1
                else:
                    if wound >=5:
                        wound_need="5+"
                        wounds_count+=1
        printto(Stat_screen,"Needed: %s\nWounds: %s"%(wound_need,wounds_count))
        return wounds_count

    def saves_counter(Saves):
        printto(Messagescreen,"Enter Targets Save Value.")
        Next()
        is_invuln=int(invuln.get())
        save_value=int(TargetSave.get())
        AP=int(WeaponAP.get())
        savestomake=Saves
        save_need= save_value+AP
        saves=0
        failed=0
        for save in savestomake:
            if is_invuln==1:
                if save>= save_value:
                    saves+=1
                    save_need=save
            else:
                if save-AP>=save_value:
                    saves+=1
                else:
                    failed+=1
        printto(Stat_screen,"Saves Made: %s\nNeeded: %s"%(saves,save_need))
        return saves

    def showRerolls():
        rerollLabel.grid(row=8,column=4)
        NoneButton.grid(row=8,column=5)
        AllButton.grid(row=8,column=6)
        OnesButton.grid(row=8,column=7)
        Next()
        rerollLabel.grid_remove()
        NoneButton.grid_remove()
        AllButton.grid_remove()
        OnesButton.grid_remove()

    def reroll_action(Input,rerolltype,Phase):
        printto(Messagescreen,"Select Reroll Type.")
        showRerolls()
        reroll_type=rerolltype.get()
        reroll_list=Input
        count=0
        if Phase=='Hits':
            Need=int(BSamount.get())
        elif Phase=='Wounds':
            Need=get_Wound_need()
        if reroll_type==0:
            pass
        else:
            for reroll in reroll_list:
                if reroll_type==1:
                    if reroll==1:
                        reroll=random.randint(1,6)
                        reroll_list[count]=reroll
                elif reroll_type==2:
                    if reroll < Need:
                        reroll=random.randint(1,6)
                        reroll_list[count]=reroll
                else: pass
                count+=1
            reroll_list.sort()
            printto(DiceLog, reroll_list)
        return reroll_list

    def default():
        diceamount.insert(0,10)
        BSamount.insert(0,3)
        TargetT.insert(0,3)
        WeaponS.insert(0,4)
        TargetSave.insert(0,5)
        WeaponAP.insert(0,0)
    
    def clearscreen():
        Messagescreen.delete(1.0, "end-1c")
        DiceLog.delete(1.0, "end-1c")
        Stat_screen.delete(1.0, "end-1c")
        
    def printto(where,Text):
        where.delete(1.0, "end-1c")
        return where.insert("end-1c","%s\n"%(Text))

    def dice_roll(ans):
        results_list=[]
        amount=ans
        while amount>=1:
            roll=random.randint(1,6)
            results_list.append(roll)
            amount-=1
        results_list.sort()
        printto(DiceLog, results_list)
        return results_list

    def hit_counter(input_results_list):
        hits=0
        missed=0
        for shot in input_results_list:
            if shot ==1:
                missed+=1
            elif shot >= int(BSamount.get()):
                hits+=1
            else: missed +=1
        printto(Stat_screen, "Hits: %s\nMissed:%s"%(hits,missed))
        return hits
    
    def modifier_applier(input_list,Phase):
        printto(Messagescreen,"Select Modifier Value.")
        Next()
        mod_value=int(rerolltype3.get())
        count=0
        if Phase=="Saves" and invuln==1:
            pass
        else:
            for value in input_list:
                if value==1:
                    count+=1
                else:
                    value+=mod_value
                    input_list[count]= value
                    count+=1
            printto(DiceLog,input_list)
            return input_list
        
    def action_phase():
        clearscreen()
        Step1=To_hit()
        Step2=To_wound(Step1)
        To_save(Step2)
        printto(Messagescreen,"End Of Attack.\nPress 'Enter' To Start New Attack...")

    def To_hit():
        Phase='Hits'
        #printto(Messagescreen,"To Hit Phase")
        Hit_list=dice_roll(int(diceamount.get()))
        hit_counter(Hit_list)
        Next()
        Hit_list=reroll_action(Hit_list,rerolltype,Phase)
        hit_counter(Hit_list)
        Next()
        Hit_list=modifier_applier(Hit_list,Phase)
        Hits=hit_counter(Hit_list)
        Next()
        return Hits

    def To_wound(Hits):
        Phase='Wounds'
        Wound_list=dice_roll(Hits)
        wound_counter(Wound_list)
        Next()
        Wound_list=reroll_action(Wound_list,rerolltype,Phase)
        wound_counter(Wound_list)
        Next()
        Wound_list=modifier_applier(Wound_list,Phase)
        Wounds=wound_counter(Wound_list)
        return Wounds

    def To_save(Wounds):
        Phase="Saves"
        Saves_list=dice_roll(Wounds)
        saves_counter(Saves_list)
        Next()
        Saves_list=modifier_applier(Saves_list,Phase)
        saves_counter(Saves_list)






    #rerollButtons()
    rerollLabel=tk.Label(None,text="Select Rerolls:")
    #rerollLabel.grid(row=2, column=0)
    NoneButton=tk.Radiobutton(None, text="None",value=0,variable=rerolltype, indicatoron=0)
    #NoneButton.grid(row=2,column=1) ,
    AllButton=tk.Radiobutton(None, text="All Failed", value=2,variable=rerolltype,indicatoron=0)
    #AllButton.grid(row=2,column=2) ,
    OnesButton=tk.Radiobutton(None, text="Ones", value=1,variable=rerolltype,indicatoron=0)
    #OnesButton.grid(row=2,column=3)
    tk_tools.ToolTip(NoneButton, 'Do not reroll any failed  rolls.')
    tk_tools.ToolTip(AllButton, 'Reroll all failed rolls.')
    tk_tools.ToolTip(OnesButton, 'Reroll  results of 1.')


    #rerollLabel=tk.Label(None,text="Wound Rerolls:")
    #rerollLabel.grid(row=3, column=0)
    NoneButton=tk.Radiobutton(None, text="None",value=0,variable=rerolltype, indicatoron=0)
    #NoneButton.grid(row=3,column=1) ,
    AllButton=tk.Radiobutton(None, text="All Failed", value=2,variable=rerolltype,indicatoron=0)
    #AllButton.grid(row=3,column=2) ,
    OnesButton=tk.Radiobutton(None, text="Ones", value=1,variable=rerolltype,indicatoron=0)
    #OnesButton.grid(row=3,column=3) 
    tk_tools.ToolTip(NoneButton, 'Do not reroll any failed  rolls.')
    tk_tools.ToolTip(AllButton, 'Reroll all failed rolls.')
    tk_tools.ToolTip(OnesButton, 'Reroll  results of 1.')

    
    Modlabel=tk.Label(None,text="Modifer:")
    Modlabel.grid(row=4, column=0)
    Minusonebutton=tk.Radiobutton(None, text="-1",value=-1,variable=rerolltype3, indicatoron=0,width=4)
    Minusonebutton.grid(row=4,column=1) ,
    nonemodbutton=tk.Radiobutton(None, text="0", value=0,variable=rerolltype3,indicatoron=0,width=4)
    nonemodbutton.grid(row=4,column=2) ,
    Plusonebutton=tk.Radiobutton(None, text="+1", value=1,variable=rerolltype3,indicatoron=0,width=4)
    Plusonebutton.grid(row=4,column=3)
    tk_tools.ToolTip(Minusonebutton,  'Subtract one to dice rolls.')
    tk_tools.ToolTip(nonemodbutton, 'Do not modify dice rolls.')
    tk_tools.ToolTip(Plusonebutton, 'Add one to dice rolls\n"1"s still fail.')

    diceamountLabel= tk.Label(text="Enter Amount of Shots:")
    diceamountLabel.grid(row=0,column=0)
    diceamount= tk.Entry()
    diceamount.grid(row=0, column=1, columnspan=3)
    tk_tools.ToolTip(diceamount, 'enter a value between 1 and 100')

    BSamountLabel= tk.Label(text="Enter BS:")
    BSamountLabel.grid(row=1,column=0)
    BSamount= tk.Entry()
    BSamount.grid(row=1, column=1,columnspan=3)
    tk_tools.ToolTip(BSamount, 'enter a value between 2 and 6')
    
    Stat_screen=tk.Label(text="Stat Screen")
    Stat_screen.grid(row=0,column=4,padx=15)
    Stat_screen= tk.Text(root, width = 10, height = 5)
    Stat_screen.grid(row=1, column= 4, columnspan=1, rowspan=5)

    Messagescreen = tk.Text(root, width = 40, height = 2)
    Messagescreen.grid(row=6,column=4,columnspan=4,rowspan=2)
    
    DiceLogLabel=tk.Label(text="Dice Log")
    DiceLogLabel.grid(row=0,column=5)
    DiceLog= tk.Text(root, width= 30, height= 5)
    DiceLog.grid(row=1, column= 5, columnspan=3, rowspan=5)

    WeaponSLabel=tk.Label(text="Enter Weapons Strength:")
    WeaponSLabel.grid(row=5,column=0)
    WeaponS=tk.Entry(width=3)
    WeaponS.grid(row=5,column=1,columnspan=1)
    tk_tools.ToolTip(WeaponS, 'enter a numerical Value.')

    WeaponAPLabel=tk.Label(text="Enter Weapon's AP:")
    WeaponAPLabel.grid(row=6,column=0, sticky=E)
    WeaponAP=tk.Entry(width=3)
    WeaponAP.grid(row=6,column=1,columnspan=1)
    tk_tools.ToolTip(WeaponAP, 'enter a positive Number\n(-1 AP = "1")')

    TargetTLabel=tk.Label(text="Enter Targets Toughness:")
    TargetTLabel.grid(row=7,column=0,sticky=E)
    TargetT=tk.Entry(width=3)
    TargetT.grid(row=7,column=1,columnspan=1)
    tk_tools.ToolTip(TargetT, 'enter a numerical Value.')

    TargetSaveLabel=tk.Label(text="Enter Targets Save:")
    TargetSaveLabel.grid(row=8,column=0)
    TargetSave=tk.Entry(width=3)
    TargetSave.grid(row=8,column=1,columnspan=1)
    tk_tools.ToolTip(TargetSave, 'enter a value between 2 and 7')

    #Invuln_SaveLabel=tk.Label(text="Is Invulnerable Save?")
    #Invuln_SaveLabel.grid(row=9,column=0)
    Invuln_Save=tk.Checkbutton(root,text="Invuln",variable=invuln)
    Invuln_Save.grid(row=8,column=2)

    Enterbutton=tk.Button(text="Enter", command=Enter)
    Enterbutton.grid()
    Nextbutton=tk.Button(text="Next", command=lambda: var.set(1))
    #Nextbutton.grid(row=9,column=1)

    default()
    root.mainloop()
if __name__ == "__main__":
    Main()