import random

#roll dice
    #generates a list of dice based on [ans] provided by user
def dice_roll(ans):
        results_list=[]
        amount=ans
        while amount>=1:
            roll=random.randint(1,6)
            results_list.append(roll)
            amount-=1
        #sorts the list by numerical order
        results_list.sort()
        return results_list
#modifier application
    #ensures that negative and positive modifiers are correctly applied in accordance with rules
    #takes previously generated list and applies the user variable to each dice result in list
def modifier_applier(input_list):
    mod_value=int(input("What is the modifier?: "))
    count=0
    #itterates through each dice result in order
    for value in input_list:
        value= value+mod_value
        input_list[count]= value
        count+=1
    
    return input_list



#count Hits/miss
    #counts hits in list based on user provided BS
def hit_counter(input_results_list):
    hits=0
    missed=0
    for shot in input_results_list:
        if shot >= BS:
            hits+=1
        else: missed +=1
    return hits
    #counts missed in list based on user provided BS
def miss_counter(input_results_list):
    hits=0
    missed=0
    for shot in input_results_list:
        if shot >= BS:
            hits+=1
        else: missed +=1
    return missed
    



#reroll
    #takes a previously generated list and allows user to reroll selected values of dice
def reroll_counter(input_list):
    #determine if the user wants to reroll all results of '1' or all failed results
    reroll_type= input("\n1's [1]; All [2]; or None[Enter]: ")
    reroll_list=input_list
    count=0
    #iterate through each result in list
    for reroll in reroll_list:
        if reroll_type!=1 or 2:
            pass
        if reroll_type==1:
            if reroll ==1:
                #simulate rerolling the dice
                reroll=random.randint(1,6)
                print("this",reroll)
                #Counter places dice back into list
                reroll_list[count]=reroll
        if reroll_type==2:
            if reroll < BS:
                #simulate rerolling the dice
                reroll=random.randint(1,6)
                #counter places dice back into list
                reroll_list[count]=reroll
        else: pass
        count+=1
    #Sort all dice in numerical order 
    reroll_list.sort()
    return reroll_list


#wound Roll
def wound_list_creator(num_hits):
    wound_list=dice_roll(num_hits)
    wound_list.sort()
    return wound_list



#wound rerolls

def wound_counter(T,S,input_list):
    wounds_count=0
    for wound in input_list:
        #dice rolls of 1 are always a failure
        #when Weapon Strength is greater than the targets toughness
        if S>T:
            #test if the strength is 2 times as great or more than the toughness
            if S>=2*T:
                #if yes than dice rolls of 2+ cause wounds
                if wound >= 2:
                    wounds_count+=1
            else:
                #if no then wound rolls of 3+ cause wounds
                if wound >=3:
                    wounds_count+=1
        if S==T:
            #if strength is equal to toughness dice roll of 4+ cause wounds
            if wound >=4:
                wounds_count+=1
        #when Weapon Strength is less than the targets toughness
        if S<T:
            #test if the toughness is 2 times as great or more than the weapon strength
            if T>=2*S:
                #dice roll of 6+ is needed
                if wound==6:
                    wounds_count+=1
            else:
                #dice roll of 5+ is needed
                if wound >=5:
                    wounds_count+=1
    return wounds_count


#save rolls
def save_roll_creator(num_wounds):
    save_roll_list=dice_roll(num_wounds)
    save_roll_list.sort()
    return save_roll_list

#save counter
def save_test_creator(input_list,AP,save_value):
    saves=0
    failed=0
    for save in input_list:
        if save-AP>=save_value:
            saves+=1
        else:
            failed+=1
    return saves



count=1
while count==1:
    #info
    print("")
    print("")
    print("")
    print("")
    print("\n[New Attack Start]\n")
    print("----------------------")
        #Gather info on number of shots and model skill
    answer=int(input("\nEnter number of dice to roll: "))
    BS = int(input("Enter Ballistic Skill value: "))

    #hits
        #generate Hit roll list
    results = dice_roll(answer)
        #show hit roll list
    print("The results are: \n",results)
        #determine number of hits and misses based on BS
    hit_results= hit_counter(results)
    miss_results= miss_counter(results)
        #show results
    print("\nHit results: ",hit_results)
    print("\nMiss results: ",miss_results)
    
    #reroll
    print('---------------------------------------')
        #gather info on available rerolls
    print("\nAny available Rerolls?")
        #feed Results list into reroll function
    updated_list=reroll_counter(results)
        #feed Reroll list into modifier function
    updated_list=modifier_applier(updated_list)
        #show New List with rerolls and Modifiers applied
    print("Updated List Results: \n",updated_list)
        #determine number of hits and misses updated
    hit_results= hit_counter(results)
    miss_results= miss_counter(results)
        #show hits and misses
    print("\nHit results: ",hit_results)
    print("\nMiss results: ",miss_results)
    
    #wounds
    Wound_rolls=wound_list_creator(hit_results)
    print("\nWound Rolls: \n",Wound_rolls)
   
   
    #wounds reroll
    print("\nAny Avaiable Rerolls?")
    Wound_rolls=reroll_counter(Wound_rolls)
    Wound_rolls=modifier_applier(Wound_rolls)
    print("\nWound rolls after rerolls: \n",Wound_rolls)
   
    #wounds final
        #gather info on target and weapon
    toughness=int(input("What is targets Toughness?: "))
    Strength=int(input("What is the Weapons Strength?: "))
    AP=int(input("What is the Weapon AP value?: "))
        #run wound_counter fucntion
    num_wounds=wound_counter(toughness,Strength,Wound_rolls)
        #show Number of wounds
    print("Number of wounds: \n",num_wounds)
   
    #saves
        #Generate save roll list
    Save_roll=save_roll_creator(num_wounds)
        #show Save Roll List
    print("Save roll List: \n",Save_roll)
        #gather info on targets save value
    save_value=int(input("what is the Targets save value?: "))
        #determine if save roll is suffecient
    successful_saves=save_test_creator(Save_roll,AP,save_value)
        #show Successful saves and failed saves
    print("Number of successful saves: ",successful_saves)
    print("Number of Failed saves: ",num_wounds-successful_saves)


    #totals



#update list

    
        
 




