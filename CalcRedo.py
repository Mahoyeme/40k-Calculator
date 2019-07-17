import random
import tkinter as tk
from tkinter import *

def Main():
    root=tk.Tk()
    root.geometry("800x500")
    rerolltype=IntVar()
    rerolltype2=IntVar()
    rerolltype3=IntVar()
    var=IntVar()

    def Enter():
        Enterbutton.grid_remove()
        Nextbutton.grid(row=9,column=1)
        action_phase()
        Enterbutton.grid(row=9,column=0)
        Nextbutton.grid_remove()
      
    def Next():
        Messagescreen.insert("end-1c","Press 'Next' To Continue...")
        Nextbutton.wait_variable(var)
        Messagescreen.delete(1.0, "end-1c")

    def wound_counter(input_list):
        printto(Messagescreen,"Enter Toughness and Strength values:")
        Next()
        hits=hit_counter(input_list)
        wound_rolls=dice_roll(hits)
        wound_rolls=reroll_action(wound_rolls,rerolltype2)
        wound_rolls=modifier_applier(wound_rolls)
        wounds_count=0
        T=int(TargetT.get())
        S=int(WeaponS.get())
        for wound in wound_rolls:
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
        
        printto(Hit_MissScreen,"Needed: %s\nWounds: %s"%(wound_need,wounds_count))
        return wounds_count

    def Save_action(count):
        printto(Messagescreen,"Enter Targets Save Value.")
        Next()
        save_value=int(TargetSave.get())
        AP=int(WeaponAP.get())
        savestomake=dice_roll(count)
        savestomake=modifier_applier(savestomake)
        save_need= save_value+AP
        saves=0
        failed=0
        for save in savestomake:
            if save-AP>=save_value:
                saves+=1
            else:
                failed+=1
        printto(Hit_MissScreen,"Saves Made: %s\nNeeded: %s"%(saves,save_need))
        return saves

    def reroll_action(Input,rerolltype):
        printto(Messagescreen,"Select Reroll Type.")
        Next()
        reroll_type=rerolltype.get()
        reroll_list=Input
        count=0
        if reroll_type==0:
            pass
        else:
            for reroll in reroll_list:
                if reroll_type==1:
                    if reroll==1:
                        reroll=random.randint(1,6)
                        reroll_list[count]=reroll
                elif reroll_type==2:
                    if reroll < int(BSamount.get()):
                        reroll=random.randint(1,6)
                        reroll_list[count]=reroll
                else: pass
                count+=1
            reroll_list.sort()
            hit_counter(reroll_list)
            printto(DiceLog, reroll_list)
        return reroll_list

    def rerollButtons():
        rerollLabel=tk.Label(None,text="Hit Rerolls::")
        rerollLabel.grid(row=2, column=0)
        NoneButton=tk.Radiobutton(None, text="None",value=0,variable=rerolltype, indicatoron=0)
        NoneButton.grid(row=2,column=1) ,
        AllButton=tk.Radiobutton(None, text="All Failed", value=2,variable=rerolltype,indicatoron=0)
        AllButton.grid(row=2,column=2) ,
        OnesButton=tk.Radiobutton(None, text="Ones", value=1,variable=rerolltype,indicatoron=0)
        OnesButton.grid(row=2,column=3) 

        rerollLabel=tk.Label(None,text="Wound Rerolls:")
        rerollLabel.grid(row=3, column=0)
        NoneButton=tk.Radiobutton(None, text="None",value=0,variable=rerolltype2, indicatoron=0)
        NoneButton.grid(row=3,column=1) ,
        AllButton=tk.Radiobutton(None, text="All Failed", value=2,variable=rerolltype2,indicatoron=0)
        AllButton.grid(row=3,column=2) ,
        OnesButton=tk.Radiobutton(None, text="Ones", value=1,variable=rerolltype2,indicatoron=0)
        OnesButton.grid(row=3,column=3) 
        
        rerollLabel=tk.Label(None,text="Modifer:")
        rerollLabel.grid(row=4, column=0)
        Minusonebutton=tk.Radiobutton(None, text="-1",value=-1,variable=rerolltype3, indicatoron=0)
        Minusonebutton.grid(row=4,column=1) ,
        nonemodbutton=tk.Radiobutton(None, text="0", value=0,variable=rerolltype3,indicatoron=0)
        nonemodbutton.grid(row=4,column=2) ,
        Plusonebutton=tk.Radiobutton(None, text="+1", value=1,variable=rerolltype3,indicatoron=0)
        Plusonebutton.grid(row=4,column=3) 

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
        Hit_MissScreen.delete(1.0, "end-1c")
        
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
        printto(Hit_MissScreen, "Hits: %s\nMissed:%s"%(hits,missed))
        return hits
    
    def modifier_applier(input_list):
        printto(Messagescreen,"Select Modifier Value.")
        Next()
        mod_value=int(rerolltype3.get())
        count=0
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
        dice_list=[]
        dice_list=dice_roll(int(diceamount.get()))
        hit_counter(dice_list)
        dice_list=reroll_action(dice_list,rerolltype)
        dice_list=modifier_applier(dice_list)
        dice_list=wound_counter(dice_list)
        Save_action(dice_list)
        printto(Messagescreen,"End Of Attack.\nPress 'Enter' To Start New Attack...")

    rerollButtons()
    

    diceamountLabel= tk.Label(text="Enter Amount of Shots:")
    diceamountLabel.grid(row=0,column=0)
    diceamount= tk.Entry()
    diceamount.grid(row=0, column=1, columnspan=3)

    BSamountLabel= tk.Label(text="Enter BS:")
    BSamountLabel.grid(row=1,column=0)
    BSamount= tk.Entry()
    BSamount.grid(row=1, column=1,columnspan=3)
    
    Hit_MissScreen=tk.Label(text="Hits & Misses")
    Hit_MissScreen.grid(row=0,column=4,padx=10)
    Hit_MissScreen= tk.Text(root, width = 10, height = 5)
    Hit_MissScreen.grid(row=1, column= 4, columnspan=1, rowspan=5)

    Messagescreen = tk.Text(root, width = 30, height = 2)
    Messagescreen.grid(row=6,column=4,columnspan=2,rowspan=3)
    
    DiceLogLabel=tk.Label(text="Dice Log")
    DiceLogLabel.grid(row=0,column=5)
    DiceLog= tk.Text(root, width= 30, height= 5)
    DiceLog.grid(row=1, column= 5, columnspan=1, rowspan=5)

    WeaponSLabel=tk.Label(text="Enter Weapons Strength:")
    WeaponSLabel.grid(row=5,column=0)
    WeaponS=tk.Entry()
    WeaponS.grid(row=5,column=1,columnspan=3)

    WeaponAPLabel=tk.Label(text="Enter Weapon's AP:")
    WeaponAPLabel.grid(row=6,column=0)
    WeaponAP=tk.Entry()
    WeaponAP.grid(row=6,column=1,columnspan=3)

    TargetTLabel=tk.Label(text="Enter Targets Toughness:")
    TargetTLabel.grid(row=7,column=0)
    TargetT=tk.Entry()
    TargetT.grid(row=7,column=1,columnspan=3)

    TargetSaveLabel=tk.Label(text="Enter Targets Save:")
    TargetSaveLabel.grid(row=8,column=0)
    TargetSave=tk.Entry()
    TargetSave.grid(row=8,column=1,columnspan=3)

    Enterbutton=tk.Button(text="Enter", command=Enter)
    Enterbutton.grid(row=9,column=0)
    Nextbutton=tk.Button(text="Next", command=lambda: var.set(1))
    #Nextbutton.grid(row=9,column=1)

    
    
    default()
    root.mainloop()
    


if __name__ == "__main__":
    Main()