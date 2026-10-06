from itertools import combinations

#Make lists so we save there the existing and desired amounts of chocolate.
choco_list = []
kids_list = []

#Take the number of chocolates and kids
#Save all the existing lengths of chocolate
m = int(input('Give the amount of chocolates: '))
print('Give all the lengths of chocolates: ')
for ch in range(m):
    choco = int(input())
    choco_list.append((choco,ch))



#Save all the desired lengths
n = int(input('Give the number of the children: '))
print('Give all the length of chocolate each child wants: ')
for k in range(n):
    kid = int(input())
    kids_list.append((kid,k))



#according to the exercise there is always enough chocolate,
#but I add this step as testing that there was no error in inputs. 
if sum(x[0] for x in choco_list) < sum(x[0] for x in kids_list):
    print('Error. Not enough chocolates.')
    exit()

#I make this ghost kid in case the chocolates are more than the desired lengths, 
# so I can calculate more efficiently the combinations.
if sum(x[0] for x in choco_list) > sum(x[0] for x in kids_list):
        ghost_kid = sum(x[0] for x in choco_list) - sum(x[0] for x in kids_list)
        kids_list.append((ghost_kid,n))
else:
    ghost_kid = None




#Make tuples so they are unchangeable and safer.
kids_list = tuple(kids_list)
choco_list = tuple(choco_list)


#I set a maximum number of kids and chocolates to avoid 
# too many combinations that will cause exponential computation time.
#I suppose that setting them below a threshold of 5 is a good idea,
#because I suppose that the length of each chocolate is not extremely large,
# hence, it will be easy to find appropriate matching groups.
#If I don't find as many perfect matches as I wanted, 
# I can manually increase the maximum numbers.
if n < 5:
    max_kid = len(kids_list) #because in case I use a ghost kid, n != len(kids_list)
else:
    max_kid = 5

if m < 5:
    max_choco = m
else:
    max_choco = 5



#function that groups kids with chocolates, so that each group is "self-sufficient".
def match(kids_list, choco_list, max_kid, max_choco):
    #Take indexes of the number of kids and chocolates.
    #I first check if there are perfect "one to one" matches between kids and chocolates, to avoid cuts.  
    #I then use these indexes to try if combinations add to sums that match perfectly. 
    for i in range(1, max_kid+1):
        for j in range(1, max_choco+1):
            #i find all the combinations of kids and chocolates of length i and j
            #so I construct "groups" of kids and chocolates, in order to compare their total desired and existing lengths.
            #The process begins from groups of 1 kid and groups of 1 chocolate. 
            #So, I first check if there are perfect matches between 1 kid and 1 chocolate.
            #Then I have groups of 1 kid and groups of 2 chocolates. Then 1 kid and 3 chocolates. 
            #This way I search for combinations of chocolates that their lengths add perfectly
            # to the desired length of the kid. This process prevents cuts.
            for k in combinations(range(len(kids_list)), i):
                for ch in combinations(range(len(choco_list)), j):
                    if sum(kids_list[x][0] for x in k) == sum(choco_list[x][0] for x in ch):
                        group = (tuple(kids_list[x] for x in k), tuple(choco_list[x] for x in ch))
                        new_case = tuple([kids_list[x] for x in range(len(kids_list)) if x not in k]),\
                            tuple([choco_list[x] for x in range(len(choco_list)) if x not in ch])
                        return group, new_case
    return None

#takes each pair of kids-chocolates that their (desired & existing) sums match perfect, and cuts the chocolates appropriately. 
def cuts(group):
    cut = 0         #counts the number of cuts
    chocos_ingroup = group[1]
    kids_ingroup = group[0]
    ch = 0              #which chocolate I am sharing right now
    k = 0               #which kid is taking chocolate right now
    left = chocos_ingroup[ch][0]
    need = kids_ingroup[k][0]
    cut_list = [[] for a in range(len(kids_ingroup))] #gives for each child how many pieces we give from which chocolate



    #runs a chocolate and a kid in the "perfect subgroup". 
    #gives to the kid the chocolate.
    while ch < len(chocos_ingroup) :
        piece = min(left, need)
        left -= piece       #how many pieces left from the current chocolate
        need -= piece       #how many pieces the current kid needs to be full
        #adds for the current kid "(how many pieces took, from this chocolate)
        cut_list[k].append((piece, chocos_ingroup[ch][1]))   

        #If (kid took all desired length) AND (current chocolate isn't over), counts a cut and goes to the next kid.
        if (need == 0) and (left != 0):
            cut += 1

        #If chocolate ended, goes to the next chocolate.
        if left == 0:
            ch +=1
            #tests if chocolates in group ended
            if ch < len(chocos_ingroup):
                left = chocos_ingroup[ch][0]
        #If kid doesn't need more, goes to the next kid.
        if need == 0:
            k += 1
            #tests if kids in group ended
            if k < len(kids_ingroup):
                need = kids_ingroup[k][0]
    return cut, cut_list




def main():
    k_now = kids_list       # temporary list, for remaining kids, that will be updated after each match is found.
    ch_now = choco_list     # same as above, for remaining chocolates.
    final_groups = []       #"final_groups" is the list of matched groups ((kids), (chocolates)).
    while True:
        result = match(k_now, ch_now, max_kid, max_choco)
        if result is None:     #hence, if there are not remaining kids and chocolates to return
            break
        group, new_case = result  
        k_now, ch_now = new_case
        final_groups.append(group)

    if len(k_now) != 0 or len(ch_now) != 0:  
        final_groups.append((k_now, ch_now))

    total_cuts = 0
    all_pieces = []
    
    for group in final_groups:
        cut, cut_list = cuts(group)
        total_cuts += cut    
        for (want, kid_id), pieces in zip(group[0], cut_list):       
            for piece, bar_id in pieces:
                #the final triplets of (chocolate number, pieces we take, which kid takes them) 
                all_pieces.append((bar_id, piece, kid_id))


    all_pieces.sort()
    print(f'{"From chocolate no.":<22}{"of length":<12}{"we give":<11}{"to kid no.":<6}')
    print('-' * 55)
    for bar_id, piece, kid_id in all_pieces:
        if kid_id != n:
            print(f'{ bar_id+1 :<22}{(choco_list[bar_id][0]):<12}{piece:<11}{ kid_id+1 :<6}')
    
    
    if ghost_kid != None:
        print('Leftover chocolates of total length: ', ghost_kid)

    print('Total cuts are: ', total_cuts)


    estim = len(kids_list) - len(final_groups)
    if estim == total_cuts:
        print('Total cuts are the estimated.')
    else:
        print('There was a decomposable group. Total cuts are less than the estimated.')

main()
