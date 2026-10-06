chocolates-distribution
# Distributing chocolate bars among children with the fewest cuts.


## The PROBLEM:
There are m chocolate bars of varying (integer) length and n hungry children who want differing
amounts of chocolate (again integer values). You can cut the chocolate bars in a way that every
child gets the desired amount. Write a programme to distribute the chocolate using the least
number of cuts.

Example: 
Suppose that 3 chocolate bars have lengths {2,5,7} and 4 children want {3,2,5,1}. As a
result, you can solve the problem by making 2 cuts.
We are more interested in solutions that get close to the least possible time required, rather
than those that take an exponential amount of time. 


## The logic I use is the following: 
I first add up all the desired amounts and I add up all the existing amounts of chocolate.

According to the exercise, the chocolates are always enough for the children.
According to the example, the chocolates can be more than the desired amount.

Hence, I create (if needed) a ghost child, in order to have (desired amount) = (existing amount).

Then, I search if there are kids and chocolates with lengths that match perfect. If yes, I give them the corresponding chocolates and keep them apart.
Then, I search if there are kids that can take exactly 2 whole chocolates. If yes, I give the chocolates. 
I do the same, for 3 whole chocolates, etc.
Hence, each of these children take whole chocolates, hence, they need 0 cuts.

Then, I only remain with the kids that will need some cut of chocolates (or whole chocolate + a cut, etc.). 
I create groups of kids and chocolates, such that inside the group I have exactly (desired amount in group) = (existing amount in group).

Inside the groups that I have made I (ideally) cannot find subgroups that satisfy (desired amount in subgroup of kids) = (existing amount in subgroup of chocolates).
This has to do with the total numbers of kids and chocolates: if the crowds are large, the combinations I must do are too many.
Then, I choose to sacrifice some cuts, so I will not have exponential computation time.
Also, I cannot find in these groups a perfect match between 1 kid <-> some chocolates, because this work was also done before.

I do the distribution inside each group. I put the kids in (any) order and the chocolates in (any) order.
I give to the 1st kid a part of the 1st chocolate 
(or the whole 1st chocolate and a part of the 2nd chocolate, or the whole 1st and 2nd chocolate and a part of the 3rd, etc.)
Then, I give the remaining (or part of the remaining) chocolate to the 2nd kid, etc.

I said that (ideally) there are not "subgroups" in the groups as I explained above. 
So, I will need to make exactly 1 cut for every kid, except the last kid that will need 0 cuts, that will take the remaining piece (or the remaining piece and one (or more) whole chocolate).

Hence, in the ideal case (no subgroups case), 
if there are $x_i$  kids in the  $i_{th}$ group, then, I will have exactly $x_i - 1$ cuts. 
We said that the kids that take whole chocolates need 0 cuts.
So, the total amount of cuts is $\Sigma_{i} ( x_i - 1 )$.

So, for every case (ideal or not), an upper bound for the total amount of cuts is  $\Sigma_{i} ( x_i - 1 )$.

Let it be $w$ the number of kids with whole chocolates.
Let it be $g$ the number of groups (including those with kid that takes whole chocolate(s)).
So, the total amount of cuts is at most:

$\Sigma_{i} ( x_i - 1 )                           = $
$\Sigma_{i} ( x_i - 1 ) + w - w                   = $
$\Sigma_{i} ( x_i )     + w     - \Sigma_{i} (1) - w =         n                  -        g $

Therefore, the total amount of cuts is at most $n - g$, where $n$ is the number of kids and $g$ is the number of groups.
